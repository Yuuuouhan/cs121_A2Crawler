import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import time

threshold = 10 # threshold for repeated urls

# use if we want a dictionary approach
parsed_urls = {} 

def already_parsed(url):
    """
    Checks whether we have already parsed this url or not.

    @param url: url that is about to be parsed.
    @return: Returns True if url is in the dictionary
    """
    return url in parsed_urls
    
    ### use this code if we want a .txt approach ###
    # with open("parsed_urls.txt") as file:
        #contents = file.read()
        #return url in contents

def remove_fragment(url):
    """
    Removes the fragment of an URL. If URL has no fragment, return the original URL.

    @param: url that is to be defragmented.
    @returnL returns the URL without fragment.
    """
    return urlparse.urldefrag(url)[0]

def passed_threshold(url):
    """
    Checks whether we have accessed this page (or a similar page) beyond the thresold

    @param url: url that is about to be parsed.
    @return: Returns True if we've passed the threshold of parsing this specific url.
    """
    return parsed_urls[url] == threshold

def scraper(url, resp):
    links = extract_next_links(url, resp)  #links is a list
    return [link for link in links if is_valid(link)]

def get_redirect(url, resp):
    """
    Find redircted link(s).
    @param: url, response
    @return: list of link(s) redirected to
    """
    status = str(resp.status)
    return list()

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    # Thought process?:
    # need try/except statements for status codes (resp.status)
    # add resp.url to parse_urls if not already there, else, update the num of times we've parsed this
    # if a page is a duplicate/near duplicate, update the num of times we've parsed the similar url
    # scrape the urls in that page, return list
    # except if status code is 300: do not go to redirected page?
    # except if status code is 400: continue

    # status code checking
    # 4xx client side error -> no links scrapped
    if str(resp.status).startswith("4"):
        return None
    # 3xx redirect: check redirect url, parse redirect url
    else if str(resp.status).startswith("3"):
        return get_redirect(url, resp)

    return list()

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
            
        valid_hostname_pattern = r'.*\.(ics|cs|informatics|stat)\.uci\.edu$'

        if not re.match(valid_hostname_pattern, parsed.hostname) or already_parsed(url) or passed_threshold(url):
            return False
        
        # claiming this code is unreachable
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
