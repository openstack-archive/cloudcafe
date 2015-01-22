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

import unittest

from cloudcafe.events.pipeline_utilities import (
    Result, box_data, bind, PipelineTask, combine_result_with_and,
    combine_result_with_or, Pipeline, PipelineRuntimeError)


class TestResult(unittest.TestCase):
    """Test Result type"""

    def test_box_data(self):
        """Test box_data method creates default Result"""
        msg = 'test'
        result = box_data(msg)
        self.assertEqual(result, Result(True, msg))


class CheckEmailNotEmpty(PipelineTask):
    """Example pipeline task"""
    inputs = ['email']

    @classmethod
    def task(cls, data):
        if data['email']:
            return cls.succeeded(data)
        else:
            return cls.failed('email was empty')


class CheckNameNotEmpty(PipelineTask):
    """Example pipeline task"""
    inputs = ['name']

    @classmethod
    def task(cls, data):
        if data['name']:
            return cls.succeeded(data)
        else:
            return cls.failed('name was empty')


class TestPipelineMethods(unittest.TestCase):
    """Test methods used by Pipeline class"""

    good = Result(success=True, payload={'email': 'test@test.com'})
    bad = Result(success=False, payload={'bad': 'error'})
    alt_bad = Result(success=False, payload={'alt_bad': 'bad'})

    def test_bind(self):
        """Test bind method works for both kinds of Result input"""
        task = bind(CheckEmailNotEmpty.task)

        good_result = task(self.good)
        bad_result = task(self.bad)
        self.assertEqual(good_result, self.good)
        self.assertEqual(bad_result, self.bad)

    def test_combine_and_both_success(self):
        """Test Result AND combinator"""
        result = combine_result_with_and(self.good, self.good)
        self.assertEqual(result, self.good)

    def test_combine_and_first_failure(self):
        """Test Result AND combinator"""
        result = combine_result_with_and(self.bad, self.good)
        self.assertEqual(result, self.bad)

    def test_combine_and_second_failure(self):
        """Test Result AND combinator"""
        result = combine_result_with_and(self.good, self.bad)
        self.assertEqual(result, self.bad)

    def test_combine_and_both_failure(self):
        """Test Result AND combinator"""
        result = combine_result_with_and(self.bad, self.alt_bad)
        self.assertEqual(
            result.payload, dict(self.bad.payload, **self.alt_bad.payload))

    def test_combine_or_both_success(self):
        """Test Result OR combinator"""
        result = combine_result_with_or(self.good, self.good)
        self.assertEqual(result, self.good)

    def test_combine_or_first_failure(self):
        """Test Result OR combinator"""
        result = combine_result_with_or(self.bad, self.good)
        self.assertEqual(result, self.good)

    def test_combine_or_second_failure(self):
        """Test Result OR combinator"""
        result = combine_result_with_or(self.good, self.bad)
        self.assertEqual(result, self.good)

    def test_combine_or_both_failure(self):
        """Test Result OR combinator"""
        result = combine_result_with_or(self.bad, self.alt_bad)
        self.assertEqual(
            result.payload, dict(self.bad.payload, **self.alt_bad.payload))


class TestPipeline(unittest.TestCase):
    """Test Pipeline class"""

    good_data = {'email': 'test@test.com',
                 'name': 'bob'}
    good_extra_input = {'email': 'test@test.com',
                        'name': 'bob',
                        'id': 1}
    bad_data_empty = {'email': '',
                      'name': ''}
    bad_data_missing_input = {'email': 'test@test.com'}

    pipeline = Pipeline('Test')

    pipeline.add_task(CheckEmailNotEmpty)
    pipeline.add_task(CheckNameNotEmpty)
    pipeline.add_parallel_tasks([CheckEmailNotEmpty, CheckNameNotEmpty])

    def test_happy_path(self):
        """Check that valid pipeline workflow is successful"""
        result = self.pipeline.run_pipeline(
            self.good_data, print_summary=False)
        self.assertTrue(result.success)

    def test_failed_validation(self):
        """Check that failure result correctly returned by tasks"""
        result = self.pipeline.run_pipeline(
            self.bad_data_empty, print_summary=False)
        self.assertTrue(result.failure)

    def test_missing_input(self):
        """Check that pipeline won't run with missing input"""
        with self.assertRaises(PipelineRuntimeError):
            self.pipeline.run_pipeline(
                self.bad_data_missing_input, print_summary=False)

    def test_extra_input(self):
        """Check that pipeline allows (although ignores) extra input"""
        result = self.pipeline.run_pipeline(
            self.good_extra_input, print_summary=False)
        self.assertTrue(result.success)

    def test_add_invalid_task(self):
        """Check that pipeline rejects invalid task"""
        with self.assertRaises(TypeError):
            self.pipeline.add_task([])

    def test_add_nonlist_parallel_tasks(self):
        """Check that pipeline rejects non-list parallel tasks"""
        with self.assertRaises(TypeError):
            self.pipeline.add_parallel_tasks('')

    def test_add_invalid_parallel_task(self):
        """Check that pipeline rejects invalid parallel task"""
        with self.assertRaises(TypeError):
            self.pipeline.add_parallel_tasks([TestPipeline])

    def test_get_summary(self):
        """Check that a summary is present after running pipeline"""
        self.pipeline.run_pipeline(self.good_data, print_summary=False)
        summary = self.pipeline.get_summary()
        self.assertGreater(len(summary), 0)
