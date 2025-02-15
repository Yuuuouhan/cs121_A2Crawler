from urllib.parse import urlparse, urldefrag
import re
import tokenizer

pages = set()
subdomains = dict()
max_URL = ""
max_words = 0

def answers():
	num_unique_URLS = unique_URLS()
	longest_page = return_longest_page()
	common_words = tokenizer.compute_word_frequencies()
	subdomains = find_subdomains()
	
	with open("final_answers.txt", "w") as file:
		file.write(f"UNIQUE_URLS: {num_unique_URLS}\n")
		file.write(f"LONGEST_PAGE: {longest_page[0]}: {longest_page[1]}\n")
		file.write(f"COMMON WORDS: {common_words}\n")
		file.write(f"SUBDOMAINS: {subdomains}\n")

def add_page(url: str) -> None:
	"""
	Checks an incoming URL, removes the fragment, and adds ito the set of pages.
	
	@param url: incoming absolute URL path
	@return: None
	"""
	url = urldefrag(url)
	pages.add(url)

def add_to_ics_domains(url: str) -> None:
	"""
	Checks an incoming URL and sees if it is within the ics domain, and whether
	we should add it to the existing ics_domains set
	
	@param url: incoming absolute URL path
	@return: None
	"""
	domain = urlparse(url).netloc[-11:]
	url = urldefrag(url)
	if domain == "ics.uci.edu":
		parsed_url = urlparse(url).hostname
		if parsed_url not in subdomains:
			subdomains[parsed_url] = set(url)
		else:
			subdomains[parsed_url].add(url)

def unique_URLS() -> int:
	"""
	Returns the number of unique URLS in the ics domain.
	
	@return: integer representing the number of unique URLS in the ics domain.
	"""
	return len(pages)

def update_max_URL(url: str, length: int) -> None:
	"""
	Updates max_URL and max_words to find the longest page in terms of the number
	of words.
	
	@param url: incoming URL
	@param length: length of incoming URL
	@return: None
	"""
	max_URL = url
	max_words = length
	

def return_longest_page() -> int:
	"""
	Returns the longest page in terms of the number of words, excluding HTML markup.
	
	@return: integer representing the longest page in terms of the number of words.
	"""
	return max_URL, max_words

def find_subdomains() -> dict:
	"""
	Returns the subdomains of ics.uci.edu, as well as the number of unique pages
	belonging to each subdomain.
	
	@return: dictionary of each subdomain and its respective number of unique pages.
	"""
	return_dict = dict()
	for subdomain in subdomains:
		return_dict[subdomain] = len(subdomains[subdomain])
	return return_dict

