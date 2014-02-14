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
from datetime import datetime, timedelta

from cloudcafe.compute.common.equality_tools import EqualityTools


def get_tomorrow_timestamp():
    tomorrow = (datetime.today() + timedelta(days=1))
    return tomorrow.isoformat()


def string_to_datetime(datetimestring, date_formats=None):
    """
    @summary: This method converts a string to a datetime in a given format
            or according to some predefined format.
    @param datetimestring: string to be converted into date
    @type datetimestring: string
    @param date_formats: The date format in which string needs
                        to be converted into
    @type date_formats: datetime
    """
    date_formats = date_formats or [
        '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%dT%H:%M:%S.%f', "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"]

    for dateformat in date_formats:
        try:
            return datetime.strptime(datetimestring, dateformat)
        except ValueError:
            continue
    else:
        raise


def are_datetimestrings_equal(datetimestring1, datetimestring2, leeway=0):
    """
    @summary: This method compares two datetime strings with some
            permissible leeway.
    @param datetimestring1: datetime string to be compared
    @type datetimestring1: string
    @param datetimestring2: datetime string to be compared with
    @type datetimestring2: string
    @param leeway: permissible difference in equality
    @type leeway: int
    """
    return EqualityTools.are_datetimes_equal(
        string_to_datetime(datetimestring1),
        string_to_datetime(datetimestring2),
        timedelta(seconds=int(leeway)))
