# -*- coding: utf-8 -*-

import falcon
import json

from app import log
from app import config

logger = log.get_logger()


# todo: remove this
class BaseResource(object):

    def on_get(self, req, resp):
        logger.info('Getting the resource')
        logger.info(config.LOG_LEVEL)
        resource = {
            'message': 'Welcome to vietvivu365 API! v1'
        }
        resp.body = json.dumps(resource)
        resp.status = falcon.HTTP_200
