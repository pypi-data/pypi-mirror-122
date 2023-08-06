import base64
import urllib.parse
import zlib

from xsdata.formats.dataclass.parsers import XmlParser

from pareqs.models.pares import ThreeDSecure

xml_parser = XmlParser()


def url_decode(url):
    return urllib.parse.unquote(url)


def base64_decode(base64_encoded):
    return base64.b64decode(base64_encoded)


def zlib_decode(zlib_encoded):
    return zlib.decompress(zlib_encoded)


def decode_pareqs(encoded_pareqs: str) -> str:
    u = url_decode(encoded_pareqs)
    b = base64_decode(u.encode())
    return zlib_decode(b).decode()


def parse_pareqs(encoded_pareqs: str) -> ThreeDSecure:
    return xml_parser.from_string(decode_pareqs(encoded_pareqs), ThreeDSecure)
