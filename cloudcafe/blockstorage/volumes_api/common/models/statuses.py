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
from cafe.configurator.managers import _NamespaceDict

_CommonStatus = _NamespaceDict(**dict(
    AVAILABLE="available",
    DELETING="deleting",
    CREATING="creating",
    ERROR="error",
    ERROR_DELETING="error_deleting"))

Volume = _NamespaceDict(**dict(
    ATTACHING="attaching",
    IN_USE="in-use"))
Volume.update(_CommonStatus)

Snapshot = _NamespaceDict()
Snapshot.update(_CommonStatus)
