import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urldefrag

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
    return urldefrag(url)[0]

def passed_threshold(url):
    """
    Checks whether we have accessed this page (or a similar page) beyond the thresold

    @param url: url that is about to be parsed.
    @return: Returns True if we've passed the threshold of parsing this specific url.
    """
    return (url in parsed_urls) and (parsed_urls[url] == threshold)

def scraper(url, resp):
    links = extract_next_links(url, resp)  #links is a list
    return [link for link in links if is_valid(link)]
     

def get_redirect(url, resp):
    """
    Find redircted link(s).
    @param: url, response
    @return: list of link(s) redirected to
    Notes:
    304 - not modified: returned when request sent with 
        conditional "Has website updated sice xyz?" and answer is no
    305 - use proxy: decapricated due to security concerns
    306 - not used
    PROBLEM: how do I access HTTP headers???
    """
    print("WE HAVE A CODE 3XX!!!")
    print(resp.error)

    # integer
    status = resp.status
    # multiple choices 
    if status == 300:
        # implementation specific: can check HTTP header Alternative or html
        pass
    # moved perm, moved temp (AKA found), see other (primarily from POST), temp redirect, perm redirect
    elif status in (301, 302, 303, 308, 309):
        # Location header in HTTP for redirection link
        pass
    
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
    if (resp.status // 100 == 4) or (resp.status // 100 == 6):
        return list()
    # 3xx redirect: check redirect url, parse redirect url
    elif resp.status // 100 == 3:
        return get_redirect(url, resp)

    content = resp.raw_response.content
    soup = BeautifulSoup(content, 'html5lib')

    if url not in parsed_urls:
        parsed_urls[url] = 1
    else:
        parsed_urls[url] += 1

    #only extracting link as of now
    extracted_links = []
    for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                if not bool(urlparse(href).netloc):
                    base_url = resp.url
                    href = urljoin(base_url, href)
                href = remove_fragment(href)
                if href not in extracted_links:
                    extracted_links.append(href)
    return extracted_links

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        # original: r'.*\.(ics|cs|informatics|stat)\.uci\.edu$'
        valid_hostname_pattern = r'.*\.(ics|cs|informatics|stat)\.uci\.edu$'

        if not re.match(valid_hostname_pattern, parsed.hostname.strip()):
            print(f"BAD LINK (domain): {parsed.hostname}")
            return False
        
        if already_parsed(url):
            print(f"BAD LINK (discovered): {url}")
            return False
        
        if passed_threshold(url):
            print(f"BAD LINK (threshold): {url}")
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
