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

from cafe.drivers.unittest.datasets import DatasetList, _Dataset
from cafe.drivers.unittest.decorators import memoized

from cloudcafe.common.datasets import ModelBasedDatasetToolkit
from cloudcafe.blockstorage.composites import VolumesAutoComposite

# Prevent non-integration consumers from breaking when compute
# service is unavailable.
try:
    from cloudcafe.compute.datasets import ComputeDatasets
except Exception as ex:
    import warnings
    msg = "Compute integration datasets are unavailable"
    warnings.warn(msg)
    # Dummy class to prevent errors when non-integrating consumers import
    # this class while compute services are unavailable

    class ComputeDatasets(object):
        pass


class BlockstorageDatasets(ModelBasedDatasetToolkit):
    """Collection of dataset generators for blockstorage data driven tests"""
    _volumes = VolumesAutoComposite()

    @classmethod
    @memoized
    def _get_volume_types(cls):
        """Gets list of all Volume Types in the environment, and caches it for
        future calls"""
        return cls._get_model_list(
            cls._volumes.client.list_all_volume_types, 'volume_types')

    @classmethod
    def _get_volume_type_names(cls):
        """Gets list of all Volume Type Names in the environment, and caches it
        for future calls"""
        vtype_names = []
        for vtype in cls._get_volume_types():
            vtype_names.append(vtype.name)
        return vtype_names

    @classmethod
    def default_volume_type_model(cls):
        for vtype in cls._get_volume_types():
            if (vtype.id_ == cls._volumes.config.default_volume_type
                    or vtype.name == cls._volumes.config.default_volume_type):
                return vtype

        raise Exception("Unable to get configured default volume type")

    @classmethod
    def default_volume_type(cls):
        vol_type = cls.default_volume_type_model()
        dataset = _Dataset(
            name=vol_type.name,
            data_dict={
                'volume_type_name': vol_type.name,
                'volume_type_id': vol_type.id_})
        dataset_list = DatasetList()
        dataset_list.append(dataset)
        return dataset_list

    @classmethod
    def volume_types(
            cls, max_datasets=None, randomize=None, model_filter=None,
            filter_mode=ModelBasedDatasetToolkit.INCLUSION_MODE, tags=None):
        """Returns a DatasetList of all VolumeTypes
        Filters should be dictionaries with model attributes as keys and
        lists of attributes as key values
        """

        volume_type_list = cls._get_volume_types()
        volume_type_list = cls._filter_model_list(
            volume_type_list, model_filter=model_filter,
            filter_mode=filter_mode)

        dataset_list = DatasetList()
        for vol_type in volume_type_list:
            data = {'volume_type_name': vol_type.name,
                    'volume_type_id': vol_type.id_}
            dataset_list.append_new_dataset(vol_type.name, data)

        # Apply modifiers
        dataset_list = cls._modify_dataset_list(
            dataset_list, max_datasets=max_datasets, randomize=randomize)

        # Apply Tags
        if tags:
            dataset_list.apply_test_tags(*tags)

        return dataset_list

    @classmethod
    def configured_volume_types(
            cls, max_datasets=None, randomize=False, tags=None):
        """Returns a DatasetList of permuations of Volume Types and Images.
        Requests all available images and volume types from API, and applies
        pre-configured image and volume_type filters.
        """

        volume_type_filter = cls._volumes.config.volume_type_filter
        volume_type_filter_mode = cls._volumes.config.volume_type_filter_mode
        return cls.volume_types(
            max_datasets=max_datasets,
            randomize=randomize,
            model_filter=volume_type_filter,
            filter_mode=volume_type_filter_mode,
            tags=tags)


