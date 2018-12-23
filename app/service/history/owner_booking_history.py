#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.model import Vehicle, Booking
from . import AbstractBookingHistory


class OwnerBookingHistory(AbstractBookingHistory):
    def get(self, req):
        current_user_id = req.context['auth_user']['uid']
        vehicle_id = req.get_param('vehicle_id')
        vehicle_slug = req.get_param('vehicle_slug')
        short_id = req.get_param('short_id')
        # get booking history of a vehicle
        if vehicle_id or vehicle_slug or short_id:
            vehicle = None
            # check if vehicle_id belongs to current user
            if vehicle_id:
                vehicle = Vehicle.objects(id=vehicle_id).first()
            if vehicle_slug:
                vehicle = Vehicle.objects(slug=vehicle_slug).first()
            if short_id:
                vehicle = Vehicle.objects(short_id=short_id).first()

            if vehicle is None:
                raise Exception(
                    "Can't find vehicle with {}".format(
                        vehicle_id if vehicle_id else vehicle_slug
                    )
                )

            if vehicle.owner != current_user_id:
                raise Exception("Only owner can view their own vehicle history")

            booking_history = Booking.objects(vehicle__id=vehicle_id)
        else:
            booking_history = Booking.objects(owner=current_user_id)

        return booking_history
