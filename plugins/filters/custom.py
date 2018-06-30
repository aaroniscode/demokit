#!/usr/bin/python
from ansible.errors import AnsibleFilterError
from ansible.module_utils.six import string_types
from ansible.plugins.filter.core import b64encode, b64decode
from string import printable

def base64decode_filter(string):
    return ''.join([printable[(printable.index(c)-(i+13))%len(printable)]
        if c in printable else c for i, c in enumerate(b64decode(string))])

def base64encode_filter(string):
    return b64encode(''.join([printable[(printable.index(c)+(i+13))%len(printable)]
        if c in printable else c for i, c in enumerate(string)]))

def le_subelements(obj, subelements, skip_missing=False):
    # Modified version of subelements filter. Subelements are a dict, not a list
    # Used to support loop on the results from the letsencrypt challenge
    if isinstance(obj, dict):
        element_list = list(obj.values())
    elif isinstance(obj, list):
        element_list = obj[:]
    else:
        raise AnsibleFilterError('obj must be a list of dicts or a nested dict')

    if isinstance(subelements, list):
        subelement_list = subelements[:]
    elif isinstance(subelements, string_types):
        subelement_list = subelements.split('.')
    else:
        raise AnsibleFilterError('subelements must be a list or a string')

    results = []

    for element in element_list:
        values = element
        for subelement in subelement_list:
            try:
                values = values[subelement]
            except KeyError:
                if skip_missing:
                    values = {}
                    break
                raise AnsibleFilterError("could not find %r key in iterated item %r" % (subelement, values))
            except TypeError:
                raise AnsibleFilterError("the key %s should point to a dictionary, got '%s'" % (subelement, values))
        if not isinstance(values, dict):
            raise AnsibleFilterError("the key %r should point to a dict, got %r" % (subelement, values))

        for key, value in values.iteritems():
            results.append((element, key))

    return results

class FilterModule(object):
    def filters(self):
        return {
            'base64decode': base64decode_filter,
            'base64encode': base64encode_filter,
            'le_subelements': le_subelements
        }

