#This is a set of helper functions to increase separation of concerns

from urllib.parse import urlparse, parse_qs

"""
Gets the doman of a url
Ex: http://www.youtube.com/watch would return http://www.youtube.com/
"""
def get_url_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain

"""
Gets the various url parameters in a url
Ex: http://www.youtube.com/watch?abc=xyz would return ['abc']
"""
def get_url_params(url):
    parsed_url = urlparse(url)
    qs_parsed_url = parse_qs(parsed_url.query)

    params = []
    for key in qs_parsed_url:
        params.append(key)
    return params

"""
Returns the URL without url parameters on it.
Ex: http://www.youtube.com/watch?abc=xyz would return
http://www.youtube.com/watch
"""
def trim_url_params(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path

"""
Tests if a URL is an absolute URL:
Ex: http://www.youtube.com/watch would return true. /watch would return false
"""
def is_absolute_url(url):
    return bool(urlparse(url).netloc)