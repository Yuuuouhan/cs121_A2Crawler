import re
from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup   
import requests

def tokenize(text):
    """
    Tokenizes the given text string.
    Parameters:
    text (str): The text string to be tokenized.
    Returns:
    list: A list of tokens (words) extracted from the text string.
    Time Complexity: O(n), where n is the number of characters in the text string.
    """
    tokens = []
    pattern = r'\b\w+\b'
    lowercase_text = text.lower()
    words = re.findall(pattern, lowercase_text)
    tokens.extend(words)
    return tokens


URL = "https://ics.uci.edu"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')
#print(soup.prettify())

extracted_links = []
canonical_link = None

# Check for canonical link
canonical_tag = soup.find('link', rel='canonical')
if canonical_tag and canonical_tag.get('href'):
    canonical_link = canonical_tag.get('href')
    if not bool(urlparse(canonical_link).netloc):  # Check if the href is a relative URL
        canonical_link = urljoin(URL, canonical_link)
    canonical_link, _ = urldefrag(canonical_link)

if canonical_link:
    print("Canonical link:", canonical_link)

for link in soup.find_all('a', href=True):
    href = link.get('href')
    if href:
        if not bool(urlparse(href).netloc): 
            href = urljoin(URL, href)
        href, _ = urldefrag(href)
        # Check for nofollow or noindex
        if 'nofollow' in link.get('rel', []) or 'noindex' in link.get('rel', []):
            continue
        if href not in extracted_links:
            extracted_links.append(href)
print("Extracted links:", extracted_links)

text_content = []
for element in soup.find_all(string=True):
    if element.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        text = element.strip()
        if text:
            text_content.append(text)
tokens = []
for text in text_content:
    tokens.extend(tokenize(text))
print("Tokens:", tokens)    

