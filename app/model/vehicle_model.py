#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import *
from datetime import datetime


class Model(Document):
    name = StringField(required=True, unique=True)
    popularity = IntField(default=None)
    created_date = IntField(default=datetime.now().timestamp())

    meta = {'collection': 'vehicle_model'}

