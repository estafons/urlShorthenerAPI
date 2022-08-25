from shorty.helper import getEnvVars
import requests
import json


def bitly(longURL: str):
    envVars = getEnvVars(TOKEN='BITLY_TOKEN', GROUPGUID='GROUPGUID')
    headers = {
        'Authorization': envVars['TOKEN'],
        'Content-Type': 'application/json',
    }
    data = json.dumps({"long_url": longURL, "domain": "bit.ly",
                      "group_guid": envVars['GROUPGUID']})
    response = requests.post(
                            'https://api-ssl.bitly.com/v4/shorten',
                            headers=headers, data=data)

    if 199 < response.status_code < 300:            # request Success
        return response.json(), response.status_code
    else:                                           # request failure
        return response.text, response.status_code


def tinyURL(longURL: str):
    requestURL = "https://tinyurl.com/api-create.php"
    query = {'url': longURL}
    response = requests.get(requestURL, params=query)
    if 199 < response.status_code < 300:            # Success
        responseJson = {'link': response.text}
        return responseJson, response.status_code
    else:                                           # Failure
        return response.text, response.status_code


def providersInterface(provider):
    '''
    takes as input the name of the prefered provider.
    returns the functions of both providers as a dict.
    first one is the primary choice. (3.7+ python dicts are ordered)
    easily extensible to swap providers or add new.
    '''
    #  Initialization

    providers_sorted = {}
    providers = {'bitly': bitly, 'tinyurl': tinyURL}

    # Sort providers

    providers_sorted[provider] = providers[provider]
    for provider_name, provider_function in providers.items():
        if provider_name not in providers_sorted:
            providers_sorted[provider_name] = provider_function

    return providers_sorted
