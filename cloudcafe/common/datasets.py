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
from random import shuffle
from cafe.drivers.unittest.datasets import DatasetList


class DatasetGeneratorError(Exception):
    pass


class ModelBasedDatasetToolkit(object):
    """Collection of dataset generators and helper methods for
    developing data driven tests
    """
    INCLUSION_MODE = 'inclusion'
    EXCLUSION_MODE = 'exclusion'

    @classmethod
    def _get_model_list(
            cls, get_model_list_method, model_type_name,
            *get_method_args, **get_method_kwargs):
        """Gets list of all models in the environment."""

        resp = get_model_list_method(*get_method_args, **get_method_kwargs)
        if not resp.ok:
            raise DatasetGeneratorError(
                "Unable to retrieve list of {0} during data-driven-test "
                "setup".format(model_type_name))

        if resp.entity is None:
            raise DatasetGeneratorError(
                "Unable to retrieve list of {0} during data-driven-test "
                "setup: Request failed with an HTTP {0} ERROR".format(
                    model_type_name, resp.status_code))

        return resp.entity

    @classmethod
    def _filter_model_list(
            cls, model_list, model_filter=None, filter_mode=None):
        """Filters should be dictionaries with model attributes as keys and
        lists of attributes as key values.
        example: {"id": ["12345", "42"]}
        Include only those models who match at least one criteria in the
        model_filter dictionary.
        filter_mode can be 'inclusion' or 'exclusion'.
        inclusion mode will include models that match any attributes in
        the model_filter in the final model_list.
        exclusion mode will exclude any models that match attributes in
        the model-filer from the final model_list.
        """
        if not filter_mode:
            raise Exception(
                "_filter_model_list must me called with a mode set to either "
                " 'inclusive' or 'exclusive'")

        if not model_filter:
            return model_list

        final_list = []
        for model in model_list:
            for k in model_filter:
                if filter_mode == cls.INCLUSION_MODE:
                    if str(getattr(model, k)) in model_filter[k]:
                        final_list.append(model)
                        break
                elif filter_mode == cls.EXCLUSION_MODE:
                    if not (str(getattr(model, k)) in model_filter[k]):
                        final_list.append(model)
                        break
        return final_list

    @classmethod
    def _modify_dataset_list(
            cls, dataset_list, max_datasets=None, randomize=False):
        """Aggregates common modifiers for dataset lists"""

        if randomize:
            shuffle(dataset_list)

        if max_datasets:
            dataset_list = DatasetList(dataset_list[:max_datasets])

        return dataset_list
