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


def deserialize(response_entity_type):
    """
    Auto-deserializes the response from any decorated client method call.

    Deserializes the response into response_entity_type domain object

    response_entity_type must be a Domain Object with a <format>_to_obj()
    classmethod defined for every supported format or this won't work.
    """

    def decorator(f):
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs)
            setattr(response.request, 'entity', None)
            setattr(response, 'entity', None)
            deserialize_format = None

            content_type = response.headers.get('content-type', '')

            formats = ['text', 'json', 'xml']
            for format_ in formats:
                if format_ in content_type:
                    deserialize_format = format_
                    break

            resp_entity = response_entity_type.deserialize(
                response.content,
                deserialize_format)

            setattr(response, 'entity', resp_entity)

            return response
        return wrapper
    return decorator
