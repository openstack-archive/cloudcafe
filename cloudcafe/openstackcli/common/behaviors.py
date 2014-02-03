from cafe.engine.behaviors import BaseBehavior


class OpenstackCLI_BehaviorError(Exception):
    pass


class OpenstackCLI_BaseBehavior(BaseBehavior):

    _default_exception = OpenstackCLI_BehaviorError

    @staticmethod
    def is_parse_error(resp):
        if resp.entity is None:
            return "Unable to parse CLI response"

    @staticmethod
    def is_cli_error(resp):
        if resp.standard_error[-1].startswith("ERROR"):
            return "CLI returned an error message"

    @staticmethod
    def is_process_error(resp):
        if resp.return_code is not 0:
            return "CLI process returned an error code"

    @classmethod
    def raise_if(cls, check, msg):
        if check:
            raise cls._default_exception(msg)

    @classmethod
    def raise_on_error(cls, resp, msg=None):
        errors = [
            cls.is_parse_error(resp),
            cls.is_cli_error(resp),
            cls.is_process_error(resp)]
        errors = [e for e in errors if e is not None]
        msg = msg or "ERROR: {0}".format(
            " : ".join(["{0}".format(e) for e in errors]))
        cls.raise_if(errors, msg)
