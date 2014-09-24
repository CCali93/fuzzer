#This is a set of helper functions to increase separation of concerns

from urllib.parse import urlparse, parse_qs

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

def validate_url(url, source_url):
    not_equal_to_source = not _urls_equal(url, source_url)
    not_absolute = not _is_absolute_url(url)
    no_mailto_links = 'mailto' not in url
    no_dots = '.' not in url
    no_cross_domain = _get_url_domain(url) != _get_url_domain(source_url)
    no_domain = url != _get_url_domain(source_url)

    return (
        not_equal_to_source and no_mailto_links and no_dots and no_cross_domain\
        and no_domain
    ) or (
        not_absolute and no_mailto_links
    )

"""
Gets the doman of a url
Ex: http://www.youtube.com/watch would return http://www.youtube.com/
"""
def _get_url_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain

"""
Tests if a URL is an absolute URL:
Ex: http://www.youtube.com/watch would return true. /watch would return false
"""
def _is_absolute_url(url):
    return bool(urlparse(url).netloc)

def _urls_equal(src_url, other_url):
    src_url = src_url if src_url.endswith('/') else src_url + '/'
    other_url = other_url if other_url.endswith('/') else other_url + '/'

    return urlparse(other_url) == urlparse(other_url)