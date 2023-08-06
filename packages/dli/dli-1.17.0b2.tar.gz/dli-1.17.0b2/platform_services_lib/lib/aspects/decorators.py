import inspect
from functools import wraps

from .analytics_aspect import AnalyticsAspect
from .logging_aspect import LoggingAspect
from ..services.dlc_attributes_dict import AttributesDict
from ..aspects import extract_metadata


def log_public_functions_calls_using(decorators, class_fields_to_log=None):
    if not class_fields_to_log:
        class_fields_to_log = []

    def decorate(cls):
        functions_to_exclude = inspect.getmembers(AttributesDict, inspect.isfunction)
        functions_to_decorate = [
            func for func in inspect.getmembers(cls, inspect.isfunction)
            if func not in functions_to_exclude and not func[0].startswith('_') and not func[0].startswith('__')
        ]
        for function_meta in functions_to_decorate:
            function_name = function_meta[0]
            for decorator in decorators:
                setattr(
                    cls,
                    function_name,
                    decorator(getattr(cls, function_name),
                              class_fields_to_include=class_fields_to_log)
                )
        return cls
    return decorate


def analytics_decorator(function, class_fields_to_include):
    aspect = AnalyticsAspect()

    @wraps(function)
    def function_wrapper(target, *args, **kwargs):
        metadata = extract_metadata(
            target._client, target, function, args, kwargs, class_fields_to_include
        )

        aspect.invoke_pre_call_aspects(target._client, metadata)
        try:
            result = function(target, *args, **kwargs)
        except TypeError as t:
            # its a pity to put this here, but we need to hijack TypeError for UnstructuredDatasetModel
            # we can't use hasattr, since the TypeError hijack will return something!
            # N.B. if you need to see the real cause, comment out the _type_exception_handler of the class.
            if "_type_exception_handler" in dir(target):
                target._type_exception_handler(t, function, args, kwargs)
                return
            else:
                aspect.invoke_after_exception_aspects(target._client, metadata, t)
                raise t

        except Exception as e:
            aspect.invoke_after_exception_aspects(target._client, metadata, e)
            raise e
        aspect.invoke_post_call_aspects(target._client, metadata)
        return result

    return function_wrapper


def logging_decorator(function, class_fields_to_include):
    aspect = LoggingAspect()

    @wraps(function)
    def function_wrapper(target, *args, **kwargs):
        metadata = extract_metadata(
            target._client, target, function, args, kwargs, class_fields_to_include
        )
        aspect.invoke_pre_call_aspects(target._client, metadata)
        try:
            result = function(target, *args, **kwargs)
        except Exception as e:
            aspect.invoke_after_exception_aspects(target._client, metadata, e)
            raise e
        aspect.invoke_post_call_aspects(target._client, metadata)
        return result

    return function_wrapper

