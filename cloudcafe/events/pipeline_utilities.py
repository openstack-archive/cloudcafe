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

from collections import namedtuple, OrderedDict
from functools import wraps
import re
import sys


class Result(object):
    """Result type for use in a pipeline

    This type is the interchange format used by tasks
    in the pipeline. This type functionally behaves
    as a union type that is switched based on the success
    attribute. If success is True, the payload will be
    the input data to the task. If success is False,
    the payload will be the error data produced by
    previous tasks in the pipeline.

    Attributes:
        success (bool): True if the task result was
            successful, False otherwise
        payload: Payload is different depending on the success
            variable. If success is True, payload is the input
            data for the pipeline. If success is False, payload
            is a dict with keys mapping the failed task name
            to the corresponding error message.

    Example:
        Result(True, 'A message to validate')
        Result(False, {'task1': 'Task 1 failed'})
    """
    def __init__(self, success=False, payload=None):
        self.success = success
        self.payload = payload
        self.failure = not success

    def __repr__(self):
        status = 'Success' if self.success else 'Failure'
        return '{status}: {payload}'.format(status=status,
                                            payload=self.payload)

    def __eq__(self, other):
        return ((self.success, self.payload, self.failure) ==
                (other.success, other.payload, other.failure))

    @classmethod
    def success(cls, payload):
        """Construct a success Result

        Args:
            payload (dict): Pipeline data

        Note:
            The payload should typically be the same
            data that was passed into a task.

        Returns:
            Result: Success result
        """

        return cls(True, payload)

    @classmethod
    def failure(cls, error_msg):
        """Construct a failure Result

        Args:
            error_msg (str): Reason for failure

        Returns:
            Result: Failure result with a dict payload
                that maps the task name to the error
                message.
        """
        caller_name = _get_caller()
        return cls(False, {caller_name: error_msg})


def box_data(data):
    """Box input data for pipeline

    This method 'boxes' data into the Result type
    needed by pipeline tasks.

    Args:
        data (dict): Input data for pipeline

    Returns:
        Result: A Result object encapsulating the input data
    """
    return Result.success(data)


def bind(task):
    """Bind a task method for use in a pipeline

    This decorator method adapts a task method to work
    in a pipeline. Specifically, it routes successful
    Result input to the task logic, and passes through
    failure Result input without performing any
    additional actions.

    Args:
        task: A task method that returns a Result

    Returns:
        function: Bound task that accepts and returns a Result

    Example:
                             <Before bind>
                                              ---> Result(Success)
                             -------------    |
                        data |           |    |
                        ---> |   Task    | ---|
                             |           |    |
                             -------------    |
                                              ---> Result(Failure)

    ==============================================================

                             <After bind>
                                              ---> Result(Success)
                             -------------    |
                        data |           |    |
        Result(Success) ---> |   Task    | ---|
                             |           |    |
                             -------------    |
        Result(Failure) -------------------------> Result(Failure)

    """
    @wraps(task)
    def inner(result):
        if result.success:
            return task(result.payload)
        else:
            return result
    return inner


def combine_result_with_and(s1, s2=None):
    """Combine Result objects using AND logic

    This method combines Result objects using
    boolean AND logic. This is useful for combining
    the results of a batch of tasks run in parallel.

    Args:
        s1 (Result): The first Result to combine
        s2 (Result): The second Result to combine

    Returns:
        Result: The combined result

    Note:
        This method can be used in conjunction with
        the 'reduce' method to process a list of
        tasks.

    Example:

        R1<Success>
             *
        R2<Success>   ==>   Result<Success>
             *
        R3<Success>

        ====================================

        R1<Failure>
             *
        R2<Failure>   ==>   Result<Failure>
             *              (Combined R1/R2 payload)
        R3<Success>

    """
    if s1.success and s2.success:
        return Result(True, s1.payload)

    elif s1.success and s2.failure:
        return Result(False, s2.payload)

    elif s1.failure and s2.success:
        return Result(False, s1.payload)

    else:
        payload = dict(s1.payload, **s2.payload)
        return Result(False, payload)


