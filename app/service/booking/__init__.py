#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import *

from abc import ABC, abstractmethod


class AbstractStateHandler(ABC):
    BOOKING_PHASE_INITIALIZED = "initialized"
    BOOKING_PHASE_ACCEPTED = "accepted"
    BOOKING_PHASE_REJECTED = "rejected"
    BOOKING_PHASE_CANCELED = "canceled"
    BOOKING_PHASE_DEPOSITED = "deposited"
    BOOKING_PHASE_PICKED_UP = "picked_up"
    BOOKING_PHASE_DONE = "done"

    def __new__(cls):
        if '_instance' not in type.__dict__:
            cls._instance = object.__new__(cls)
        return cls._instance

    @abstractmethod
    def handle(self, **kwargs):
        pass
