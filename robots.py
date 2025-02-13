import urllib.robotparser as r

class Robot_Reader:
	def __init__(self):
		self.ics_url = r.RobotFileParser()
		self.cs_url = r.RobotFileParser()
		self.stats_url = r.RobotFileParser()
		self.informatics_url = r.RobotFileParser()

		self.ics_url.set_url("https://www.ics.uci.edu")
		self.cs_url.set_url("https://www.cs.uci.edu")
		self.stats_url.set_url("https://www.stats.uci.edu")
		self.informatics_url.set_url("https://www.informatics.uci.edu")

		self.ics_url.read()
		self.cs_url.read()
		self.stats_url.read()
		self.informatics_url.read()
	
	def check(self, url: str) -> bool:
		"""
		Checks through all of the robots.txt of the root sites and checks if the site
		can crawl there or not.
		
		@param url: url of the string waiting to be parsed.
		@return: boolean of whether it should be parsed or not.
		"""
		return self.ics_url.can_fetch(url) or self.cs_url.can_fetch(url) or self.stats_url.can_fetch(url) or self.informatics_url.can_fetch(url)