def combine_result_with_or(s1, s2=None):
    """Combine Result objects using OR logic

    This method combines Result objects using
    boolean OR logic. This is useful for special cases
    where multiple valid options are possible. For example,
    two tasks could check the same metadata field for
    a different value, but either option is a valid choice.

    Args:
        s1 (Result): The first Result to combine
        s2 (Result): The second Result to combine

    Returns:
        Result: The combined result

    Note:
        This method can be used in conjunction with
        the 'reduce' method to process a list of
        tasks.

    Note:
        Warning!! Error messages from failed tasks will
        be discarded if any of the tasks in this batch
        are successful.


    Example:

        R1<Failure>
             +
        R2<Failure>   ==>   Result<Failure>
             +              (Combined R1/R2/R3 payload)
        R3<Failure>

        ====================================

        R1<Failure>
             +
        R2<Success>   ==>   Result<Success>
             +              (**R1 payload discarded**)
        R3<Success>

    """
    if not s2:
        return s1

    if s1.success:
        return Result(True, s1.payload)

    elif s2.success:
        return Result(True, s2.payload)

    else:
        payload = dict(s1.payload, **s2.payload)
        return Result(False, payload)


class PipelineTask(object):
    """Base class for pipeline tasks

    A pipeline task consists of a method to run in a pipeline,
    and a list of dictionary keywords specifying the parameters
    needed by the method.

    Attributes:
        inputs (list): List of strings that specify expected
            input parameters.

    Note:
        This class should not be instantiated directly.
    """

    inputs = None

    @staticmethod
    def task(data):
        """Method to run in a pipeline

        This method should be overridden in a subclass. It
        is expected to return a Result type.

        Note:
            The input data must not be modified!


        Example:
            condition = data['condition']

            if condition:
                return Result.success(data)
            else:
                return Result.failure('Condition was False')
        """
        raise NotImplementedError('Override this method in a subclass')


class PipelineRuntimeError(Exception):
    """Error during pipeline validation"""
    pass


class Pipeline(object):
    """Pipeline manager

    This class manages the logic for running tasks in a
    pipeline and collecting the results. To configure a
    pipeline, the user adds tasks using the add_task and
    add_parallel_tasks methods. The configured pipeline
    is run using run_pipeline. A summary of the pipeline
    results may be retrieved using get_summary.
    """

    def __init__(self, name):
        self._happy_path = True
        self._inputs = []
        self._pipeline = []
        self._summary = _ResultSummary(name)

    def add_task(self, task):
        """Add a task to the pipeline

        Add a task to the end of the pipeline. Tasks
        will be run sequentially in the order that
        they are added. Invalid input will be
        rejected.

        Args:
            task (subclass of PipelineTask): Task to add

        Raises:
            TypeError: If task is not a subclass of PipelineTask
        """
        self._process_added_task(task)

        self._pipeline.append(_box_task(task))

    def add_parallel_tasks(self, tasks, reduce_method=combine_result_with_and):
        """Add a batch of parallel tasks to the pipeline

        Add a batch of tasks to the pipeline that will be
        run in parallel. The combined result of the parallel
        tasks will be created using the provided reduce_method.
        Invalid input will be rejected.

        Args:
            tasks (list): Tasks to add. Each task must be a subclass
                of PipelineTask
            reduce_method (function, optional): Method to reduce
                parallel results to single Result. Defaults
                to combine_result_with_and.

        Raises:
            TypeError: If any task is not a subclass of PipelineTask
                or if tasks is not a list
        """

        if type(tasks) is not list:
            msg = 'Expected a list of tasks. Received: {}'
            raise TypeError(msg.format(tasks))

        boxed_tasks = []
        for task in tasks:
            self._process_added_task(task)
            boxed_tasks.append(_box_task(task))

        parallel_task = _ParallelPipelineTask(subtasks=boxed_tasks,
                                              reduce_method=reduce_method)
        self._pipeline.append(parallel_task)

    def get_summary(self):
        """Get a summary of pipeline results

        Get a summary of the results from each task in a
        pipeline after processing data with run_pipeline.

        Returns:
            str: Result summary
        """
        return str(self._summary)

    def run_pipeline(self, data, print_summary=True):
        """Process data with pipeline

        Run all configured pipeline tasks to process the
        input data.

        Args:
            data (dict): Data to process. The dict must include,
                at a minimum, all of the inputs required by
                the pipeline tasks.
            print_summary (bool): Print the result summary at the
                conclusion of the run if True, else print nothing

        Returns:
            Result: The result of processing.

        Raises:
            PipelineRuntimeError: If expected input was not present
        """

        self._check_inputs(data)

        data = box_data(data)

        for item in self._pipeline:
            if type(item) is _ParallelPipelineTask:
                subtasks, reduce_method = item
                tasks, names = zip(*subtasks)
                data = _process_parallel(tasks, data, reduce_method)

                name_str = ', '.join(names)
                type_str = (
                    'AND' if reduce_method is combine_result_with_and else 'OR')
                name = '<<{type_str}>>( {name_str} )'.format(
                    type_str=type_str, name_str=name_str)
                self._update_summary(data, name)
            else:
                task, name = item
                data = task(data)
                self._update_summary(data, name)

        if print_summary:
            print(self.get_summary())

        return data
    
    def _check_inputs(self, inputs):
        """Verify inputs match task requirements"""

        actual = set(inputs.keys())
        expected = set(self._inputs)
        missing = expected - actual

        if set(inputs.keys()) != set(self._inputs):
            msg = (
                'Pipeline expected the following inputs: {inputs}. '
                'Missing: {missing}'.format(
                    inputs=list(expected), missing=list(missing)))
            raise PipelineRuntimeError(msg)
        
    def _process_added_task(self, task):
        """Check type and update input requirements"""

        if not issubclass(task, PipelineTask):
            raise TypeError()

        self._inputs = list(set(task.inputs).union(self._inputs))

    def _update_summary(self, result, name):
        """Update result summary"""

        if result.success:
            self._summary[name] = 'Success'
        elif result.failure and self._happy_path:
            self._summary[name] = 'Failure'
            self._happy_path = False
        else:
            self._summary[name] = 'Skipped'


