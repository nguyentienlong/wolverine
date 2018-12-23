#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import AbstractStateHandler

from app import log

logger = log.get_logger()
SERVICE_TYPE = 'premium'

state_order = {
    # renter book a vehicle
    AbstractStateHandler.BOOKING_PHASE_INITIALIZED: 1,

    # owner accepted the deal with renter
    AbstractStateHandler.BOOKING_PHASE_ACCEPTED: 2,

    # owner rejected the deal after discussion
    AbstractStateHandler.BOOKING_PHASE_REJECTED: 2,

    # owner accept request from renter
    AbstractStateHandler.BOOKING_PHASE_DEPOSITED: 3,

    # pickup vehicle (or vehicle delivered)
    AbstractStateHandler.BOOKING_PHASE_PICKED_UP: 4,

    # client cancel after booking initialized, owner cancel after accepting
    AbstractStateHandler.BOOKING_PHASE_CANCELED: 5,

    # renter gave vehicle back to owner, both side give feed back to each other
    AbstractStateHandler.BOOKING_PHASE_DONE: 6
}


class InitializedStateHandler(AbstractStateHandler):
    def handle(self, booking_id, status):
        raise Exception('Not implemented')


class AcceptedStateHandler(AbstractStateHandler):
    def handle(self, booking_id, status):
        raise Exception('Not implemented')


class RejectedStateHandler(AbstractStateHandler):
    def handle(self, booking_id, status):
        raise Exception('Not implemented')


class CanceledStateHandler(AbstractStateHandler):
    def handle(self, booking_id, status):
        raise Exception('Not implemented')


class DepositedStateHandler(AbstractStateHandler):
    def handle(self, booking_id, status):
        raise Exception('Not implemented')


class PickedUpStateHandler(AbstractStateHandler):
    def handle(self, booking_id, status):
        raise Exception('Not implemented')


class DoneStateHandler(AbstractStateHandler):
    def handle(self, booking_id, status):
        raise Exception('Not implemented')
