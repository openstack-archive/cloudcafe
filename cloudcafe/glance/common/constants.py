"""
Copyright 2015 Rackspace

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


class ImageProperties(object):
    ID_REGEX = ('^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-'
                '[0-9a-fA-F]{12}$')
    TZ_REGEX = '[\-+]\d{,2}:\d{,2}'


class Messages(object):
    CONTAINER_DNE = 'Container not found. Container: {0}'
    DUPLICATE_FILE_MSG = ('Object already exists in user\'s container. '
                          'Container/Object: {0}/{1}.vhd')
    EXPORT_WINDOWS_MSG = ('Image cannot be exported due to licensing or '
                          'billing restrictions (com.rackspace__1__options: '
                          '\'{0}\')')
    EXTRA_IMAGE_PROPERTIES_MSG = ('Unsupported element in image_properties, '
                                  'please consult the documentation.')
    NOT_OWNER_MSG = 'An image may only be exported by the image owner.'
    IMAGE_NOT_FOUND = 'Image not found for import. Possible invalid location'
    OK_RESP_MSG = 'Unexpected response received.  Expected: OK, Received: {0}'
    PROPERTY_MSG = ('Unexpected value for {0} received. Expected: {1}, '
                    'Received: {2}')
    STATUS_CODE_MSG = ('Unexpected status code received. Expected: {0}, '
                       'Received: {1}')
    EXPORT_UNKNOWN_ERROR_MSG = 'Unknown error occurred during image export'
    UPDATE_IMAGE_MEMBER_STATUS = ('You are not permitted to modify \'status\' '
                                  'on this image.')
