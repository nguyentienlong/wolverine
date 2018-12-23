#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import *
from datetime import datetime


class Booking(Document):
    # short id like as order id #XYZ123
    short_id = StringField(required=True)
    # who did the booking
    renter = StringField(required=True)
    # vehicle owner
    owner = StringField(required=True)
    # which vehicle
    vehicle = DictField(required=True)
    # steps [
    #   1.init(waiting for accept),
    #   2.accepted/rejected,
    #   3.deposited - when deposited, update reserved_date_time into vehicle
    #   4.received_vehicle
    #   5.canceled,
    #   6.done(give vehicle back)]
    # {
    #     "init": {
    #         "date_time": timestamp
    #     },
    #     "accepted": {
    #         "date_time": timestamp
    #     },
    #     "deposited": {
    #         "date_time": timestamp
    #     },
    #     "received_vehicle": {
    #         "date_time": timestamp
    #     },
    #     "done": {
    #         "date_time": timestamp
    #     }
    # }
    phases = DictField()
    # current phase [init, accepted or rejected, deposited, done ...]
    current_phase = StringField()

    # {
    #     "from": timestamp, date_time in utc
    #     "to": timestamp
    # }
    reserved_date_time = DictField(
        required=True,
        unique_with=['renter']
    )

    # store in utc-now
    created_date_time = IntField(
        required=True,
        default=datetime.now().timestamp()
    )

    # flag to check if owner gave feedback or not
    is_owner_gave_feedback = BooleanField(default=False)

    # flag to check is renter gave feedback to vehicle
    is_renter_gave_feedback = BooleanField(default=False)

    # price of booking
    total_price = FloatField(required=True)