def _box_task(task):
    """Prepare task for pipeline"""
    return bind(task.task), task.__name__


def _get_caller():
    """Retrieve caller method name"""
    return sys._getframe(2).f_code.co_name


_ParallelPipelineTask = namedtuple('_ParallelPipelineTask',
                                   ['subtasks', 'reduce_method'])


def _process_parallel(tasks, data, reduce_method=combine_result_with_and):
    """Process a list of tasks in parallel

    This method processes a list of tasks and then
    combines the results using the reduce_method

    Args:
        tasks (list): List of bound tasks
        data (Result): 'Boxed' data input for tasks
        reduce_method (function, optional): Method to reduce
            inputs to single Result. Defaults to combine_result_with_and.

    Returns:
        Result: Combined result of all tasks
    """
    return reduce(reduce_method, [task(data) for task in tasks])


class _ResultSummary(OrderedDict):
    """Summary of pipeline task results

    Results are stored as an OrderedDict to preserve
    task order. Keys are the task name and values are
    strings representing the result of the task. The class
    can be printed directly to produce a nicely-formatted table
    of results.

    Note:
        This class is used internally by Pipeline, and is not
        intended to be used elsewhere.
    """
    def __init__(self, name):
        super(_ResultSummary, self).__init__()
        self.name = name

    def __repr__(self):
        step = 1
        summary = '\nPipeline Results ({name}):'.format(name=self.name)

        if self.__len__() == 0:
            msg = 'No results -- pipeline has not run'
            return '{0}\n{1}'.format(summary, msg)

        for task_name, result in self.iteritems():
            task_name = _ResultSummary._pretty_format_name(task_name)
            result = '{step}: ({result}) {method_name}'.format(
                step=step, method_name=task_name, result=result)
            summary = '{0}\n{1}'.format(summary, result)
            step += 1

        return summary

    @staticmethod
    def _pretty_format_name(name):
        formatted = name.replace('/', ' -> ')
        formatted = re.sub(r'([a-z]+)([A-Z])',r'\1 \2', formatted)
        formatted = ' '.join(word[0].upper() + word[1:]
                             for word in formatted.split())

        return formatted
