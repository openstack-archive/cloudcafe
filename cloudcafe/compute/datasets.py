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

from cafe.drivers.unittest.datasets import DatasetList
from cafe.drivers.unittest.decorators import memoized

from cloudcafe.common.datasets import ModelBasedDatasetToolkit
from cloudcafe.compute.composites import \
    _ComputeAuthComposite, ImagesComposite, FlavorsComposite


class ComputeDatasets(ModelBasedDatasetToolkit):
    """Collection of dataset generators for compute and compute-integration
    data driven tests
    """

    _images = ImagesComposite(_ComputeAuthComposite())
    _flavors = FlavorsComposite(_ComputeAuthComposite())

    @classmethod
    @memoized
    def _get_images(cls):
        """Gets list of all Images in the environment, and caches it for
        future calls"""
        return cls._get_model_list(
            cls._images.client.list_images_with_detail, 'images')

    @classmethod
    @memoized
    def _get_flavors(cls):
        """Gets list of all Flavors in the environment, and caches it for
        future calls"""
        return cls._get_model_list(
            cls._flavors.client.list_flavors_with_detail, 'flavors')

    @classmethod
    def images(
            cls, max_datasets=None, randomize=False, model_filter=None,
            filter_mode=ModelBasedDatasetToolkit.INCLUSION_MODE):
        """Returns a DatasetList of all Images.
        Filters should be dictionaries with model attributes as keys and
        lists of attributes as key values
        """
        image_list = cls._get_images()
        image_list = cls._filter_model_list(
            image_list, model_filter=model_filter, filter_mode=filter_mode)

        dataset_list = DatasetList()
        for img in image_list:
            data = {'image': img}
            dataset_list.append_new_dataset(
                str(img.name).replace(" ", "_").replace("/", "-"), data)

        # Apply modifiers
        return cls._modify_dataset_list(
            dataset_list, max_datasets=max_datasets, randomize=randomize)

    @classmethod
    def flavors(
            cls, max_datasets=None, randomize=False, model_filter=None,
            filter_mode=ModelBasedDatasetToolkit.INCLUSION_MODE):
        """Returns a DatasetList of all Flavors
        Filters should be dictionaries with model attributes as keys and
        lists of attributes as key values
        """
        flavor_list = cls._get_flavors()
        flavor_list = cls._filter_model_list(
            flavor_list, model_filter=model_filter, filter_mode=filter_mode)

        dataset_list = DatasetList()
        for flavor in flavor_list:
            data = {'flavor': flavor}
            dataset_list.append_new_dataset(
                str(flavor.name).replace(" ", "_").replace("/", "-"), data)

        # Apply modifiers
        return cls._modify_dataset_list(
            dataset_list, max_datasets=max_datasets, randomize=randomize)

    @classmethod
    def images_by_flavor(
            cls, max_datasets=None, randomize=False,
            image_filter=None, flavor_filter=None,
            image_filter_mode=ModelBasedDatasetToolkit.INCLUSION_MODE,
            flavor_filter_mode=ModelBasedDatasetToolkit.INCLUSION_MODE):
        """Returns a DatasetList of all combinations of Flavors and Images.
        Filters should be dictionaries with model attributes as keys and
        lists of attributes as key values
        """
        image_list = cls._get_images()
        image_list = cls._filter_model_list(
            image_list, model_filter=image_filter,
            filter_mode=image_filter_mode)

        flavor_list = cls._get_flavors()
        flavor_list = cls._filter_model_list(
            flavor_list, model_filter=flavor_filter,
            filter_mode=flavor_filter_mode)

        dataset_list = DatasetList()
        for image in image_list:
            for flavor in flavor_list:
                data = {'flavor': flavor,
                        'image': image}
                testname = \
                    "image_{0}_and_flavor_{1}".format(
                        str(image.name).replace(" ", "_").replace("/", "-"),
                        str(flavor.name).replace(" ", "_").replace("/", "-"))
                dataset_list.append_new_dataset(testname, data)

        # Apply modifiers
        return cls._modify_dataset_list(
            dataset_list, max_datasets=max_datasets, randomize=randomize)
