# Copyright is waived. No warranty is provided. Unrestricted use and modification is permitted.

import sys


# Make xrange() available in a version-independent manner
try:
    xrange = xrange
except NameError:
    xrange = range


# Make raw_input() available in a version-independent manner
try:
    raw_input = raw_input
except NameError:
    raw_input = input


# Make quote() available in a version-independent manner
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


# Make urlencode() available in a version-independent manner
try:
    from urllib import urlencode            # Python 2
except ImportError:
    from urllib.parse import urlencode      # Python 3


# Return any string or byte type as str()
def as_string(value):
    if sys.version_info.major >= 3:
        if type(value) is bytes:
            return value.decode("latin_1")  # bytes() --> str()
        elif type(value) is bytearray:
            return value.decode("latin_1")  # bytearray() --> str()
        else:
            return value                    # str()
    else:
        if type(value) is str:
            return value                    # str()
        elif type(value) is bytearray:
            return str(value)               # bytearray() -> str()
        else:
            return value.encode("latin_1")  # unicode() -> str()


# Return any string or byte type as bytes()
def as_bytes(value):
    if sys.version_info.major >= 3:
        if type(value) is str:
            return value.encode("latin_1")        # str() --> bytes()
        elif type(value) is bytearray:
            return bytes(value)                   # bytearray() --> bytes()
        else:
            return value                          # bytes()
    else:
        if type(value) is str:
            return bytes(value)                   # str() -> bytes()  (really a noop)
        elif type(value) is bytearray:
            return bytes(value)                   # bytearray() -> bytes()
        else:
            return bytes(value.encode("latin_1")) # unicode() -> bytes()


# Version-independent wrapper for simple synchronous network I/O
try:
    from urllib2 import Request, urlopen, HTTPError, URLError           # Python 2
except ImportError:
    from urllib.request import Request, urlopen, HTTPError, URLError    # Python 3


def urlrequest(uri, method=None, data=None, headers=None):
    request = Request(uri)
    if method:
        request.get_method = lambda: method
    if data:
        request.data = data
    if headers:
        for k, v in headers.items():
            request.add_header(k, v)
    try:
        fp = urlopen(request)
        headers = {key.lower(): fp.headers[key] for key in fp.headers}
        return fp.code, fp.read(), headers                  # On success the response body is returned as bytes()
    except HTTPError as e:
        headers = {key.lower(): e.headers[key] for key in e.headers}
        return e.code, as_string(e.read()), headers         # On fail the response body is returned as str()
    except URLError as e:
        return 0, "URL Error", []