class ComputeIntegrationDatasets(ComputeDatasets, BlockstorageDatasets):

    @classmethod
    def images_by_volume_type(
            cls, max_datasets=None, randomize=False,
            image_filter=None, volume_type_filter=None,
            image_filter_mode=ModelBasedDatasetToolkit.INCLUSION_MODE,
            volume_type_filter_mode=ModelBasedDatasetToolkit.INCLUSION_MODE):
        """Returns a DatasetList of all combinations of Images and
        Volume Types.
        Filters should be dictionaries with model attributes as keys and
        lists of attributes as key values
        """
        image_list = cls._get_images()
        image_list = cls._filter_model_list(
            image_list, model_filter=image_filter,
            filter_mode=image_filter_mode)

        volume_type_list = cls._get_volume_types()
        volume_type_list = cls._filter_model_list(
            volume_type_list, model_filter=volume_type_filter,
            filter_mode=volume_type_filter_mode)

        # Create dataset from all combinations of all images and volume types
        dataset_list = DatasetList()
        for vtype in volume_type_list:
            for image in image_list:
                data = {'volume_type': vtype,
                        'image': image}
                testname = \
                    "{0}_and_{1}".format(
                        str(vtype.name).replace(" ", "_"),
                        str(image.name).replace(" ", "_"))
                dataset_list.append_new_dataset(testname, data)

        # Apply modifiers
        return cls._modify_dataset_list(
            dataset_list, max_datasets=max_datasets, randomize=randomize)

    @classmethod
    def flavors_by_images_by_volume_type(
            cls, max_datasets=None, randomize=None,
            flavor_filter=None, volume_type_filter=None, image_filter=None,
            flavor_filter_mode=ModelBasedDatasetToolkit.INCLUSION_MODE,
            volume_type_filter_mode=ModelBasedDatasetToolkit.INCLUSION_MODE,
            image_filter_mode=ModelBasedDatasetToolkit.INCLUSION_MODE,):
        """Returns a DatasetList of all combinations of Flavors and
        Volume Types.
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

        volume_type_list = cls._get_volume_types()
        volume_type_list = cls._filter_model_list(
            volume_type_list, model_filter=volume_type_filter,
            filter_mode=volume_type_filter_mode)

        # Create dataset from all combinations of all images, flavors, and
        # volume types
        dataset_list = DatasetList()
        for vtype in volume_type_list:
            for flavor in flavor_list:
                for image in image_list:
                    data = {'volume_type': vtype,
                            'flavor': flavor,
                            'image': image}
                    testname = \
                        "{flavor}_{image}_on_{vtype}".format(
                            flavor=str(flavor.name), image=str(image.name),
                            vtype=str(vtype.name)).replace(' ', '_').replace(
                            '.', '_').replace('(', '').replace(')', '')
                    dataset_list.append_new_dataset(testname, data)

        # Apply modifiers
        return cls._modify_dataset_list(
            dataset_list, max_datasets=max_datasets, randomize=randomize)

    @classmethod
    def configured_images(cls, max_datasets=None, randomize=None):
        """Returns a DatasetList of permuations of Images.
        Requests all available images from API, and applies pre-configured
        image and volume_type filters.
        """

        image_filter = cls._volumes.config.image_filter
        image_filter_mode = cls._volumes.config.image_filter_mode
        return cls.images(
            max_datasets=max_datasets, randomize=randomize,
            model_filter=image_filter, filter_mode=image_filter_mode)

    @classmethod
    def configured_images_by_volume_type(
            cls, max_datasets=None, randomize=None):
        """Returns a DatasetList of permuations of Volume Types and Images.
        Requests all available images and volume types from the API, and
        applies pre-configured image and volume_type filters.
        """

        image_filter = cls._volumes.config.image_filter
        volume_type_filter = cls._volumes.config.volume_type_filter
        image_filter_mode = cls._volumes.config.image_filter_mode
        volume_type_filter_mode = cls._volumes.config.volume_type_filter_mode
        return cls.images_by_volume_type(
            max_datasets=max_datasets, randomize=randomize,
            image_filter=image_filter, volume_type_filter=volume_type_filter,
            image_filter_mode=image_filter_mode,
            volume_type_filter_mode=volume_type_filter_mode)

    @classmethod
    def configured_images_by_flavor(cls, max_datasets=None, randomize=None):
        """Returns a DatasetList of permuations of Images and Flavors.
        Requests all available images and flavors from the API, and applies
        pre-configured image and flavor filters.
        """
        image_filter = cls._volumes.config.image_filter
        image_filter_mode = cls._volumes.config.image_filter_mode
        flavor_filter = cls._volumes.config.flavor_filter
        flavor_filter_mode = cls._volumes.config.flavor_filter_mode
        return cls.images_by_flavor(
            max_datasets=max_datasets, randomize=randomize,
            image_filter=image_filter, flavor_filter=flavor_filter,
            image_filter_mode=image_filter_mode,
            flavor_filter_mode=flavor_filter_mode)

    @classmethod
    def configured_images_by_flavor_by_volume_type(
            cls, max_datasets=None, randomize=None):
        """Returns a DatasetList of permuations of Images, Flavors and
        VolumeTypes. Requests all available images, flavors and volume-types
        from the API, and applies pre-configured image, flavor and volume-type
        filters.
        """
        image_filter = cls._volumes.config.image_filter
        image_filter_mode = cls._volumes.config.image_filter_mode
        flavor_filter = cls._volumes.config.flavor_filter
        flavor_filter_mode = cls._volumes.config.flavor_filter_mode
        volume_type_filter = cls._volumes.config.volume_type_filter
        volume_type_filter_mode = cls._volumes.config.volume_type_filter_mode
        return cls.flavors_by_images_by_volume_type(
            max_datasets=max_datasets, randomize=randomize,
            image_filter=image_filter, flavor_filter=flavor_filter,
            image_filter_mode=image_filter_mode,
            flavor_filter_mode=flavor_filter_mode,
            volume_type_filter=volume_type_filter,
            volume_type_filter_mode=volume_type_filter_mode)
