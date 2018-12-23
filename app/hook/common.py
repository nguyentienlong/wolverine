"""Hooks Submodule"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import time
import falcon

from app import log
from app import config
from firebase_admin import auth

logger = log.get_logger()


def api_key(req, resp, resource, params):
    # track client by api_key from request header
    key = req.get_header('Api-Key', None)
    logger.info('request from client with api key: {}'.format(key))
    if key is None:
        raise falcon.HTTPForbidden(
            title='Error',
            description='Api-Key is required')

    if key not in config.ALLOWED_API_KEYS:
        raise falcon.HTTPForbidden(
            title='Error',
            description='Invalid Api-Key')


def is_admin(req, resp, resource, params):
    # Good place to check the user role
    logger.info(req.context['auth_user'])


def authenticate(req, resp, resource, params):
    auth_value = req.get_header('Authorization', None)

    if auth_value is None \
            or len(auth_value.split(' ')) != 2 \
            or not validate_token(req, auth_value.split(' ')[1]):
        raise falcon.HTTPUnauthorized(title=falcon.HTTP_401, description='Unauthorized')


def validate_token(req, token):
    try:
        decoded_token = auth.verify_id_token(token)
        logger.info(decoded_token)
        # check if user email verified or not
        if decoded_token['firebase']['sign_in_provider'] == 'password':
            if decoded_token['email_verified'] is False:
                logger.info('User email not verified')
                return False

        req.context['auth_user'] = decoded_token
    except ValueError as e:
        logger.error(e)
        return False
    if not decoded_token:
        return False
    return True


def parse_request_body(req, resp, params):
    def _is_json_type(content_type):
        return content_type == 'application/json'

    if req.method.upper() in ['POST', 'PUT', 'PATCH']:
        if not _is_json_type(req.content_type):
            raise falcon.HTTPBadRequest(
                title='Invalid Content Type',
                description='JSON required. '
                            'Invalid Content-Type {}'.format(req.content_type)
            )

    if req.content_length in (None, 0):
        raise falcon.HTTPBadRequest('Empty request body',
                                    'A valid JSON document is required.')
    data = req.stream.read()
    if not data:
        raise falcon.HTTPBadRequest('Empty request body',
                                    'A valid JSON document is required.')

    data = json.loads(data.decode('utf-8'))

    req.params['body'] = data
