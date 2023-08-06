from urllib.parse import urlparse, urlunparse, parse_qs

from pydash import head


def get_host_url(url):
    urlp = urlparse(url)
    return f"{urlp.scheme}://{urlp.hostname}"


def strip_query_params(url):
    parsed_url = urlparse(url)
    return urlunparse((parsed_url.scheme, parsed_url.hostname, parsed_url.path, "", "", ""))


def get_query_param(url, key):
    parsed_url = urlparse(url)
    return head(parse_qs(parsed_url.query).get(key))
