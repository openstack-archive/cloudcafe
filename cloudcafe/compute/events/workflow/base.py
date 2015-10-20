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

from collections import namedtuple

from cafe.common.reporting import cclogging


class Error(object):
    """Error datatype for use in workflows.

    Data container for error information related to workflows. String
    representation of Error object is used in workflow summaries.

    Attributes:
        method (str): Name of the method producing the error.

        expected (str): Expected value or description of the
            unfulfilled expectation.

        actual (str): Actual value or description of the actual
            behavior that caused the error.

        message (Optional[str]): Free-form description of the error.
    """
    def __init__(self, expected, actual, message=None):
        self.message = message
        self.expected = expected
        self.actual = actual

    def summary(self):
        """Generate a summary of the error.

        Returns:
            str: Error summary.
        """
        msg = '(Expected: {expected} / Actual: {actual})'.format(
            expected=self.expected, actual=self.actual)
        if self.message:
            msg = '{0} -- {1}'.format(msg, self.message)

        return msg

    def __repr__(self):
        """String representation of the Error object.

        Note:
            This representation is used by the WorkflowRunner to produce
            summaries.

        Returns:
            str: String representation of the Error object.
        """
        msg = '{summary}'.format(summary=self.summary())

        return msg


class Result(object):
    """Result datatype for use in workflows.

    Data container for result information related to workflows. String
    representation of Result object is used in workflow summaries.

    Attributes:
        method_name (str): Name of the method producing the result.

        error (Optional[Error]): Error object corresponding to a
            Failure result.

        success (bool): True if result is Success, False otherwise.

        skipped (Optional[bool]): Indicate if the Result corresponds to
            a skipped step in a workflow.
    """
    def __init__(self, method_name, error=None, skipped=False):
        self.method_name = method_name
        self.error = error
        self.success = False if error or skipped else True
        self.skipped = skipped

    def __repr__(self, indent_str=''):
        """String representation of the Result object.

        Note:
            This representation is used by the WorkflowRunner to produce
            summaries.

        Args:
            indent_str (Optional[str]): Prefix string used to indent
                lines in a printed workflow summary.

        Returns:
            str: String representation of the Result object.
        """
        if self.method_name[0] == '_':
            self.method_name = self.method_name[1:]
        method_name_str = self.method_name.replace('_', ' ')
        method_name_str = method_name_str[0].upper() + method_name_str[1:]
        if self.success:
            msg = '(Success) {}'.format(method_name_str)
        elif self.skipped:
            msg = '(Skipped) {}'.format(method_name_str)
        else:
            msg = '(Failure) {0} -- {1}'.format(method_name_str, self.error)

        return '{indent}{message}'.format(indent=indent_str, message=msg)


class WorkflowStatus(object):
    """Status string for a workflow."""
    SUCCESS = 'Success'
    FAILURE = 'Failure'
    SKIPPED = 'Skipped'


class Workflow(object):
    """Workflow datatype for use in workflows.

    Data container for workflow information. String representation of
    Workflow object is used in workflow summaries.

    Attributes:
        workflow_name (str): Name (description) of the workflow.

        results (list): List of result objects. These objects can be of
            any type as long as they provide a 'success' attribute and
            a __repr__(indent_str='') method. Currently, this includes
            Result, and Workflow.

        skipped (Optional[bool]): Indicate if the Workflow corresponds
            to a skipped step in containing workflow.

        success (bool): True if all results are Success, False otherwise.

        status (str): Status of the workflow based on the provided input.
    """
    _parallel = False

    def __init__(self, workflow_name, results, skipped=False):
        self.workflow_name = workflow_name
        self.results = results
        self.skipped = skipped
        self.success = self._process_results(results, skipped)
        self.status = self._process_status(skipped, self.success)

    @staticmethod
    def _process_results(results, skipped):
        """Determine success or failure of the workflow.

        Returns:
            bool: True if successful, False otherwise.
        """
        if skipped:
            return False

        for result in results:
            if not result.success:
                return False

        return True

    @staticmethod
    def _process_status(skipped, success):
        """Determine status of the workflow.

        Returns:
            str: Status string chosen from WorkflowStatus types.
        """
        if skipped:
            return WorkflowStatus.SKIPPED
        elif success is False:
            return WorkflowStatus.FAILURE
        else:
            return WorkflowStatus.SUCCESS

    def __repr__(self, indent_str=''):
        """String representation of the Workflow object.

        Note:
            This representation is used by the WorkflowRunner to produce
            summaries.

        Args:
            indent_str (Optional[str]): Prefix string used to indent
                lines in a printed workflow summary.

        Returns:
            str: String representation of the Workflow object.
        """
        _indent_level = '  '

        heading = 'Parallel Workflow:' if self._parallel else 'Workflow:'
        base = '{indent}({status}) {heading} {name}'.format(
            indent=indent_str, status=self.status,
            heading=heading, name=self.workflow_name)

        results = []
        for result in self.results:
            if self._parallel:
                new_indent_str = '{0}|| '.format(indent_str + _indent_level)
            else:
                new_indent_str = indent_str + _indent_level
            results.append(result.__repr__(new_indent_str))

        result = '\n'.join(results)

        msg = '{base}\n{results}'.format(
            base=base, results=result)

        return msg


