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


class SingleAttributeResponseExtension(object):
    """Simple extension that can be inherited and used to support a single
    response property"""
    __metaclass__ = ResponseExtensionType
    __extends__ = []
    key_name = None
    attr_name = None

    def extend(cls, obj, **kwargs):
        value = kwargs.get(cls.key_name)
        setattr(obj, cls.attr_name, value)
        return obj
