import math
import abc

import functools

import html

print(html.unescape('%C0%B4%B5%C3%BC%B0%B3%E4%B5%E7%C2%F0'))

import urllib.parse
print(urllib.parse.unquote('%C0%B4%B5%C3%BC%B0%B3%E4%B5%E7%C2%F0', encoding='gbk'))