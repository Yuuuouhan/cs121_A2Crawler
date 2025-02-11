#file to store all functionality done by beautifulsoup

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin, urldefrag
import time
from scraper import parsed_urls

def extraction(url, resp):
    time.sleep(0.5)  # Politeness delay of 0.5 seconds
    content = resp.content #would like to see what this looks like maybe?
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
    
    if canonical_link:
        return [canonical_link]

    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href:
            if not bool(urlparse(href).netloc):  # Check if the href is a relative URL
                href = urljoin(base_url, href)
            href, _ = urldefrag(href)
            # Check for nofollow or noindex
            if 'nofollow' in link.get('rel', []) or 'noindex' in link.get('rel', []):
                continue
            if href not in extracted_links:
                extracted_links.append(href)
    return extracted_links

def extract_text_content(soup):
    text_content = []
    for a_tag in soup.find_all('a'): #change this
        text_content.append(a_tag.get_text())
    return text_content
