import inspect


def extract_metadata(
        dli_client, wrapped_object, func, arguments,
        keyword_args, class_fields_to_include=None
):
    # Get the user calling the function
    org_id, subject = _retrieve_user_details(dli_client)

    # This is to find out what the 'arg' names are.
    argspec = inspect.getfullargspec(func)
    args_dict = dict(zip(argspec.args, [wrapped_object, *arguments]))

    properties = _read_field_values(class_fields_to_include, wrapped_object)

    if not subject:
        if args_dict.get('api_key'):
            subject = '***' + args_dict.get('api_key')[:6]
        else:
            subject = 'UNKNOWN USER'

    return {
        'func': func,
        'subject': subject,
        'organisation_id': org_id,
        'arguments': args_dict,
        'kwargs': dict(keyword_args),
        'properties': properties
    }


def _retrieve_user_details(dli_client):
    org_id = None
    user_id = getattr(dli_client, 'api_key', '')[:6]
    try:
        org_id = dli_client.session.decoded_token.get('datalake').get('organisation_id')
        user_id = dli_client.session.decoded_token.get('sub', 'UNKNOWN USER')
    except AttributeError:
        pass

    return org_id, user_id


def _read_field_values(class_fields_to_include, wrapped_object):
    properties = {}
    for field in class_fields_to_include or []:
        property_name = field.split('.')[-1]
        property_value = wrapped_object
        for nested_field_name in field.split('.'):
            property_value = property_value.__dict__[nested_field_name]
        properties.update({property_name: property_value})
    return properties
