#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import *
from datetime import datetime


class Brand(Document):
    name = StringField(required=True)
    popularity = IntField(default=None)
    manufacturer = StringField(required=True, unique_with=['name'])
    created_date = IntField(default=datetime.now().timestamp())

    meta = {'collection': 'vehicle_brand'}
