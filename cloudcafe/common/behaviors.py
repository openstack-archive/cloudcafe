from time import time, sleep


class StatusProgressionError(Exception):
    pass


class StatusProgressionVerifier(object):
    """ Verifies a defined progression of the string returned by status_call().
    Once start() is called, the class will loop through the defined states.
    Each state will have a status it is watching for, a timeout defining how
    long to wait for the status before declaring failure, a poll_rate to 
    control how often the status_call() is made, and a boolean value 
    'transient' that controls wether or not to declare failure if the status
    is not observed.  (If transient == True, the status is watched for but 
    won't cause failure if not observed."""
    def __init__(
            self, model_type, model_id, status_call,
            *status_call_args, **status_call_kwargs):
        self.model_type = model_type
        self.model_id = model_id
        self.status_call = status_call
        self.status_call_args = status_call_args
        self.status_call_kwargs = status_call_kwargs
        self._state_list = []

    def add_state(
            self, expected_status, timeout, poll_rate, poll_failure_retries=1,
            transient=False):
        """Append a new watch status to the ProgressionVerifier
        expected_status should be a string matching the expected response
        from a successful status_call()

        timeout is the length of time in seconds to wait for the 
        expected_status to be observed before declaring failure, or continuing
        to the next status if transient==True

        poll_rate is the time in seconds to wait between calls to poll_rate.

        poll_failure_retries is the amount of times status_call() should be 
        retried if it raises an exception.

        Note: The first state added to the StatusProgressionVerifier will be
        the starting state.  If you have a situation where the starting status
        is very short lived, make sure to set transient=True for the first
        state.
        """
        self._state_list.append(
            (expected_status, timeout, poll_rate, transient))

    def start(self):
        current_state = 0
        for expected_status, transient, timeout, poll_rate in self._state_list:

            self._log.debug(
                "Current {model_type} {model_id} status progression state:\n"
                "expected_status: {expected_status}\n"
                "transient: {transient}\n"
                "timeout: {timeout},\n"
                "poll_rate: {poll_rate}".format(
                    model_type=self.model_type, model_id=self.model_id,
                    expected_status=expected_status, transient=transient,
                    timeout=timeout, poll_rate=poll_rate))

            #Try and set the next_status if there is one.
            next_status = None
            try:
                next_status, _, _, _ = self._state_list[current_state+1]
            except:
                pass

            endtime = time() + timeout
            current_status = None
            while time() < endtime:
                current_status = self.status_call(
                    *self.status_call_args, **self.status_call_kwargs)

                self._log.debug(
                    "Current {model_type} {model_id} status: "
                    "'{current_status}'".format(
                        model_type=self.model_type, model_id=self.model_id,
                        current_status=current_status))

                if expected_status == current_status:
                    current_state += 1
                    self._log.debug(
                        "Current {model_type} {model_id} status matches "
                        "expected status '{expected_status}'".format(
                            model_type=self.model_type, model_id=self.model_id,
                            expected_status=expected_status))
                    break

                elif transient and (current_status == next_status):
                    self._log.debug(
                        "Next status '{next_status}' found while searching for"
                        " transient status '{expected_status}'".format(
                            next_status=next_status,
                            expected_status=expected_status))
                    break
                sleep(poll_rate)

            else:
                if transient:
                    self._log.debug(
                        "Neither the transient status '{expected_status}' nor "
                        "the next status '{next_status}' where found, "
                        "continuing to next status search.".format(
                            expected_status=expected_status,
                            next_status=next_status))
                    continue

                else:
                    msg = (
                        "{model_type} {model_id} did not progress to the "
                        "'{expected_status}' status in the alloted time of "
                        "{timeout} seconds. Last observed status was "
                        "'{last_observed}'".format(
                            model_type=self.model_type, model_id=self.model_id,
                            expected_status=expected_status, timeout=timeout,
                            last_observed=current_status))

                    self._log.error(msg)
                    raise StatusProgressionError(msg)
