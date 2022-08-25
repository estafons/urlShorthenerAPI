from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR
from flask import Blueprint, jsonify, request
from shorty.shorturl import providersInterface
from shorty.helper import getQueryParameters, error_response_creator

api = Blueprint('api', __name__)


@api.route('/shortlinks', methods=['POST'])
def create_shortlink():

    # initialization
    status_codes = {}

    # request's parameters #

    params = request.args
    try:
        longURL, provider_choice = getQueryParameters(params)
    except ValueError as e:
        return e.args[0], BAD_REQUEST

    # primary and secondary provider #

    providers = providersInterface(provider_choice)

    # get shortened URL #

    # Request from primary provider
    for order, provider in providers.items():
        try:
            responseJson, status_code = provider(longURL)
        except Exception:
            return "Internal Server Error", INTERNAL_SERVER_ERROR
        if 199 < status_code < 300:   # if response success return json
            shortURL = responseJson['link']
            return jsonify({'url': longURL, 'link': shortURL})
        else:
            status_codes[order] = status_code

        # If failed request from secondary provider
    return error_response_creator(status_codes)