class ParallelWorkflow(Workflow):
    """Parallel Workflow datatype for use in workflows.

    Data container for parallel workflow information. String
    representation of ParallelWorkflow object is used in
    workflow summaries.

    Note:
        This class is identical in functionality to the Workflow class,
        with the exception of the string representation.
    """
    _parallel = True


ParallelTasks = namedtuple('ParallelTasks', ['tasks', 'name'])
WorkflowOutput = namedtuple('WorkflowOutput', ['result', 'data'])


class WorkflowRunner(object):
    """Runner containing the logic for executing workflows.

    The class is the workhorse for workflow processing. Each instance
    is initialized with a description and a list of tasks to
    perform, and then processes the tasks and produces results
    when the run method is called. Results are logged and returned
    as a data structure containing a comprehensive summary of the
    steps and corresponding results of the workflow.

    Attributes:
        description (str): Description of the workflow's purpose.

        tasks (list): List of tasks to perform. Supported types are:
            1. Any method accepting a single argument and returning a
               single item.
            2. A ParallelTasks object.
            3. A WorkflowRunner object.

        parallel (Optional[bool]): Set the result processing mode
            of the instance. Process results in parallel if True,
            and serially otherwise. Note that tasks are not
            currently run in parallel; this setting only affects
            the processing of task output and flow logic.
    """
    def __init__(self, description, tasks, parallel=False):
        self.description = description
        self.tasks = tasks
        self.parallel = parallel

    def add_task(self, task):
        """Add task to the end of the current workflow

        Args:
            task: Any supported task type (see class description for
                full list of supported types)
        """
        self.tasks.append(task)

    def run(self, data=None, _skip=False, log_result=True):
        """Run the workflow with provided data.

        Args:
            data: Input data to be processed by the workflow. Data can
                be of any type.

            _skip (Optional[bool]): Skip running tasks in this workflow.
                This argument is used to process nested workflows, and
                should not be needed outside of the WorkflowRunner's
                internal processing.

            log_result (Optional[bool]): Log run results if True.
        """
        results, data_out = self._run_tasks(
            tasks=self.tasks, data=data, parallel=self.parallel, skip=_skip)

        result = self._bundle_results(
            results=results, description=self.description,
            parallel=self.parallel, skipped=_skip)

        # TODO (levi_b): Decouple logging from CloudCafe
        if log_result:
            _log = cclogging.getLogger()
            _log.info(self._format_log_output(
                result=result, input_data=data, output_data=data_out))

        return WorkflowOutput(result=result, data=data_out)

    @staticmethod
    def _run_tasks(tasks, data, parallel, skip):
        """Run the tasks and return results and processed data."""
        results = []

        for task in tasks:
            task = WorkflowRunner._preprocess_task(task)

            if isinstance(task, WorkflowRunner):
                result, data_out = task.run(
                    data=data, _skip=skip, log_result=False)
            else:
                result, data_out = WorkflowRunner._process_task(
                    task=task, data=data, skip=skip)

            if not parallel:
                data = data_out

            results.append(result)

            if not (result.success or parallel):
                skip = True

        return results, data

    @staticmethod
    def _preprocess_task(task):
        """Convert ParallelTask into WorkflowRunner."""
        if isinstance(task, ParallelTasks):
            task = WorkflowRunner(
                description=task.name, tasks=task.tasks, parallel=True)

        return task

    @staticmethod
    def _process_task(task, data, skip):
        """Process a task."""
        name = task.__name__

        if skip:
            result = Result(method_name=name, skipped=True)
            data_out = None
        else:
            try:
                task_result = task(data)
            except Exception as e:
                task_result = Error(
                    expected='Results of task "{0}"'.format(name),
                    actual='Exception raised while '
                           'processing "{0}"'.format(name),
                    message='{0}: {1}'.format(type(e).__name__, e))
            result, data_out = WorkflowRunner._process_task_result(
                task_name=name, task_result=task_result)

        return result, data_out

    @staticmethod
    def _process_task_result(task_name, task_result):
        """Handle possible task output cases."""
        if isinstance(task_result, Error):
            result = Result(method_name=task_name, error=task_result)
            data_out = None
        else:
            result = Result(method_name=task_name)
            data_out = task_result

        return result, data_out

    @staticmethod
    def _bundle_results(results, description, parallel, skipped):
        """Bundle results into appropriate Workflow type."""
        if parallel:
            return ParallelWorkflow(
                workflow_name=description, results=results, skipped=skipped)
        else:
            return Workflow(
                workflow_name=description, results=results, skipped=skipped)

    @staticmethod
    def _format_log_output(result, input_data, output_data):
        """Format result output for logging."""
        sep = '=' * 80
        output = ('\n{sep}\n---Result---\n{result}\n'
                  '---Input Data---\n{input_data}\n'
                  '---Output Data---\n{output_data}\n{sep}')

        return output.format(result=result, input_data=input_data,
                             output_data=output_data, sep=sep)


class ValidatorBase(object):
    """Base class for validator classes.

    A validator class consists of a list of workflow tasks that
    define a validation, and a workflow method that bundles the
    tasks into a WorkflowRunner instance for easy access.
    """
    tasks = None

    @classmethod
    def workflow(cls):
        raise NotImplementedError(
            'Must override to return a WorkflowRunner in child class')
