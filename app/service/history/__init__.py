#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import *

from abc import ABC, abstractmethod


class AbstractBookingHistory(ABC):
    OWNER = "owner"
    RENTER = "renter"

    def __new__(cls):
        if '_instance' not in type.__dict__:
            cls._instance = object.__new__(cls)
        return cls._instance

    @abstractmethod
    def get(self, req):
        pass
