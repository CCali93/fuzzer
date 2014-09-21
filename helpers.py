from urllib.parse import urlparse

def get_url_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain

def is_absolute_url(url):
    return bool(urlparse(url).netloc)