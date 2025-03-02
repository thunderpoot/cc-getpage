![Masthead Image](mast.png)

# cc-getpage

`cc-getpage` is a lightweight Python utility for retrieving individual pages from the [Common Crawl](https://commoncrawl.org) archive. It provides a simple way to fetch specific web pages using Common Crawl's index and downloads the corresponding WARC file segment.

For **bulk downloads** or **entire snapshots**, please use the official [`cc-downloader`](https://github.com/commoncrawl/cc-downloader) program.


## Features

- Fetches specific web pages from Common Crawl archives
- Lists available crawl snapshots for selection
- Supports manual or automatic crawl selection
- Displays archived versions of a URL for selection
- Downloads only the necessary WARC segment
- Includes automatic retries with backoff


## Usage

```sh
python cc-getpage.py <URL> [CRAWL-ID]
```


## **Contribute**
Pull requests are welcome. Feel free to improve features or fix bugs.


## License
This project is licensed under the **MIT Licence**.


## Contact
For support or questions, visit [Common Crawl](https://commoncrawl.org/contact-us) or open an issue on GitHub. You're also welcome to join our [Discord server](https://discord.gg/njaVFh7avF) or [Google Group](https://groups.google.com/g/common-crawl).
