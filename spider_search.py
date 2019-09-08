import functools
import requests
import re
from agent import Agent
from proxy import Proxy
from urllib.parse import urlsplit, urlunsplit, urlparse


class SpiderSearch:

    def __init__(self, url, exclude=None):
        self.links = []
        self.found_links = []

        self.proxies = Proxy().generate()
        self.user_agent = Agent().generate()

        self.url = self.normalize(url)
        self.host = urlparse(self.url).netloc
        self.exclude = exclude
        self.visited_links = [self.url]

    def start(self):
        print(self.proxies)
        print(self.user_agent)

        self.crawl(self.url)

        return sorted(self.found_links)

    @functools.lru_cache()
    def crawl(self, url):
        print(f"Парсим {url} - в обработку: {len(self.links)} обработано: {len(self.found_links)}")

        s_request = self.send_request(url)

        page = str(s_request.content)

        found_links = re.findall("<a [^>]*href=['|\"](.*?)['\"].*?>", page)

        for link in found_links:
            is_url = self.is_url(link)

            if is_url:
                link = self.correct_link(link)
                if (link not in self.visited_links) and (link not in self.links):
                    is_internal = self.is_internal(link)
                    if is_internal:
                        self.add_url(link, self.links, self.exclude)

        for link in self.links:
            self.links.remove(link)
            if (link not in self.visited_links) and (link not in self.links):
                request = self.send_request(self.normalize(link))
                if request.status_code == 200:
                    self.visited_links.append(link)
                    self.add_url(request.url, self.found_links, self.exclude)
                    self.crawl(request.url)

    def send_request(self, url):
        return requests.get(url, headers=self.user_agent)

    def add_url(self, link, link_list, exclude_pattern=None):
        if link:
            if (link not in self.visited_links) and (link not in self.links):
                excluded = False
                if exclude_pattern:
                    excluded = re.search(exclude_pattern, link)

                if not excluded:
                    link_list.append(link)

    def correct_link(self, url):
        scheme, netloc, path, qs, anchor = urlsplit(url)
        return path

    def normalize(self, url):
        scheme, netloc, path, qs, anchor = urlsplit(url)
        if (scheme in ['http', 'https', '']) and (path not in ['\\', '/']):
            if netloc != '':
                return urlunsplit((scheme, netloc, path, qs, anchor))
            elif path != '':
                base_url = urlparse(self.url)
                return urlunsplit((base_url.scheme, base_url.netloc, path, qs, anchor))
            else:
                return False
        return False

    def is_internal(self, url):
        host = urlparse(url).netloc
        return host == self.host or host == ''

    def is_url(self, url):
        scheme, netloc, path, qs, anchor = urlsplit(url)

        if url not in ['', '#'] and (path not in ['\\', '/', '/index.php', '/index', '']) and (
                scheme in ['http', 'https', '']):
            return True
        else:
            return False
