![Masthead Image](mast.png)

# cc-getpage

`cc-getpage` is a lightweight Python utility for retrieving individual pages from the [Common Crawl](https://commoncrawl.org) archive. It provides a simple way to fetch specific web pages using Common Crawl's index and downloads the corresponding WARC file segment.

For **bulk downloads** or **entire snapshots**, please use the official [`cc-downloader`](https://github.com/commoncrawl/cc-downloader) program.


## Features

- Fetches specific web pages from Common Crawl archives
- Automatically probes crawls to find which ones contain your URL
- Supports manual or automatic crawl selection
- Displays archived versions of a URL for selection
- Downloads only the necessary WARC segment
- Includes automatic retries with backoff
- `--viewpage` option to get a Common Crawl viewer URL instead of downloading


## Usage

```sh
python cc-getpage.py [--viewpage] <URL> [CRAWL-ID]
```

### Options

| Option | Description |
|---|---|
| `--viewpage` | Print a Common Crawl viewer URL instead of downloading the WARC segment |
| `--version` | Show the program version |

If `CRAWL-ID` is omitted, the program will probe all available crawls to find which ones contain the given URL. This is rate-limited to be polite to the index server, so it may take a while. Press `Ctrl+C` to stop early and work with whatever matches have been found so far.


## **Contribute**
Pull requests are welcome. Feel free to improve features or fix bugs.


## License
This project is licensed under the **MIT Licence**.


## Contact
For support or questions, visit [Common Crawl](https://commoncrawl.org/contact-us) or open an issue on GitHub. You're also welcome to join our [Discord server](https://discord.gg/njaVFh7avF) or [Google Group](https://groups.google.com/g/common-crawl).
