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
from multiprocessing import Process


class Resource(object):
    """
    @summary: Keeps details of a resource like server
              or image and how to delete it.
    """

    def __init__(self, resource_id, delete_function):
        self.resource_id = resource_id
        self.delete_function = delete_function

    def delete(self):
        """
        @summary: Deletes the resource
        """
        self.delete_function(self.resource_id)


class ResourcePool(object):
    """
    @summary: Pool of resources to be tracked for deletion.
    """
    def __init__(self):
        self.resources = []

    def add(self, resource_id, delete_function):
        """
        @summary: Adds a resource to the resource pool
        @param resource_id: Unique identifier of resource
        @type resource_id: string
        @param delete_function: The function to be called to delete a server
        @type delete_function: Function Pointer
        """
        self.resources.append(Resource(resource_id, delete_function))

    def release(self, async=False):
        """
        @summary: Delete all the resources in the Resource Pool
        """
        if async:
            self.release_asynchronously()
            return

        else:
            for resource in self.resources:
                try:
                    resource.delete()
                except:
                    pass

    def release_asynchronously(self):
        """Delete all the resources in the Resource Pool asynchronously"""

        running_processes = []
        for resource in self.resources:
            try:
                p = Process(
                    target=resource.delete, args=(resource.resource_id,))
                p.start()
                running_processes.append(p)
            except:
                pass

        for p in running_processes:
            try:
                p.join()
            except:
                pass
