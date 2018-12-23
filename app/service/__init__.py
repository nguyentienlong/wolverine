#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
from app.service.booking import free_booking_handler, premium_booking_handler
from app.service.search import search_handler
from app.service.history.owner_booking_history import *
from app.service.history.renter_booking_history import *


class BookingServiceFactory(object):
    @staticmethod
    def create_state_handler(service_type, status):
        if service_type not in ['free', 'premium']:
            raise Exception(
                "service_type {} is not valid,"
                "only support [free, premium]".format(service_type))

        state_handler = getattr(
            importlib.import_module(
                "app.service.booking.{}_booking_handler".
                format(service_type).lower()),
            (status.title()+'StateHandler').replace('_', '')
        )

        return state_handler()


class BookingHistoryServiceFactory(object):
    @staticmethod
    def create_booking_history_service(user_type):
        if user_type == AbstractBookingHistory.OWNER:
            return OwnerBookingHistory()
        elif user_type == AbstractBookingHistory.RENTER:
            return RenterBookingHistory()

        raise Exception("{} type is invalid".format(user_type))
