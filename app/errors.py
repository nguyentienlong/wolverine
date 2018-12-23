#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from app import config
from app import log
import falcon

logger = log.get_logger()


class Handler(object):
    @staticmethod
    def handle(exception, req, res, error):
        logger.exception(exception)
        # don't show actually error message on prod
        if config.APP_ENV == 'prod':
            raise falcon.HTTPBadRequest(
                title=falcon.HTTP_400,
                description=falcon.HTTP_BAD_REQUEST
            )

        # handle not derived class of HTTPError
        if not hasattr(exception, 'status'):
            res.status = falcon.HTTP_BAD_REQUEST
            res.body = json.dumps(
                {
                    'status': 'failed',
                    'message': str(exception)
                }
            )
            return

        res.status = exception.status
        meta = {
            'status':  'failed',
            'message': exception.title
        }
        if exception.description:
            meta['description'] = exception.description
        res.body = json.dumps(meta)
