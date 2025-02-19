import re
from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup
import tokenizer
import duplication
import answers as a


# DEBUG - printing
debug = False
debug_v = False # even more prints, v for verbose

#key - url, value - content scraped from page
# scraped_content = {} 

# exact duplication checking: checksum
checksums = set()
# # near duplication checking: simhash
# simhashes = set()


def already_parsed(url):
    """
    Checks whether we have already parsed this url or not.

    @param url: url that is about to be parsed.
    @return: Returns True if url is in the dictionary
    """
    return urldefrag(url)[0] in a.pages
    
    ### use this code if we want a .txt approach ###
    # with open("parsed_urls.txt") as file:
        #contents = file.read()
        #return url in contents


def crawler_trap(url):
    """
    Detects if a URL is a crawler trap.
    
    @param url: URL to be checked.
    @return: Returns True if the URL is a crawler trap, otherwise False.
    """

    calendar_patterns = [
        r'calendar', r'icalendar', r'event', r'month', r'year', r'day', r'pdf'
    ]
    query_patterns = [
        r'ical', r'date'
    ]
    
    parsed_url = urlparse(url)
    
    for pattern in calendar_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            if debug:
                print(f"Detected crawler trap (calendar related): {url}")
            return True
    
    if parsed_url.query:
        for pattern in query_patterns:
            if re.search(pattern, parsed_url.query, re.IGNORECASE):
                if debug:
                    print(f"Detected crawler trap (query related): {url}")
                return True
    
    return False


def scraper(url, resp):
    links = extract_next_links(url, resp)  # links is a list
    valid_links = [link for link in links if is_valid(link)]
    if debug_v:
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

    # STATUS CODE CHECKING
    # 4xx client side error -> no links scrapped
    if (resp.status // 100 == 4) or (resp.status // 100 == 6):
        return list()
    # 3xx redirect: check redirect url, parse redirect url
    elif resp.status // 100 == 3:
        return get_redirect(url, resp)

    
    # UPPER BOUND CHECKING
    # Do not scrape web content over 250KB
    content_size = len(resp.raw_response.content)
    if content_size > 250000:
        print(f"Content over 250,000 bytes (250KB): {content_size}")
        return list()

    
    # GET CONTENT (TOKENS)
    # beautiful soup takes over from here and returns html content
    soup = extraction(url, resp)
    # not soupable
    if not soup:
        return list()

    #extraction of links from 'url'
    extracted_links = []
    extracted_links = extract_links(soup, url)  
    
    #extraction of text content from 'url'
    #note - UNIQUE URL CHECKING ISSUE
    content, num_words= extract_text_content(soup)

    
    # DUPLICATION CHECKING
    # checksum
    checksum_val = duplication.checksum(content)
    # exact duplicate found
    if checksum_val in checksums:
        return list()
    else:
        checksums.add(checksum_val)
    # # simhash
    # simhash_val = duplication.simhash(tokenizer.current_word_frequencies(content))
    # # check if any previous simhash and current simhash are too similar
    # near_dup = False
    # for sim in simhashes:
    #     # threshold for near duplication is 0.85
    #     if duplication.similarity_score(sim, simhash_val) >= 0.85:
    #         near_dup = True
    #         break
    # if near_dup:
    #     return list()
    # else:
    #     simhashes.add(simhash_val)

    
    # LOWER BOUND CHECKING
    # save content of webpage only if over 50
    if len(content) > 50:
        # scraped_content[url] = content
        a.add_page(url)
        a.add_to_ics_domains(url)
    else:
        print(f"Low info web ({len(content)} tokens): {url}")
        return list()

    
    # UPDATE ANSWERS
    if num_words > a.max_words:
        a.update_max_URL(url, num_words)
    tokenizer.update_tokens_dict(content)
    
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
        valid_hostname_pattern = r'.*(ics|cs|informatics|stat)\.uci\.edu$' 
        #this one seems to work. needs to be tested with class server

        if not re.match(valid_hostname_pattern, parsed.hostname.strip()):
            if debug:
                print(f"BAD LINK (domain): {parsed.hostname}")
            return False
        
        if already_parsed(url):
            if debug:
                print(f"BAD LINK (discovered): {url}")
            return False
        
        if crawler_trap(url):
            if debug:
                print(f"BAD LINK (trap): {url}")
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
    content = resp.raw_response.content # would like to see what this looks like maybe?
    if debug_v:
        print(content)
    try:
        soup = BeautifulSoup(content, 'html5lib')
    except Exception:
        try:
            soup = BeautifulSoup(content, 'lxml-xml')
        except Exception:
            print("soup error")
            return None
    #if there is a soup error, it terminates?
    
    # if url not in parsed_urls:
    #     parsed_urls[url] = 1
    # else:
    #     parsed_urls[url] += 1

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
    
    if canonical_link and not same_url(canonical_link, base_url):
        #if debug:
            #print(f"Returning canonical link only: {canonical_link}")
        return [canonical_link]

    # not canonical -> get all other links
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
    @return: list of tokens and the length of text
    """
    tokens = []
    length_of_text = 0
    for element in soup.find_all(string=True):
        if element.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            text = element.strip()
            if text:
                word_count = len(text.split())
                length_of_text += word_count
                tokens.extend(tokenizer.current_tokens(text))
    if debug_v:
        print(f"Tokens: {tokens}")

    return tokens, length_of_text

def same_url(url1:str, url2:str):
    """
    Check if two URLs are essentially the same.
    @params: URL1 and URL2 for comparison
    @return: True if URL1 = URL2 else False
    """
    parsed1 = urlparse(url1)
    if parsed1.path == '/':
        parsed1 = parsed1._replace(path='')
    parsed2 = urlparse(url2)
    if parsed2.path == '/':
        parsed2 = parsed2._replace(path='')

    return (parsed1.scheme == parsed2.scheme and parsed1.netloc == parsed2.netloc
            and parsed1.path == parsed2.path and parsed1.query == parsed2.query)
