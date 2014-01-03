from cafe.engine.models.base import BaseModel
from cafe.common.reporting import cclogging
from cloudcafe.openstackcli.common.models.extensions import extensions


class PRETTYTABLE_FRAME:
    HORIZONTAL_SEPERATOR = '-'
    VERTICAL_SEPERATOR = '|'
    INTERSECTION_CHARACTER = '+'


class PrettyTableDeserializationError(Exception):
    pass


class BaseExtensibleModel(BaseModel):

    def __init__(self, **kwargs):
        super(BaseExtensibleModel, self).__init__()
        global extensions
        for ext in extensions:
            if self.__class__.__name__ in ext.__extends__:
                self = ext().extend(self, **kwargs)


class BaseExtensibleListModel(list, BaseExtensibleModel):
    pass


class BasePrettyTableResponseModel(BaseExtensibleModel):
    _log = cclogging.getLogger(__name__)

    @classmethod
    def _listify(cls, prettytable_string):
        return [l for l in prettytable_string.split('\n') if len(l) > 0]

    @classmethod
    def _get_row_list(cls, prettytable_string):
        return cls._listify(prettytable_string)[3:-1]

    @classmethod
    def _get_column_count(cls, prettytable_string):
        top_line = cls._listify(prettytable_string)[0]
        intersection_count = top_line.count(
            PRETTYTABLE_FRAME.INTERSECTION_CHARACTER)
        return intersection_count - 1

    @classmethod
    def _get_column_widths(cls, prettytable_string):
        top_line = cls._listify(prettytable_string)[0]
        return [len(l) for l in top_line.split(
            PRETTYTABLE_FRAME.INTERSECTION_CHARACTER)[1:-1]]

    @classmethod
    def _get_row_count(cls, prettytable_string):
        #Remove headers and horizontal seperators
        lines = cls._get_row_list(prettytable_string)
        left_vertical = "".join([l[0] for l in lines])
        return left_vertical.count(PRETTYTABLE_FRAME.VERTICAL_SEPERATOR) - 1

    @classmethod
    def _get_headers(cls, prettytable_string):
        header_line = cls._listify(prettytable_string)[1]
        headers = [h.strip() for h in header_line.split(
            PRETTYTABLE_FRAME.VERTICAL_SEPERATOR) if len(h) > 0]

        if len(headers) != cls._get_column_count(prettytable_string):
            raise PrettyTableDeserializationError
        return headers

    @classmethod
    def _get_rows(cls, prettytable_string):
        rows = cls._get_row_list(prettytable_string)
        column_widths = cls._get_column_widths(prettytable_string)

        final_row_list = []
        for row in rows:
            #Split values out by column width
            row_items = []
            for length in column_widths:
                row = row.lstrip(PRETTYTABLE_FRAME.VERTICAL_SEPERATOR)
                row_items.append(row[:length])
                row = row[length:]

            #Strip leading and trailing whitepace for all values in row
            row = [r.strip() for r in row_items]
            final_row_list.append(row)

        return final_row_list

    @classmethod
    def _load_prettytable_string(
            cls, prettytable_string, expected_row_count=None,
            expected_column_count=None):

        def _check_count(count_type, expected, actual):
            if expected is not None and expected != actual:
                msg = (
                    "Expected {expected} {count_type}, but response had "
                    "{actual} {count_type}".format(
                        expected=expected, actual=actual,
                        count_type=count_type))
                raise PrettyTableDeserializationError(msg=msg)

        _check_count(
            'rows', expected_row_count,
            cls._get_row_count(prettytable_string))

        _check_count(
            'columns', expected_column_count,
            cls._get_column_count(prettytable_string))

        final_list = list()
        headers = cls._get_headers(prettytable_string)
        rows = cls._get_rows(prettytable_string)
        for row in rows:
            final_list.append(dict(zip(headers, row)))

        return tuple(final_list)

    @staticmethod
    def _apply_kwmap(kwmap, kwdict):
        for local_attr, response_attr in kwmap.items():
            kwdict[local_attr] = kwdict.pop(response_attr, None)
        return kwdict

    @classmethod
    def _property_value_table_to_dict(cls, prettytable_string):
        datatuple = cls._load_prettytable_string(prettytable_string)
        kwdict = {}

        for datadict in datatuple:
            kwdict[datadict['Property']] = datadict['Value'].strip() or None

        return kwdict

    @classmethod
    def deserialize(cls, serialized_str):
        cls._log = cclogging.getLogger(cclogging.get_object_namespace(cls))

        model_object = None
        deserialization_exception = None
        try:
            model_object = cls._prettytable_str_to_obj(serialized_str)
        except Exception as deserialization_exception:
            cls._log.exception(deserialization_exception)

        if deserialization_exception is not None:
            try:
                cls._log.debug(
                    "Deserialization Error: Attempted to deserialize string "
                    "as a prettytable:")
                cls._log.debug("\n{0}".format(serialized_str.decode(
                    encoding='UTF-8', errors='ignore')))
            except Exception as exception:
                cls._log.exception(exception)
                cls._log.warning(
                    "Unable to log information regarding the deserialization "
                    "exception")

        return model_object

    @classmethod
    def _prettytable_str_to_obj(cls, serialized_str):
        raise NotImplementedError


class BasePrettyTableResponseListModel(list, BasePrettyTableResponseModel):
    pass
