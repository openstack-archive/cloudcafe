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

import raxcafe.common.workflow.base as wf


def wf1(data):
    actual = data
    expected = 'foo'
    if actual != expected:
        return wf.Error(expected=expected, actual=actual)

    return 'bar'


def wf2(data):
    actual = data
    expected = 'bar'
    if actual != expected:
        return wf.Error(expected=expected, actual=actual)

    return 'baz'


def wf3(data):
    actual = data
    expected = 'baz'
    if actual != expected:
        return wf.Error(expected=expected, actual=actual)

    return 'The End!'


def foo(data):
    actual = data
    expected = 'foo'
    if actual != expected:
        return wf.Error(expected=expected, actual=actual)


def bar(data):
    actual = data
    expected = 'bar'
    if actual != expected:
        return wf.Error(expected=expected, actual=actual)


def baz(data):
    actual = data
    expected = 'baz'
    if actual != expected:
        return wf.Error(expected=expected, actual=actual)


def bam(_):
    raise RuntimeError('Test exception')


class TestWorkflowUtilsSuccess(unittest.TestCase):
    def setUp(self):
        self.data = 'foo'

    def test_single_validation_succeeds(self):
        v = wf.WorkflowRunner('Single', [foo])
        result, data = v.run(self.data)
        self.assertTrue(result.success)
        self.assertEqual(data, None)

    def test_workflow_succeeds(self):
        v = wf.WorkflowRunner('Serial', [wf1, wf2, wf3])
        result, data = v.run(self.data)
        self.assertTrue(result.success)
        self.assertEqual(data, 'The End!')

    def test_parallel_workflow_succeeds(self):
        v = wf.WorkflowRunner('Parallel', [foo, foo], parallel=True)
        result, data = v.run(self.data)
        self.assertTrue(result.success)
        self.assertEqual(data, 'foo')

    def test_parallel_tasks_workflow_succeeds(self):
        v = wf.WorkflowRunner(
            'Parallel', [wf.ParallelTasks([foo, foo], 'Foo')])
        result, data = v.run(self.data)
        self.assertTrue(result.success)
        self.assertEqual(data, 'foo')

    def test_nested_workflow_succeeds(self):
        v = wf.WorkflowRunner(
            'Workflow',
            [wf1, wf.WorkflowRunner('Nested', [wf2, wf3])])
        result, data = v.run(self.data)
        self.assertTrue(result.success)
        self.assertEqual(data, 'The End!')

    def test_nested_parallel_workflow_succeeds(self):
        v = wf.WorkflowRunner(
            'Workflow',
            [
                wf1,
                wf.WorkflowRunner(
                    'Nested',
                    [
                        wf2,
                        wf.WorkflowRunner('Nested2', [wf2, bar], parallel=True)
                    ], parallel=True)
            ])
        result, data = v.run(self.data)
        self.assertTrue(result.success)
        self.assertEqual(data, 'bar')

    def test_complex_workflow(self):
        v = wf.WorkflowRunner(
            'Workflow',
            [
                wf1,
                wf.WorkflowRunner(
                    'Nested Validation', [wf2, bar],
                    parallel=True),
                wf2,
                wf.WorkflowRunner(
                    'Nested Validation', [wf3, baz],
                    parallel=True),
                wf.WorkflowRunner(
                    'Nested Workflow', [wf3, wf3],
                    parallel=True)
            ])
        result, data = v.run(self.data)
        self.assertTrue(result.success)
        self.assertEqual(data, 'baz')


class TestWorkflowUtilsFailure(unittest.TestCase):
    def setUp(self):
        self.data = 'foo'
        self.single_validation = wf.WorkflowRunner('Single', [bar])
        self.serial_validation = wf.WorkflowRunner('Serial', [wf1, wf3, wf2])
        self.parallel_validation = wf.WorkflowRunner(
            'Parallel', [wf.ParallelTasks([foo, bar, baz], 'Foobarbaz')])
        self.nested_workflow = wf.WorkflowRunner(
            'Nested', [foo, self.serial_validation])

    def test_single_validation_fails(self):
        v = self.single_validation
        result, data = v.run(self.data)
        self.assertFalse(result.success)

    def test_workflow_fails(self):
        v = self.serial_validation
        result, data = v.run(self.data)
        self.assertFalse(result.success)

    def test_workflow_fails_with_exception(self):
        v = wf.WorkflowRunner('Workflow', [bam])
        result, data = v.run(self.data)
        self.assertFalse(result.success)

    def test_nested_workflow_fails(self):
        v = self.nested_workflow
        result, data = v.run(self.data)
        self.assertFalse(result.success)

    def test_skip_after_failure(self):
        v = self.serial_validation
        result, data = v.run(self.data)
        r1 = result.results[0]
        r2 = result.results[1]
        r3 = result.results[2]

        self.assertTrue(r1.success)
        self.assertFalse(r2.success)
        self.assertFalse(r3.success)

        self.assertFalse(r1.skipped)
        self.assertFalse(r2.skipped)
        self.assertTrue(r3.skipped)

    def test_skip_after_workflow_failure(self):
        v = wf.WorkflowRunner('Workflow', [self.serial_validation, foo])
        result, data = v.run(self.data)
        r1 = result.results[0]
        r2 = result.results[1]

        self.assertFalse(r1.success)
        self.assertFalse(r2.success)

        self.assertFalse(r1.skipped)
        self.assertTrue(r2.skipped)

    def test_parallel_workflow_fails(self):
        v = self.parallel_validation
        result, data = v.run(self.data)
        self.assertFalse(result.success)

        workflow = result.results[0]
        r1 = workflow.results[0]
        r2 = workflow.results[1]
        r3 = workflow.results[2]
        self.assertTrue(r1.success)
        self.assertFalse(r2.success)
        self.assertFalse(r3.success)

    def test_no_skip_on_parallel_workflow_failure(self):
        v = self.parallel_validation
        result, data = v.run(self.data)

        workflow = result.results[0]
        r1 = workflow.results[0]
        r2 = workflow.results[1]
        r3 = workflow.results[2]

        self.assertTrue(r1.success)
        self.assertFalse(r2.success)
        self.assertFalse(r3.success)

        self.assertFalse(r1.skipped)
        self.assertFalse(r2.skipped)
        self.assertFalse(r3.skipped)


class TestValidatorBase(unittest.TestCase):
    def test_can_not_use_base_class_directly(self):
        with self.assertRaises(NotImplementedError):
            base = wf.ValidatorBase()
            base.workflow()

    def test_can_instantiate_child_class(self):
        class Child(wf.ValidatorBase):
            @classmethod
            def workflow(cls):
                pass

        child = Child()
        child.workflow()
