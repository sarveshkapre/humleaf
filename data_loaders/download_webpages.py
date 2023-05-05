"""
Here's a quick description of the code:

This Python script is designed to perform a recursive download of web pages from a specified URL and its subpages. The script starts by downloading the main page and then recursively downloads all linked pages up to a specified maximum depth. The script uses the requests library to make HTTP requests and the BeautifulSoup library to parse HTML content. It also includes error handling to gracefully manage network errors, timeouts, and HTTP errors. Additionally, the script filters out external links and non-HTML content to focus on downloading relevant pages. The downloaded pages are saved to a specified output directory. The script provides progress updates by printing messages to the console, including the total number of pages downloaded at the end.

Key features of the script:

Recursive downloading of web pages and their subpages.
Error handling for network and HTTP errors.
Filtering of external links and non-HTML content.
Maximum depth limit to prevent infinite recursion.
Progress updates and status messages.

"""
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class WebPageDownloader:
    def __init__(self, base_url, output_dir=None, timeout=10, max_depth=3):
        self.base_url = base_url
        self.timeout = timeout
        self.visited_urls = set()
        parsed_url = urlparse(base_url)
        self.domain_name = parsed_url.netloc
        self.output_dir = output_dir or self.domain_name
        self.max_depth = max_depth
        os.makedirs(self.output_dir, exist_ok=True)

    def _download_page(self, url):
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f'Error downloading page: {url} - {e}')
            return None

    def _download_recursive(self, url, depth=0):
        if depth > self.max_depth or url in self.visited_urls:
            return
        self.visited_urls.add(url)

        filename = urlparse(url).path.split('/')[-1] or 'index.html'
        output_path = os.path.join(self.output_dir, filename)

        page_content = self._download_page(url)
        if not page_content:
            return

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(page_content)

        soup = BeautifulSoup(page_content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]

        for link in links:
            full_url = urljoin(url, link)
            if urlparse(full_url).netloc == self.domain_name and full_url.endswith('.html'):
                self._download_recursive(full_url, depth + 1)

    def download(self):
        print('Starting download...')
        self._download_recursive(self.base_url)
        total_downloaded = len(self.visited_urls)
        print(f'Download complete. Total pages downloaded: {total_downloaded}')

if __name__ == '__main__':
    base_url = 'https://python.langchain.com/en/latest/'
    downloader = WebPageDownloader(base_url, max_depth=5000)
    downloader.download()
