import validators
import os
from http.client import BAD_GATEWAY, INTERNAL_SERVER_ERROR


def getQueryParameters(params):
    '''

    Parameters
    -----------
    params: MultiDict
        request's query parameters

    Returns
    ------------
    url: str
        url to be shortened
    provider: str
        specified provider to prefer if possible

    Raises
    ------------
    ValueError
        if input parameters are not valid

    '''
    print(password)
    if params.get('url'):
        url = params.get('url')
    else:
        raise ValueError("Url Not Found")
    if params.get('provider'):
        provider = params.get('provider')
        if provider not in ['bitly', 'tinyurl']:
            raise ValueError("Invalid Provider")
    else:
        provider = 'bitly'
    if validators.url(url.strip()):
        return url, provider
    else:
        raise ValueError("Invalid Url")


def getEnvVars(**kwargs):
    '''

    Parameters
    -------------
    key-value pairs
    keys: will be used for drawing variables from return dict
    values: name of the enviornment variable

    Returns
    --------------
    envVars: dict

    Example
    -------------
    Get environment variable with name exampleEnvVarName and value 'test'

    assert getEnvVars(exampleKey='exampleEnvVarName')['exampleKey'] == 'test'
    True

    '''
    try:
        envVars = {key: os.environ[val] for key, val in
                   zip(kwargs.keys(), kwargs.values())}
    except KeyError:
        print("Enviroment variables not found.")
        # here should return internal server error
        raise KeyError("Enviroment variables not found.")

    return envVars


def error_response_creator(status_codes: dict):
    '''
    return error response based on third party api response codes.
    ready to adapt in case of adding new third party apis.
    '''
    for status_code in status_codes.values():
        if 399 < status_code < 500:             # at least one with error
            return "Internal Server Error", INTERNAL_SERVER_ERROR
    return "Bad Gateway", BAD_GATEWAY
