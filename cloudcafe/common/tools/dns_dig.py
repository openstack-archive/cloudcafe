"""
Copyright 2016 Rackspace

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
import re
from dns import resolver


def dig(url, dig_type=None):
    """
    Use dns.resolver to query the provided url and return the target from the
    answer. Resolver will raise an exception if no Answer is returned from the
    query.
    """
    for rdata in resolver.query(url, dig_type):
        return rdata.target


def dig_search(url, search_string=None):
    """
    Recursively digs URL's until one with the specified search string is
    found. Otherwise return None.
    """
    url = str(url)

    if re.search(search_string, url):
        # Found search string in url, return it
        return url
    elif not url:
        return
    else:
        # Dig on the url
        url = dig(url, dig_type="cname")
        return dig_search(url, search_string)
