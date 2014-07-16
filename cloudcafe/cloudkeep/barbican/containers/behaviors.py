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


class ContainerBehaviors(BaseBehavior):

    def __init__(self, client):
        self.client = client
        self.created_containers = []

    def create_container(self, name, container_type, secret_refs):
        """ Proxies the ContainerClient's create_container and captures
        the resulting HATOAS ref for cleanup.
        """
        resp = self.client.create_container(
            name=name, container_type=container_type, secret_refs=secret_refs)

        if resp.entity:
            self.created_containers.append(resp.entity.reference)

        return resp

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
        :param priv_key_ref: HATOAS reference to a secret with containing
            a private key.
        :param priv_pass_ref: HATOAS reference to a secret with containing
            a private key passphrase.
        :param pub_key_ref: HATOAS reference to a secret with containing
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
