#!/usr/bin/env python
# -*- coding: utf-8 -*-

import falcon
from app import config
from app import log

logger = log.get_logger()

ALLOWED_ORIGINS = config.ALLOWED_ORIGINS
ALLOWED_HEADERS = config.ALLOWED_HEADERS
ALLOWED_METHODS = config.ALLOWED_METHODS


class CorsMiddleware(object):

    def process_request(self, request, response):
        origin = request.get_header('Origin')

        logger.info("origin: {}".format(origin))

        if origin is None:
            raise falcon.HTTPForbidden(title=falcon.HTTP_403, description='Origin domain is not allow')

        if origin not in ALLOWED_ORIGINS.split(','):
            raise falcon.HTTPForbidden(title=falcon.HTTP_403, description='Origin domain is not allow')

        response.set_header('Access-Control-Allow-Origin', origin)
        response.set_header('Access-Control-Allow-Headers', ALLOWED_HEADERS)
        response.set_header('Access-Control-Allow-Credentials', 'true')
        response.set_header('Access-Control-Allow-Methods', ALLOWED_METHODS)
