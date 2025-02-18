import urllib.robotparser as r
from urllib.parse import urlparse, urljoin
from utils.download import download

class Robot_Reader(r.RobotFileParser):
	def __init__(self, url, config):
		self.url = urlparse(url)
		self.config = config
		self.base_url = f"{self.url.scheme}://{self.url.hostname}"
		self.robot_url = f"{self.base_url}/robots.txt"
	
	def read(self):
		"""
		Uses the cache server to download the robots.txt file.

		@return: a response object of the content of the website.
		"""
		return download(self.robot_url, self.config)
	
	def add_disallowed_pages(self, url: str, content: str) -> list:
		"""
		Returns a list of disallowed sites that the current website cannot go through.

		@param url: robots.txt URL
		@param content: content of the robots.txt URL
		@return: a list of sites that the current URL is not allowed to go through
		"""
		disallowed_sites = []
		user_agent = None
		lines = content.splitlines()
		for line in lines:
			line = line.strip().lower()
			if line.startswith("user-agent:"):
				user_agent = line.split(":", 1)[1].strip()
			elif user_agent == "*" and line.startswith("disallow:"):
				path = line.split(":", 1)[1].strip()
				if path:
					full_url = urljoin(self.base_url, path)
					disallowed_sites.append(full_url)

		return disallowed_sites
	
