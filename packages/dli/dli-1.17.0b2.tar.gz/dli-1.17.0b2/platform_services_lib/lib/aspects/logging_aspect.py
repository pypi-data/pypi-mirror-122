#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import inspect


class LoggingAspect:

    @staticmethod
    def invoke_pre_call_aspects(wrapped_object, metadata):
        if getattr(wrapped_object, 'logger', None):
            try:
                wrapped_object.logger.debug('Client Function Called', extra=metadata)
            except Exception as e:
                wrapped_object.logger.exception(
                    'Error while invoking pre-call aspects.', e
                )

    @staticmethod
    def invoke_post_call_aspects(wrapped, metadata):
        pass

    @staticmethod
    def invoke_after_exception_aspects(wrapped_object, metadata, exception):
        if getattr(wrapped_object, 'logger', None):
            # If the object contains a `strict` boolean and it is set to
            # True, then print out the exception message and a full stack
            # trace.
            # DEFAULTED to True to match the current behaviour. This default
            # can be changed in a later release. When we change the default
            # we will have to update the tests to explicitly set strict to
            # True to maintain the previous test behaviour.
            if getattr(wrapped_object, 'strict', True):
                try:
                    wrapped_object.logger.exception(
                        'Unhandled Exception', stack_info=False, extra={
                            'locals': inspect.trace()[-1][0].f_locals
                        })
                except Exception as e:
                    wrapped_object.logger.exception(
                        'Error while invoking pre-call aspects.', e
                    )
            else:
                # Data scientists do not want to see stack dumps by default,
                # especially when we have a root cause that triggers secondary
                # exceptions.
                wrapped_object.logger.warning(
                    '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
                    '\nAn exception occurred so we are returning None.'
                    '\nTo see the exception and stack trace, please start '
                    'the session again with the parameter `strict=True`'
                    '\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
                )