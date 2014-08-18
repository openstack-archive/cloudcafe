# Stores all registered extensions in this module
extensions = []


class ResponseExtensionType(type):
    """Metaclass for auto-registering extensions.  Any new extension should
    use this as it's __metaclass__"""
    global extensions

    def __new__(cls, class_name, bases, attrs):
        extension = super(ResponseExtensionType, cls).__new__(
            cls, class_name, bases, attrs)

        if extension.__extends__:
            extensions.append(extension)
        return extension


class SimpleResponseExtension(object):
    """Simple extension that can be inherited and used to support and
    extension that adds one or multiple properties"""

    __metaclass__ = ResponseExtensionType
    __extends__ = []
    _sub_attr_map = {}

    @classmethod
    def extend(cls, obj, **kwargs):
        if obj.__class__.__name__ not in cls.__extends__:
            return obj

        for kw_name, attr_name in cls._sub_attr_map.items():
            setattr(obj, attr_name, kwargs.get(kw_name, None))
        return obj


class AttributeAggregatingResponseExtension(SimpleResponseExtension):
    """Aggregates all attributes that start with the class-defined
    prefix into a dictionary."""

    __extends__ = []
    _prefix = None
    _new_dict_attribute_name = None

    @classmethod
    def extend(cls, obj, **kwargs):
        if obj.__class__.__name__ not in cls.__extends__:
            return obj

        setattr(obj, cls._new_dict_attribute_name, dict())
        for key, val in kwargs.iteritems():
            if key.startswith(cls._prefix):
                obj.metadata[key[len(cls._prefix)::]] = val
        return obj
