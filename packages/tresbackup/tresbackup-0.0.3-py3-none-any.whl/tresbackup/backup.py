# coding=utf-8
from argparse import ArgumentParser
from collections import deque
from dataclasses import dataclass, is_dataclass, asdict
from io import BufferedReader, RawIOBase
from json import load, dump, dumps, JSONEncoder, loads
from logging import Handler, StreamHandler, INFO, Formatter, getLogger, info, exception, warning
from os.path import join
from re import compile as regexp_compile
from shutil import move
from typing import List, Dict, Pattern, Any, Generator, Tuple
from zipfile import ZipFile, ZIP_BZIP2

from dataclasses_json import dataclass_json
from elasticsearch import Elasticsearch
from elasticsearch.client.indices import IndicesClient
from elasticsearch.helpers import scan, parallel_bulk
from ijson import items as stream_ijson
from stream_unzip import stream_unzip
from tqdm import tqdm
# noinspection PyPackageRequirements
from zipstream import ZipStream


class EnhancedJSONEncoder(JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


def default_handler() -> Handler:
    console = StreamHandler()
    console.setLevel(INFO)
    formatter = Formatter('[%(asctime)s] %(levelname)s %(name)s '
                          '%(threadName)s '
                          '{%(pathname)s:%(lineno)d} '
                          ' - %(message)s')
    console.setFormatter(formatter)
    return console


@dataclass_json
@dataclass
class IndexMetadata(object):
    """
    This set of index properties should be enough to check whether index has changed
    """
    docs_num: int
    docs_deleted: int
    store_size_bytes: int
    index_total: int
    index_time_in_millis: int

    @staticmethod
    def load_metadata(filepath: str) -> Dict[str, 'IndexMetadata']:
        try:
            with open(filepath, mode="rt", encoding="utf-8") as f:
                dict_data: Dict[str, Any] = load(f)
                return {k: IndexMetadata.from_dict(v) for k, v in dict_data.items()}
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_metadata(obj: Dict[str, 'IndexMetadata'], filepath: str) -> None:
        temp_file = filepath + ".tmp"
        with open(temp_file, mode="wt", encoding="utf-8") as f:
            dump(obj, f, indent=2, cls=EnhancedJSONEncoder)
        move(temp_file, filepath)


def list_indexes(
    es: Elasticsearch,
    indexes: List[str],
    exclude: Pattern,
    request_timeout: int
) -> Dict[str, IndexMetadata]:
    ic: IndicesClient = es.indices
    stats: Dict[str, Any] = ic.stats(index=indexes, request_timeout=request_timeout)
    indices_stats: Dict[str, Any] = stats["indices"]
    filtered: Dict[str, Any] = {k: v for k, v in indices_stats.items() if not exclude.match(k)}
    result: Dict[str, IndexMetadata] = {}
    for index_name, index_stats in filtered.items():
        total: Dict[str, Any] = index_stats["total"]
        docs: Dict[str, int] = total["docs"]
        store: Dict[str, int] = total["store"]
        indexing: Dict[str, int] = total["indexing"]
        result[index_name] = IndexMetadata(
            docs_num=docs["count"],
            docs_deleted=docs["deleted"],
            store_size_bytes=store["size_in_bytes"],
            index_total=indexing["index_total"],
            index_time_in_millis=indexing["index_time_in_millis"],
        )
    return result


def backup(
    elastic: Elasticsearch,
    index_name: str,
    backup_path: str,
    meta_path: str,
    state: Dict[str, IndexMetadata],
    curr_state: IndexMetadata,
    batch_size: int,
    scroll_time: str,
    request_timeout: int,
    compression_level: int,
) -> None:
    def es_docs_generator(total_docs: int) -> Generator[Dict[str, Any], None, None]:
        bar = tqdm(desc=index_name, total=total_docs)
        yield b"[\n"
        has_doc = False
        scroll = scan(elastic, query={
            "query": {
                "match_all": {}
            },
        }, scroll=scroll_time, size=batch_size, index=index_name, request_timeout=request_timeout)
        for doc in scroll:
            if has_doc:
                yield b",\n"
            yield dumps(doc).encode("utf-8")
            bar.update()
            has_doc = True
        yield b"\n]"
        bar.close()

    info("Backing up index {}".format(index_name))
    mapping: Dict[str, Any] = elastic.indices.get_mapping(index=index_name)
    fine_mapping: Dict[str, Any] = mapping[index_name]["mappings"]
    settings = elastic.indices.get_settings(index=index_name)
    fine_settings: Dict[str, Any] = settings[index_name]["settings"]
    backup_file = join(backup_path, "{}-backup.zip".format(index_name))
    backup_tmp_file = backup_file + ".tmp"
    zs = ZipStream(compress_type=ZIP_BZIP2, compress_level=compression_level)
    with open(backup_tmp_file, mode="wb") as f:
        zs.add(dumps(fine_mapping, indent=2), "mapping.json")
        zs.add(dumps(fine_settings, indent=2), "settings.json")
        zs.add(es_docs_generator(curr_state.docs_num), "docs.json")
        f.writelines(zs)

    move(backup_tmp_file, backup_file)
    state[index_name] = curr_state
    IndexMetadata.save_metadata(state, meta_path)


def process_backup(
    elastic: Elasticsearch,
    prev_state: Dict[str, IndexMetadata],
    curr_state: Dict[str, IndexMetadata],
    backup_path: str,
    meta_path: str,
    batch_size: int,
    scroll_time: str,
    request_timeout: int,
    compression_level: int,
) -> None:
    merged_state = dict(prev_state)
    for index_name, state in curr_state.items():
        index_exists = index_name in prev_state
        if index_exists:
            prev_index_state = prev_state[index_name]
            if prev_index_state != state:
                backup(elastic, index_name, backup_path, meta_path, merged_state, state,
                       batch_size, scroll_time, request_timeout)
            else:
                info("Index {} doesn't seem to be changed, skip".format(index_name))
        else:
            backup(elastic, index_name, backup_path, meta_path, merged_state, state,
                   batch_size, scroll_time, request_timeout, compression_level)


def iterable_to_stream(iterable, buffer_size=8 * 1024 * 1024):
    """
    Lets you use an iterable (e.g. a generator) that yields byte strings as a read-only
    input stream.

    The stream implements Python 3's newer I/O API (available in Python 2's io module).
    For efficiency, the stream is buffered.
    """

    class IterStream(RawIOBase):
        def __init__(self):
            self.leftover = None

        # noinspection PyMethodMayBeStatic
        def readable(self):
            return True

        def readinto(self, b):
            try:
                length = len(b)  # We're supposed to return at most this much
                chunk = self.leftover or next(iterable)
                output, self.leftover = chunk[:length], chunk[length:]
                b[:len(output)] = output
                return len(output)
            except StopIteration:
                return 0  # indicate EOF

    return BufferedReader(IterStream(), buffer_size=buffer_size)


def restore(
    es: Elasticsearch,
    batch_size: int,
    threads: int,
    timeout: int,
    index_path: str,
    settings: Dict[str, Any],
    mapping: Dict[str, Any],
) -> None:
    def archive_generator():
        with open(index_path, mode="rb") as f:
            while True:
                data = f.read(8 * 1024 * 1024)
                if not data:
                    break
                yield data

    def docs_generator():
        for file_name, file_size, unzipped_chunks in stream_unzip(archive_generator()):
            if file_name in {b"settings.json", b"mapping.json"}:
                # iterate through generator to skip
                deque(unzipped_chunks, maxlen=0)
                continue
            if file_name == b"docs.json":
                for chunk in unzipped_chunks:
                    yield chunk
            else:
                warning(f"Unknown file observed: {file_name}, ignore")
                deque(unzipped_chunks, maxlen=0)

    def es_docs_generator():
        for doc in stream_ijson(iterable_to_stream(docs_generator(), buffer_size=8 * 1024 * 1024), "item"):
            doc.pop("_id", "")
            doc.pop("sort", "")
            doc.pop("_score", "")
            doc["_index"] = doc["_index"]

            yield doc

    info("Counting docs...")
    name = settings["index"]["provided_name"]
    bar = tqdm(desc=name, total=0)
    try:
        for _ in stream_ijson(iterable_to_stream(docs_generator(), buffer_size=8 * 1024 * 1024), "item"):
            bar.update()
    finally:
        bar.close()
    total = bar.n
    info(f"Total docs: {total}")
    index_settings = settings["index"]
    index_settings.pop("creation_date", None)
    index_settings.pop("uuid", None)
    index_settings.pop("version", None)
    index_settings.pop("provided_name", None)
    es.indices.create(index=name, body={
        "settings": settings,
        "mappings": mapping
    })
    bar = tqdm(desc=name, total=total)
    try:
        for success, err_info in parallel_bulk(
            client=es,
            thread_count=threads,
            chunk_size=batch_size,
            actions=es_docs_generator()
        ):
            bar.update()
            if not success:
                print('A document failed:', err_info)
    finally:
        bar.close()
    info(f"Flush & refresh")
    es.indices.refresh(index=name, request_timeout=timeout)
    es.indices.flush(index=name, request_timeout=timeout)
    info("Done")


def process_restore(
    es: Elasticsearch,
    batch_size: int,
    threads: int,
    timeout: int,
    indexes: List[str],
) -> None:
    info("Checking indexes...")
    validated: Dict[str, Tuple[Dict[str, Any], Dict[str, Any]]] = {}
    for index in indexes:
        # noinspection PyBroadException
        try:
            info(f"Checking index {index}...")
            with ZipFile(index, mode="r") as archive:
                mapping = loads(archive.read("mapping.json").decode("utf-8"))
                settings = loads(archive.read("settings.json").decode("utf-8"))
                name = settings["index"]["provided_name"]
                info(f"Provided name: {name}")
                validated[index] = (mapping, settings)
        except Exception:
            exception(f"Can't verify index dump {index}")

    for index, (mapping, settings) in validated.items():
        # noinspection PyBroadException
        try:
            restore(es, batch_size, threads, timeout, index, settings, mapping)
        except Exception:
            exception(f"Can't process index {index}")


def main() -> None:
    console = default_handler()
    getLogger('').addHandler(console)
    getLogger('').setLevel(INFO)
    getLogger().addHandler(console)
    getLogger().setLevel(INFO)

    parser = ArgumentParser(
        prog="tresbackup",
        description="Makes a backup/restore of all (or specified) indices"
    )

    subparsers = parser.add_subparsers(help="sub-command help", dest="command")

    parser_backup = subparsers.add_parser("backup", help="backup help")
    parser_backup.add_argument(
        "-e", "--es-url", type=str,
        required=True,
        metavar="es_url", dest="es_url",
        help="Elasticsearch url with url-encoded credentials (if required)"
    )
    parser_backup.add_argument(
        "--insecure", action="store_true",
        required=False, default=False, dest="insecure",
        help="Disables HTTPS certificate verification"
    )
    parser_backup.add_argument(
        "-b", "--batch-size", type=int,
        required=False, default=1000,
        metavar="batch_size", dest="batch_size",
        help="Elasticsearch batch size (size) parameter to fetch documents"
    )
    parser_backup.add_argument(
        "-c", "--compression-level", type=int,
        required=False, default=9, choices=range(1, 10),
        metavar="compression_level", dest="compression_level",
        help="Compression level"
    )
    parser_backup.add_argument(
        "-s", "--scroll-time", type=str,
        required=False, default="60m",
        metavar="scroll_time", dest="scroll_time",
        help="Elasticsearch scroll time parameter to fetch documents"
    )
    parser_backup.add_argument(
        "-t", "--timeout", type=int,
        required=False, default=60,
        metavar="request_timeout", dest="request_timeout",
        help="Elasticsearch request timeout in seconds"
    )
    parser_backup.add_argument(
        "-i", "--index", type=str,
        required=False,
        nargs="*", action="append",
        metavar="indexes", dest="indexes",
        help="Index(es) to backup. If not specified, all indexes are backed up. ES regexes are supported"
    )
    parser_backup.add_argument(
        "-x", "--exclude", type=str,
        required=False, default="\\..*",
        metavar="exclude", dest="exclude",
        help="Regular expression to exclude indexes. By default skips all indexes start with '.'"
    )
    parser_backup.add_argument(
        "-m", "--meta-file", type=str,
        required=False, default="es-dump-metadata.json",
        metavar="meta_file", dest="meta_file",
        help="Path to metadata file to track indexes changes"
    )
    parser_backup.add_argument(
        "-f", "--force", type=bool,
        required=False, default=False,
        metavar="force", dest="force",
        help="Ignores exising metadata file and creates backup of all specified indexes"
    )
    parser_backup.add_argument(
        "-o", "--output-path", type=str,
        required=False, default=".",
        metavar="output_path", dest="output_path",
        help="Path where backup archives will be stored"
    )

    parser_restore = subparsers.add_parser("restore", help="restore help")
    parser_restore.add_argument(
        "-e", "--es-url", type=str,
        required=True,
        metavar="es_url", dest="es_url",
        help="Elasticsearch url with url-encoded credentials (if required)"
    )
    parser_restore.add_argument(
        "--insecure", action="store_true",
        required=False, default=False, dest="insecure",
        help="Disables HTTPS certificate verification"
    )
    parser_restore.add_argument(
        "-b", "--batch-size", type=int,
        required=False, default=1000,
        metavar="batch_size", dest="batch_size",
        help="Elasticsearch batch size (size) parameter to index documents"
    )
    parser_restore.add_argument(
        "-p", "--parallel-threads", type=int,
        required=False, default=16,
        metavar="threads", dest="threads",
        help="Parallel threads to index data"
    )
    parser_restore.add_argument(
        "-t", "--timeout", type=int,
        required=False, default=300,
        metavar="request_timeout", dest="request_timeout",
        help="Elasticsearch request timeout in seconds"
    )
    parser_restore.add_argument(
        "-i", "--index", type=str,
        required=True,
        nargs="*", action="append",
        metavar="indexes", dest="indexes",
        help="Paths to index(es) ZIPs to restore. If not specified, all indexes in current directory are restored."
    )
    args = parser.parse_args()
    command: str = args.command
    if command == "backup":
        es_url: str = args.es_url
        insecure: bool = args.insecure
        exclude: Pattern = regexp_compile(args.exclude)
        meta_file: str = args.meta_file
        output_path: str = args.output_path
        timeout: int = args.request_timeout
        compression_level: int = args.compression_level
        es: Elasticsearch = Elasticsearch(es_url, verify_certs=not insecure)
        es.cluster.health(request_timeout=timeout)
        indexes = [j for i in args.indexes or [] for j in i] or ["*"]
        current_state = list_indexes(es, indexes, exclude, timeout)
        prev_state = {} if args.force else IndexMetadata.load_metadata(meta_file)
        process_backup(es, prev_state, current_state, output_path, meta_file,
                       args.batch_size, args.scroll_time, timeout, compression_level)
    elif command == "restore":
        es_url: str = args.es_url
        insecure: bool = args.insecure
        batch_size: int = args.batch_size
        threads: int = args.threads
        timeout: int = args.request_timeout
        indexes = [j for i in args.indexes or [] for j in i] or ["*"]
        es: Elasticsearch = Elasticsearch(es_url, verify_certs=not insecure)
        es.cluster.health(request_timeout=timeout)
        process_restore(es, batch_size, threads, timeout, indexes)
    else:
        raise ValueError(f"Unknown command: {command}")


if __name__ == '__main__':
    main()
