from threading import Thread

from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time
import crawler.robots as r
from urllib.parse import urlparse, urljoin


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.disallowed_pages = []
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
    
    def can_parse(self, tbd_url: str) -> bool:
        if self.disallowed_pages and any(site in tbd_url for site in self.disallowed_pages):
            return False
        robot = r.Robot_Reader(tbd_url, self.config)
        resp_url = robot.read()
        content = resp_url.raw_response.content.decode('utf-8')
        if (resp_url.status // 100 == 4) or not content or content.strip() == "":
            return True
        pages = robot.add_disallowed_pages(robot.base_url, content) or []
        self.disallowed_pages.extend(pages)
        if self.disallowed_pages and any(site in tbd_url for site in self.disallowed_pages):
            return False
        return True
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            # try:
            #     if not self.can_parse(tbd_url):
            #         continue
            # except Exception as e:
            #     print(f"EXCEPTION WITH ROBOT: {e}")
            #     pass
            
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            
            try: 
                scraped_urls = scraper.scraper(tbd_url, resp)
            except Exception as e:
                scraped_urls = list()
                print(f"WORKER EXCEPTION: {e}")

            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)

