#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" EmailSubscription Model """

from mongoengine import *


class EmailSubscription(Document):
    email = StringField(unique=True)
    ip = DictField()
    create_date = DateTimeField()
