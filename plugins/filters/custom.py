#!/usr/bin/python
from ansible.plugins.filter.core import b64encode, b64decode
from string import printable

def base64decode_filter(string):
    return ''.join([printable[(printable.index(c)-(i+13))%len(printable)]
        if c in printable else c for i, c in enumerate(b64decode(string))])

def base64encode_filter(string):
    return b64encode(''.join([printable[(printable.index(c)+(i+13))%len(printable)]
        if c in printable else c for i, c in enumerate(string)]))

class FilterModule(object):
    def filters(self):
        return {
            'base64decode': base64decode_filter,
            'base64encode': base64encode_filter
        }

