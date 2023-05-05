import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langchain.document_loaders import WebBaseLoader


class WebPageLinkExtractor:
    def __init__(self, base_url, timeout=10, max_depth=3):
        self.base_url = base_url
        self.timeout = timeout
        self.visited_urls = set()
        parsed_url = urlparse(base_url)
        self.domain_name = parsed_url.netloc
        self.max_depth = max_depth
        self.current_max_depth = 0

    def _fetch_page(self, url):
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f'Error fetching page: {url} - {e}')
            return None

    def _extract_links_recursive(self, url, depth=0, links=None):
        if depth > self.max_depth or url in self.visited_urls:
            return

        self.visited_urls.add(url)
        print(f'Fetching links from {url} at depth {depth}')
        self.current_max_depth = max(self.current_max_depth, depth)

        page_content = self._fetch_page(url)
        if not page_content:
            return

        soup = BeautifulSoup(page_content, 'html.parser')
        page_links = [a['href'] for a in soup.find_all('a', href=True)]

        for link in page_links:
            full_url = urljoin(url, link)
            parsed_full_url = urlparse(full_url)
            # Ignore URL fragments
            full_url = parsed_full_url._replace(fragment='').geturl()
            if parsed_full_url.netloc == self.domain_name:
                if links is not None:
                    links.append(full_url)
                self._extract_links_recursive(full_url, depth + 1, links=links)

    def get_links(self):
        links = []
        self._extract_links_recursive(self.base_url, links=links)
        return list(set(links))


class WebPageDownloader:
    def __init__(self, links, output_dir=None):
        self.links = links
        self.output_dir = output_dir or 'downloaded_pages'
        os.makedirs(self.output_dir, exist_ok=True)

    def _save_page(self, url, content):
        filename = urlparse(url).path.split('/')[-1] or 'index.html'
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def download_pages(self):
        for url in self.links:
            response = requests.get(url)
            if response.status_code == 200:
                print(f'Downloading page: {url}')
                self._save_page(url, response.text)
            else:
                print(f'Error downloading page: {url} - HTTP status code: {response.status_code}')


if __name__ == '__main__':
    base_url = 'https://python.langchain.com/en/latest/'
    extractor = WebPageLinkExtractor(base_url, max_depth=1000)
    links = extractor.get_links()
    print(f'\nMaximum depth reached: {extractor.current_max_depth}')
    print(f'Total links found: {len(links)}\n')

    downloader = WebPageDownloader(links)
    downloader.download_pages()
    print('\nAll pages downloaded.')

    html_links = [link for link in links if link.endswith('.html')]
    # Print filtered HTML links
    print(len(html_links))

    loader = WebBaseLoader(html_links[1:10])
    loader.requests_per_second = 10
    docs = loader.aload()

    print(len(docs))
    print(docs[0].page_content)
    print(docs[0])
    print(docs[0].metadata)
    print(docs[0].metadata.get("source"))