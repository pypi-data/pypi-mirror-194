# ES backup tool

CLI for easy ES backup and restore with simple tracking of non-modified indexes

```
usage: tresbackup [-h] {backup,restore} ...

Makes a backup/restore of all (or specified) indices

positional arguments:
  {backup,restore}  sub-command help
    backup          backup help
    restore         restore help

optional arguments:
  -h, --help        show this help message and exit


```

# Backup

```
usage: tresbackup backup [-h] -e es_url [--insecure] [-b batch_size] [-s scroll_time] [-t request_timeout] [-i [indexes ...]] [-x exclude] [-m meta_file] [-f force] [-o output_path]

optional arguments:
  -h, --help            show this help message and exit
  -e es_url, --es-url es_url
                        Elasticsearch url with url-encoded credentials (if required)
  --insecure            Disables HTTPS certificate verification
  -b batch_size, --batch-size batch_size
                        Elasticsearch batch size (size) parameter to fetch documents
  -s scroll_time, --scroll-time scroll_time
                        Elasticsearch scroll time parameter to fetch documents
  -t request_timeout, --timeout request_timeout
                        Elasticsearch request timeout in seconds
  -i [indexes ...], --index [indexes ...]
                        Index(es) to backup. If not specified, all indexes are backed up. ES regexes are supported
  -x exclude, --exclude exclude
                        Regular expression to exclude indexes. By default skips all indexes start with '.'
  -m meta_file, --meta-file meta_file
                        Path to metadata file to track indexes changes
  -f force, --force force
                        Ignores exising metadata file and creates backup of all specified indexes
  -o output_path, --output-path output_path
                        Path where backup archives will be stored

```

# Restore

```
usage: tresbackup restore [-h] -e es_url [--insecure] [-b batch_size] [-p threads] [-t request_timeout] -i [indexes ...]

optional arguments:
  -h, --help            show this help message and exit
  -e es_url, --es-url es_url
                        Elasticsearch url with url-encoded credentials (if required)
  --insecure            Disables HTTPS certificate verification
  -b batch_size, --batch-size batch_size
                        Elasticsearch batch size (size) parameter to index documents
  -p threads, --parallel-threads threads
                        Parallel threads to index data
  -t request_timeout, --timeout request_timeout
                        Elasticsearch request timeout in seconds
  -i [indexes ...], --index [indexes ...]
                        Paths to index(es) ZIPs to restore. If not specified, all indexes in current directory are restored.
```