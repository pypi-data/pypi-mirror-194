from dataclasses import dataclass
from multiprocessing.pool import ThreadPool
from os import cpu_count

import requests


@dataclass
class Fetcher:
    urls: list[str]  # List of urls to be downloaded

    def _start_thread_pool(self):
        cpus = cpu_count()
        self._thread_pool = ThreadPool(cpus - 1).imap_unordered(
            self.fetch_url, self.urls
        )

    def get_all(self):
        self._start_thread_pool()
        for result in self._thread_pool:
            yield result

    def fetch_url(self, url):
        return requests.get(url)
