from urllib.parse import urlparse

def get_webpage_domain(url:str) -> str:
    return urlparse(url).netloc

def get_webpage_path(url:str) -> str:
    return urlparse(url).path