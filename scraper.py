import re
from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup
from tokenizer import tokenize
# import robots as r


# DEBUG ON!
debug = False

# robot_checker = r.Robot_Reader()

threshold = 10 # threshold for repeated urls

# use if we want a dictionary approach
parsed_urls = {} 

#key - url, value - content scraped from page
scraped_content = {} 

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

def passed_threshold(url):
    """
    Checks whether we have accessed this page (or a similar page) beyond the thresold

    @param url: url that is about to be parsed.
    @return: Returns True if we've passed the threshold of parsing this specific url.
    """
    return (url in parsed_urls) and (parsed_urls[url] == threshold)

def scraper(url, resp):
    links = extract_next_links(url, resp)  #links is a list
    valid_links = [link for link in links if is_valid(link)]
    if debug:
        print(f"Adding to frontier: {valid_links}")
    return valid_links
     

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

    #beautiful soup takes over from here and returns html content
    soup = extraction(url, resp)

    #this part can lowk go in the beautifulsoup.py file so the 'soup'is not being transferred between files
    #then maybe just return extracted_links, scraped_content directly when calling extraction() function
    content_size = len(resp.raw_response.content)
    if content_size > 200000:
        print(f"Content over 200,000 bytes (200KB): {content_size}")

    #extraction of links from 'url'
    extracted_links = []
    extracted_links = extract_links(soup, url)
    

    #extraction of text content from 'url'
    #note - UNIQUE URL CHECKING ISSUE
    content = extract_text_content(soup)
    # save content of webpage only if over 300 words (1 page) 
    if len(content) > 300:
        scraped_content[url] = content
    else:
        print(f"Low info web ({len(content)} tokens): {url}")
    #not sure how to go about tokenizing after this step
    #can also do tokeizing in extract_text_content function
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
        valid_hostname_pattern = r'.*(ics|cs|informatics|stat)\.uci\.edu$' #this one seems to work. needs to be tested with class server

        if not re.match(valid_hostname_pattern, parsed.hostname.strip()):
            if debug:
                print(f"BAD LINK (domain): {parsed.hostname}")
            return False
        
        if already_parsed(url):
            if debug:
                print(f"BAD LINK (discovered): {url}")
            return False
        
        if passed_threshold(url):
            if debug:
                print(f"BAD LINK (threshold): {url}")
            return False

        # if not robot_checker.check(url):
        #    print(f"BAD LINK (threshold): {url}")
        #    return False
        
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

def extraction(url, resp):
    #time.sleep(0.5)  # Politeness delay of 0.5 seconds
    content = resp.raw_response.content #would like to see what this looks like maybe?
    try:
        soup = BeautifulSoup(content, 'html5lib')
    except Exception:
        try:
            soup = BeautifulSoup(content, 'lxml-xml')
        except Exception:
            print("soup error")
    #if there is a soup error, it terminates?
    
    if url not in parsed_urls:
        parsed_urls[url] = 1
    else:
        parsed_urls[url] += 1

    return soup

def extract_links(soup, base_url):
    extracted_links = []
    canonical_link = None

    # Check for canonical link
    canonical_tag = soup.find('link', rel='canonical')
    if canonical_tag and canonical_tag.get('href'):
        canonical_link = canonical_tag.get('href')
        if not bool(urlparse(canonical_link).netloc):  # Check if the href is a relative URL
            canonical_link = urljoin(base_url, canonical_link)
        canonical_link, _ = urldefrag(canonical_link)
    
    if canonical_link and same_url(canonical_link, base_url):
        if debug:
            print(f"Returning canonical link only: {canonical_link}")
        return [canonical_link] #add if statement if canonical is equal to the link

    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href:
            if not bool(urlparse(href).netloc): 
                href = urljoin(base_url, href)
            href, _ = urldefrag(href)
            # Check for nofollow or noindex
            if 'nofollow' in link.get('rel', []) or 'noindex' in link.get('rel', []):
                continue
            if href not in extracted_links:
                extracted_links.append(href)
    return extracted_links

def extract_text_content(soup):
    """
    Extract string from soup and transform into a list of tokens.
    @params: Soupified content of webpage
    @return: list of tokens
    """
    tokens = []
    for element in soup.find_all(string=True):
        if element.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            text = element.strip()
            if text:
                text_content.append(text)
    tokens = []
    for text in text_content:
        tokens.extend(tokenize(text))
    return tokens                        #list of token for simhash