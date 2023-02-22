import urllib
import re
import tldextract

def words_raw_extraction(domain, subdomain, path):
    w_domain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", domain.lower())
    w_subdomain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", subdomain.lower())   
    w_path = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", path.lower())
    raw_words = w_domain + w_path + w_subdomain
    w_host = w_domain + w_subdomain
    raw_words = list(filter(None,raw_words))
    return raw_words, list(filter(None,w_host)), list(filter(None,w_path))

def get_domain(url):
    o = urllib.parse.urlsplit(url)
    return o.hostname, tldextract.extract(url).domain, o.path
