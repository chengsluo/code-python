import urllib


def get_search_key(url):
    str_url = urllib.parse.unquote(url)
    split = str_url.split("&")
    return split[0].split("=")[1]


def get_item_url(value):
    return "https:%s" % value if not str(value).startswith("http") else value


def decode_unicode(string):
    return bytes(string, "utf8").decode("unicode_escape")


def url_decode(url):
    return urllib.parse.unquote(url)
