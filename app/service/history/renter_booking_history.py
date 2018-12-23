#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import AbstractBookingHistory

from app.model import Booking


class RenterBookingHistory(AbstractBookingHistory):
    def get(self, req):
        current_user_id = req.context['auth_user']['uid']
        booking_history = Booking.objects(renter=current_user_id)

        return booking_history
