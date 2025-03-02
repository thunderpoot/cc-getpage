#!/usr/bin/env python

import requests
import json
import sys
import dontpanic
import time
from requests.exceptions import RequestException, ConnectionError

INDEX_SERVER = "https://index.commoncrawl.org"
CC_INDEX_URL = f"{INDEX_SERVER}/collinfo.json"

dontpanic.set_message("\nExiting...")

HEADERS = {
    "User-Agent": "cc-getpage/1.0"
}


def fetch_crawl_ids():
    try:
        response = requests.get(CC_INDEX_URL, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching crawl IDs: {e}")
        return []


def select_crawl_id(crawl_ids, per_page=10):
    total_crawls = len(crawl_ids)
    current_page = 0

    while True:
        start = current_page * per_page
        end = min(start + per_page, total_crawls)
        print("\nAvailable Crawl IDs:")
        print("{:<4} {:<20} {}".format("#", "Crawl ID", "Name"))
        print("-" * 60)

        for i, crawl in enumerate(crawl_ids[start:end], start=start + 1):
            print("{:<4} {:<20} {}".format(i, crawl["id"], crawl["name"]))

        print("\n(n) Next Page | (p) Previous Page | (q) Quit")
        choice = input("\nSelect a crawl ID (enter number) or navigate pages: ").strip()

        if choice.lower() == "n":
            if end < total_crawls:
                current_page += 1
            else:
                print("Already on the last page.")
        elif choice.lower() == "p":
            if current_page > 0:
                current_page -= 1
            else:
                print("Already on the first page.")
        elif choice.lower() == "q":
            print("Exiting crawl selection.")
            return None
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < total_crawls:
                    return crawl_ids[index]["id"]
            except ValueError:
                pass
            print("Invalid selection.")


def search_commoncrawl(url, crawl_id, max_retries=3):
    query_url = f"{INDEX_SERVER}/{crawl_id}-index?url={url}&output=json"
    print(f"\nSearching index for {url} in crawl {crawl_id}...")

    for attempt in range(max_retries):
        try:
            response = requests.get(query_url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            records = [json.loads(line) for line in response.text.strip().split("\n") if line]

            if not records:
                print("No results found in the index.")
                return None

            print(f"\nFound {len(records)} results:\n")
            print("{:<4} {:<15} {:<8} {}".format("#", "Timestamp", "Size", "WARC File"))
            print("-" * 80)

            for i, record in enumerate(records, start=1):
                print("{:<4} {:<15} {:<8} {}".format(
                    i,
                    record["timestamp"],
                    record["length"],
                    record["filename"].split("/")[-1]
                ))

            return records

        except (RequestException, ConnectionError) as e:
            print(f"Error fetching index (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("Failed after multiple attempts.")
                return None


def select_record(records):
    while True:
        choice = input("\nSelect an entry to download (enter number): ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(records):
                return records[index]
        except ValueError:
            pass
        print("Invalid selection. Try again.")


def download_from_commoncrawl(record, output_file="page.warc.gz"):
    warc_url = f"https://data.commoncrawl.org/{record['filename']}"
    offset = int(record["offset"])
    length = int(record["length"])

    headers = {
        "Range": f"bytes={offset}-{offset + length - 1}",
        **HEADERS
    }

    print(f"\nDownloading {length} bytes from {warc_url}...")

    try:
        response = requests.get(warc_url, headers=headers, stream=True, timeout=20)
        response.raise_for_status()

        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Saved to {output_file}")
    except requests.RequestException as e:
        print(f"Failed to download: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python cc-getpage.py <URL> [Crawl_ID]")
        sys.exit(1)

    url = sys.argv[1]
    crawl_id = sys.argv[2] if len(sys.argv) > 2 else None

    if not crawl_id:
        crawl_ids = fetch_crawl_ids()
        if not crawl_ids:
            sys.exit(1)
        crawl_id = select_crawl_id(crawl_ids)
        if not crawl_id:
            sys.exit(1)

    records = search_commoncrawl(url, crawl_id)
    if records:
        record = select_record(records)
        if record:
            download_from_commoncrawl(record)


if __name__ == "__main__":
    main()
