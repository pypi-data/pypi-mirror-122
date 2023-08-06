
class AnalyticsAspect:

    @staticmethod
    def invoke_pre_call_aspects(wrapped_object, metadata):
        pass

    def invoke_post_call_aspects(self, wrapped_object, metadata):
        if getattr(wrapped_object, '_analytics_handler', None):
            try:
                self._create_event(wrapped_object, metadata, status_code=200)
            except Exception as e:
                wrapped_object.logger.exception(
                    'Error while invoking post-call aspects.', e
                )

    def invoke_after_exception_aspects(self, wrapped_object, metadata, exception):
        if getattr(wrapped_object, '_analytics_handler', None):
            try:
                status_code = self._retrieve_status_code_from_exception(exception)
                self._create_event(wrapped_object, metadata, status_code=status_code)
            except Exception as e:
                wrapped_object.logger.exception(
                    'Error while invoking after-exception aspects.', e
                )

    @staticmethod
    def _create_event(dli_client, metadata, status_code):
        additional_properties = metadata.get('properties') or {}
        dli_client._analytics_handler.create_event(
            metadata['subject'], metadata['organisation_id'],
            metadata['func'].__qualname__.split('.')[0],
            metadata['func'].__name__,
            {**metadata['arguments'], **metadata['kwargs'], **additional_properties},
            result_status_code=status_code
        )

    @staticmethod
    def _retrieve_status_code_from_exception(exception):
        try:
            return exception.response.status_code
        except AttributeError:
            return 500
