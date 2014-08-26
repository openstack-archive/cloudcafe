from time import time, sleep
from math import ceil
from cafe.engine.behaviors import BaseBehavior


class StatusProgressionClassUsageError(Exception):
    pass


class StatusProgressionError(Exception):
    pass


class StatusPollError(Exception):
    pass


class StatusProgressionVerifier(BaseBehavior):
    """ Verifies a defined, expected progression of the string value returned
    by repeated calls to status_call().
    """

    def __init__(
            self, model_type, model_id, status_call,
            *status_call_args, **status_call_kwargs):

        super(StatusProgressionVerifier, self).__init__()
        self.model_type = model_type
        self.model_id = model_id
        self.status_call = status_call
        self.status_call_args = status_call_args
        self.status_call_kwargs = status_call_kwargs
        self._state_list = []
        self.global_timeout = None

    def set_global_state_properties(self, timeout=None):
        """If the global timeout is set, all individual states without timeouts
        will be timed as part of the global timeout, along with the entire
        progression verification.  Individual state timeouts will still be
        honored unless it would be waiting longer than the global timeout.
        """
        if timeout is not None:
            self.global_timeout = timeout

    def add_state(
            self, expected_statuses=None, acceptable_statuses=None,
            error_statuses=None, timeout=None, poll_rate=None,
            poll_failure_retry_limit=0):

        self._state_list.append(
            (expected_statuses or [],
             acceptable_statuses or [],
             error_statuses or [],
             timeout,
             poll_rate,
             poll_failure_retry_limit))

    def start(self):
        """Once start() is called, the class will call status_call() in a loop,
        each time comparing the resulting status string to three lists defined
        by the initial state.
        If the current status is in either the expected_statuses or
        acceptable_statuses list, the state machine will move onto the next
        state (which defines new values for the three lists).
        If the current status is in the error_statuses lists or no relevant
        status is observed before timeout seconds (as defined for the
        current state) have elapsed, a StatusProgressionError is raised with
        an appropriate error message.
        """
        global_endtime = None
        if self.global_timeout:
            global_endtime = time() + self.global_timeout

        # State loop
        for expected_statuses, acceptable_statuses, error_statuses, timeout, \
                poll_rate, poll_failure_retry_limit in self._state_list:

            self._log.debug(
                "\nCurrently watching {model_type} {model_id}\n"
                "Continuing if status in : {expected}\n"
                "Bypassing if status in  : {acceptable}\n"
                "Error if status in      : {error}\n"
                "Polling every {poll_rate} seconds for "
                "{timeout} seconds.\n".format(
                    model_type=self.model_type, model_id=self.model_id,
                    expected=expected_statuses, acceptable=acceptable_statuses,
                    error=error_statuses, poll_rate=poll_rate,
                    timeout=timeout))

            current_status = None
            poll_failure_retries = 0

            # Timeout calculation
            state_timeout = None
            state_endtime = None
            if timeout and global_endtime is None:
                state_endtime = time() + timeout
                state_timeout = timeout
            elif global_endtime is not None:
                state_endtime = global_endtime
                state_timeout = state_endtime - time()
            else:
                raise StatusProgressionClassUsageError(
                    "A timeout could not be found for the current state. "
                    "Please either set a global timeout via "
                    "set_global_state_properties, or set an explicit timeout "
                    "for this state.")

            if global_endtime is not None and global_endtime < state_endtime:
                    state_endtime = global_endtime
            state_timeout = ceil(state_timeout)
            state_endtime = ceil(state_endtime)

            # State watch loop
            while time() < state_endtime:

                # Attempt to get the latest status, retry status_call() up to
                # poll_failure_retry_limit times if neccessary
                try:
                    current_status = self.status_call(
                        *self.status_call_args, **self.status_call_kwargs)
                except Exception as exception:
                    if poll_failure_retries >= poll_failure_retry_limit:
                        msg = (
                            "status_call() failed after {retries} retries."
                            " Unable to retrieve status.".format(
                                retries=poll_failure_retries))
                        if poll_failure_retry_limit > 0:
                            msg = (
                                "status_call() failed and was not allowed "
                                "any retries")
                        self._log.error(exception)
                        self._log.error(msg)
                        raise StatusPollError(msg)
                    else:
                        poll_failure_retries += 1
                        msg = (
                            "status_call() for {model_type} '{model_id}' "
                            "failed.  Retrying".format(
                                model_type=self.model_type,
                                model_id=self.model_id))
                        self._log.warning(msg)

                # Log current status
                self._log.debug(
                    "Current {model_type} {model_id} status: "
                    "'{current_status}'".format(
                        model_type=self.model_type, model_id=self.model_id,
                        current_status=current_status))

                # Fast fail if status is in the state's error_statuses list
                if current_status in error_statuses:
                    msg = (
                        "status_call() returned a status in the state's "
                        "error_statuses list: '{current_status}'".format(
                            current_status=current_status))
                    self._log.error(msg)
                    raise StatusProgressionError(msg)

                # State Logic
                if current_status in expected_statuses:
                    self._log.debug(
                        "Current status '{current_status}' is an expected "
                        "status. Continuing to next state.".format(
                            current_status=current_status))
                    break

                if current_status in acceptable_statuses:
                    self._log.debug(
                        "An acceptable status '{current_status}' was observed "
                        "before any expected statuses '{expected_statuses}'. "
                        "Bypassing this state and continuing to next state."
                        .format(
                            current_status=current_status,
                            expected_statuses=expected_statuses))
                    break

                sleep(poll_rate)

            # Timeout reached
            else:
                msg = (
                    "\nNo expected statuses or acceptable statuses where "
                    "observed withing the alloted {timeout} second timeout.\n"
                    "Last observed status: {current_status}\n"
                    "expected statuses: {expected_statuses}\n"
                    "acceptable statuses: {acceptable_statuses}\n".format(
                        timeout=state_timeout,
                        current_status=current_status,
                        expected_statuses=expected_statuses,
                        acceptable_statuses=acceptable_statuses))

                self._log.error(msg)
                raise StatusProgressionError(msg)
