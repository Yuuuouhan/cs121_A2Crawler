import urllib.robotparser as r
from urllib.parse import urlparse, urljoin
# from utils.download import download

# in crawler.worker.py, use the following code:
class Robot_Reader(r.RobotFileParser):
	# def __init__(self, url, config):
	def __init__(self, url):
		super().__init__(url)
		# self.config = config
	
	# def read(self):
		"""
		Uses the cache server to download the robots.txt file.
		"""
		#new_url = f"{self.url}/robots.txt"
		#return download(new_url, self.config)
	
	def add_disallowed_pages(self, url: str, content: str) -> list:
		disallowed_sites = []
		user_agent = None
		lines = content.splitlines()
		parsed_url = urlparse(url)
		base_url = f"{parsed_url.scheme}://{parsed_url.hostname}"
		for line in lines:
			line = line.strip().lower()
			if line.startswith("user-agent:"):
				user_agent = line.split(":", 1)[1].strip()
			elif user_agent == "*" and line.startswith("disallow:"):
				path = line.split(":", 1)[1].strip()
				if path:
					full_url = urljoin(base_url, path)
					disallowed_sites.append(full_url)

		return disallowed_sites

if __name__ == "__main__":
	# take a url
	# if site in disallowed_pages, return false
	# else, take the root site, scrape content (get the content through download() -> resp.raw_response.content)
	# if error = 404 or b'', return false
	# take content, decode(utf-8)
	# read it into add_disallowed_pages()
	# redo step 2
	# stop
	disallowed_pages = []
	tbd_url = "https://vision.uci.edu/projects.html"

	def can_parse(tbd_url: str) -> bool:
		content = """"""

		if disallowed_pages and any(site in tbd_url for site in disallowed_pages):
			return False
		new_url = urlparse(tbd_url)
		new_url = urljoin(tbd_url, "/robots.txt")
		print(f"New URL: {new_url}")
		robot = Robot_Reader(new_url)
		# resp_url = robot.read()
		# content = resp_url.raw_response.content.decode('utf-8')
		# if (resp_url.status / 100 == 4) not content or content.strip() == "":
			# return False
		if not content or content.strip() == "": # DELETE THIS LATER... ^^ is the actual code for download.py
			return False
		pages = robot.add_disallowed_pages(new_url, content) or []
		disallowed_pages.extend(pages)
		print(f"Disallowed Pages: {disallowed_pages}")
		if any(site in tbd_url for site in disallowed_pages):
			return False
		return True
	
	print(can_parse(tbd_url))
	
