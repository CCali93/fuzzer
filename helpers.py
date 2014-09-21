from urllib.parse import urlparse, parse_qs

def get_url_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain

def get_url_params(url):
    parsed_url = urlparse(url)
    qs_parsed_url = parse_qs(parsed_url.query)

    params = []
    for key in qs_parsed_url:
        params.append(key)
    return params

def trim_url_params(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc + parsed_url.path

def is_absolute_url(url):
    return bool(urlparse(url).netloc)