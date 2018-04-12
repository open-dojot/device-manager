""" Assorted utils used throughout the service """
import base64
import json
import random
from flask import make_response, jsonify


def format_response(status, message=None):
    """ Utility helper to generate default status responses """
    if message:
        payload = {'message': message, 'status': status}
    elif 200 <= status < 300:
        payload = {'message': 'ok', 'status': status}
    else:
        payload = {'message': 'Request failed', 'status': status}

    return make_response(jsonify(payload), status)

def create_id():
    """ Generates a random hex id for managed entities """
    return '%05x' % random.randrange(16**6)

# from auth service
class HTTPRequestError(Exception):
    """ Exception that represents end of processing on any given request. """
    def __init__(self, error_code, message):
        super(HTTPRequestError, self).__init__()
        self.message = message
        self.error_code = error_code


def get_pagination(request):
    try:
        page = int(request.args.get('page_num', '1'))
        per_page = int(request.args.get('page_size', '20'))

        # sanity checks
        if page < 1:
            raise HTTPRequestError(400, "Page numbers must be greater than 1")
        if per_page < 1:
            raise HTTPRequestError(400, "At least one entry per page is mandatory")
        return page, per_page

    except TypeError:
        raise HTTPRequestError(400, "page_size and page_num must be integers")

def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += '=' * (4 - missing_padding)
    return base64.decodebytes(data.encode()).decode()
