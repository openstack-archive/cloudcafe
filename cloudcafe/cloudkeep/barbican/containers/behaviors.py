"""
Copyright 2014 Rackspace

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
from cafe.engine.behaviors import BaseBehavior
from cloudcafe.cloudkeep.barbican.containers.models.container import SecretRef
from cloudcafe.cloudkeep.common.responses import CloudkeepResponse


class ContainerBehaviors(BaseBehavior):

    def __init__(self, client, secret_behaviors):
        self.client = client
        self.secret_behaviors = secret_behaviors
        self.created_containers = []

    def create_container(self, name, container_type, secret_refs):
        """ Proxies the ContainerClient's create_container and captures
        the resulting HATOAS ref for cleanup.
        """
        resp = self.client.create_container(
            name=name, container_type=container_type, secret_refs=secret_refs)

        if resp.entity and resp.entity.reference:
            self.created_containers.append(resp.entity.reference)

        return CloudkeepResponse(resp=resp, entity=resp.entity)

    def create_container_with_secret(self, name="test_container",
                                     secret_name="test_secret"):
        """Create a secret and a generic container with that secret inside.

        :param name: The name of the container
        :param secret_name: The name of the secret in the container
        :returns: A tuple containing the responses from the secret creation and
            the container creation, in that order
        """
        secret_resp = self.secret_behaviors.create_secret_from_config()
        secret_refs = [SecretRef(name=secret_name, ref=secret_resp.ref)]
        container_resp = self.create_container(name, "generic", secret_refs)
        return (secret_resp, container_resp)

    def remove_from_created_containers(self, container_ref):
        """ Clean-up helper method """
        if container_ref in self.created_containers:
            self.created_containers.remove(container_ref)

    def delete_container(self, container_ref):
        """ Proxies the ContainerClient's delete_container"""
        self.remove_from_created_containers(container_ref)
        return self.client.delete_container(container_ref)

    def delete_all_created_containers(self):
        """ Clean-up helper method to delete all containers created by
        using this class.
        """
        for container_ref in list(self.created_containers):
            self.delete_container(container_ref)
        self.created_containers = []

    def create_rsa_container(self, name, priv_key_ref, pub_key_ref,
                             priv_pass_ref=None):
        """ Creates an RSA container based on pre-created HATOAS secret
        reference urls.

        :param name: Container name
        :param priv_key_ref: HATOAS reference to a secret containing
            a private key.
        :param priv_pass_ref: HATOAS reference to a secret containing
            a private key passphrase.
        :param pub_key_ref: HATOAS reference to a secret containing
            a public key.
        """
        priv_pass = SecretRef(name='private_key_passphrase', ref=priv_pass_ref)
        priv = SecretRef(name='private_key', ref=priv_key_ref)
        pub = SecretRef(name='public_key', ref=pub_key_ref)

        refs = [pub, priv]
        if priv_pass_ref:
            refs.append(priv_pass)

        return self.create_container(name=name,
                                     container_type='rsa',
                                     secret_refs=refs)
