"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from uuid import uuid4
import random
from math import pow
import time

SOURCE_RANDOM = '/dev/urandom'
SOURCE_ZEROS = '/dev/zero'
TEMP_LOCATION = '/tmp'

#Binary prefixes
#IEE_MAGNITUDE = int(pow(2,10))
EXACT_BYTE = 8
EXACT_KIBIBYTE = int(pow(2, 10))
EXACT_MEBIBYTE = int(pow(2, 20))
EXACT_GIBIBYTE = int(pow(2, 30))
EXACT_TEBIBYTE = int(pow(2, 40))

#Decimal prefixes
#SI_MAGNITURE = int(pow(10,3))

EXACT_KILOBYTE = int(pow(10, 3))
EXACT_MEGABYTE = int(pow(10, 6))
EXACT_GIGABYTE = int(pow(10, 9))
EXACT_TERABYTE = int(pow(10, 12))


def timestamp_string(prefix=None, suffix=None, decimal_precision=6):
    '''
    Return a unix timestamp surrounded by any defined prefixes and suffixes
    Decimal precision is full (6) by default.
    '''
    t = str('%f' % time.time())
    int_seconds, dec_seconds = t.split('.')
    for x in range(6 - decimal_precision):
        dec_seconds = dec_seconds[:-1]

    int_seconds = str(int_seconds)
    dec_seconds = str(dec_seconds)
    prefix = prefix or ''
    suffix = suffix or ''
    final = None
    if len(dec_seconds) > 0:
        final = '%s%s%s' % (prefix, int_seconds, suffix)
    else:
        final = '%s%s.%s%s' % (prefix, int_seconds, dec_seconds, suffix)

    return final


def random_string(prefix=None, suffix=None, size=8):
    """
    Return exactly size bytes worth of base_text as a string
    surrounded by any defined pre or suf-fixes
    """

    base_text = str(uuid4()).replace('-', '0')

    if size <= 0:
        return '%s%s' % (prefix, suffix)

    extra = size % len(base_text)
    body = ''

    if extra == 0:
        body = base_text * size

    if extra == size:
        body = base_text[:size]

    if (extra > 0) and (extra < size):
        body = (size / len(base_text)) * base_text + base_text[:extra]

    body = str(prefix) + str(body) if prefix is not None else body
    body = str(body) + str(suffix) if suffix is not None else body
    return body


def random_ip(pattern=None):
    """
    Takes a pattern as a string in the format of #.#.#.# where a # is an
    integer, and a can be substituded with an * to produce a random octet.
    pattern = 127.0.0.* would return a random string between 127.0.0.1 and
    127.0.0.254
    """
    if pattern is None:
        pattern = '*.*.*.*'
    num_asterisks = 0
    for c in pattern:
        if c == '*':
            num_asterisks += 1
    rand_list = [random.randint(1, 255) for i in range(0, num_asterisks)]
    for item in rand_list:
        pattern = pattern.replace('*', str(item), 1)
    return pattern


def random_cidr(ip_pattern=None, mask=None, min_mask=0, max_mask=30):
    """
    Gets a random cidr using the random_ip function in this module. If mask
    is None then a random mask between 0 and 30 inclusive will be assigned.
    """
    if mask is None:
        mask = random.randint(min_mask, max_mask)
    ip = random_ip(ip_pattern)
    return ''.join([ip, '/', str(mask)])


def random_int(min_int, max_int):
    return random.randint(min_int, max_int)


def rand_name(name='test'):
    return name + str(random.randint(99999, 1000000))


def random_item_in_list(selection_list):
    return random.choice(selection_list)


def bytes_to_gb(val):
    return float(val) / 1073741824


def gb_to_bytes(val):
    return int(val * 1073741824)


def bytes_to_mb(val):
    return float(val) / 1024
