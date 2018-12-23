#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import *
from datetime import datetime


class Manufacturer(Document):
    name = StringField(required=True, unique=True)
    # start from 1,2,3. 1-is the most popularity, and following
    popularity = IntField(default=None)
    created_date = IntField(default=datetime.now().timestamp())

    meta = {'collection': 'vehicle_manufacturer'}
