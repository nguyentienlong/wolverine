#!/usr/bin/env python
# -*- coding: utf-8 -*-

import falcon
import json

from datetime import datetime

import shortuuid

from app.hook.common import api_key, authenticate, parse_request_body
from app import log
from app import config
from app.model import Booking as BookingModel, User, Vehicle

logger = log.get_logger()


class FeedBack(object):
    @falcon.before(api_key)
    @falcon.before(authenticate)
    @falcon.before(parse_request_body)
    def on_post(self, req, resp, short_booking_id):
        """
        ** Request **

            POST /v1/feedback/short_booking_id
            --data = {"rating":5.0, "comment":"good service"}

        ** Response **

            200 with json string IF success
        :param req:
        :param resp:
        :param short_booking_id:
        :return:
        """
        current_auth_user_info = req.context['auth_user']
        logger.info(current_auth_user_info)

        data = req.params.get('body')
        logger.info(data)

        booking = BookingModel.\
            objects(short_id=short_booking_id).\
            first()
        if booking is None:
            raise Exception(
                "Can't find booking id {}".format(short_booking_id)
            )

        feedback = dict()

        # owner give feedback to renter
        # todo move this into separate function
        if current_auth_user_info['user_id'] == booking.owner:
            logger.info("owner give feedback to renter")

            owner = User.objects(id=booking.owner).first()

            feedback['id'] = shortuuid.ShortUUID(
                alphabet=config.UUID_ALPHABET
            ).random(length=config.FEEDBACK_ID_LENGTH)

            feedback['short_booking_id'] = short_booking_id
            feedback['user'] = {
                "id": owner.id,
                "name": owner.name,
                "avatar": owner.avatar
            }
            feedback['vehicle'] = {"id": booking.vehicle['id']}
            if 'rating' not in data:
                raise falcon.HTTPBadRequest(
                    description="'rating' is mandatory"
                )

            feedback['rating'] = float(data['rating'])

            feedback['comment'] = data['comment']\
                if 'comment' in data else None

            feedback['created_date_time'] = int(datetime.now().timestamp())

            # owner give feedback to renter
            renter = User.objects(id=booking.renter).first()

            if renter.feedbacks is None:
                renter.feedbacks = [feedback]
            elif isinstance(renter.feedbacks, list):
                renter.feedbacks.append(feedback)

            renter.save()

            booking.is_owner_gave_feedback = True
            booking.save()

        # todo move this into separate function
        # renter give feedback to a vehicle of owner
        if current_auth_user_info['user_id'] == booking.renter:
            logger.info("renter give feedback to a vehicle")
            renter = User.objects(id=booking.renter).first()
            vehicle = Vehicle.objects(id=booking.vehicle['id']).first()

            feedback['id'] = shortuuid.ShortUUID(
                alphabet=config.UUID_ALPHABET
            ).random(length=config.FEEDBACK_ID_LENGTH)

            feedback['short_booking_id'] = short_booking_id
            feedback['user'] = {
                "id": renter.id,
                "name": renter.name,
                "avatar": renter.avatar
            }
            if 'rating' not in data:
                raise falcon.HTTPBadRequest(
                    description="'rating' is mandatory"
                )

            feedback['rating'] = float(data['rating'])

            feedback['comment'] = data['comment'] \
                if 'comment' in data else None

            feedback['created_date_time'] = int(datetime.now().timestamp())

            # owner give feedback to renter
            if vehicle.feedbacks is None:
                vehicle.feedbacks = [feedback]
            elif isinstance(vehicle.feedbacks, list):
                vehicle.feedbacks.append(feedback)

            vehicle.save()

            booking.is_renter_gave_feedback = True
            booking.save()

        resp.body = json.dumps({
            'status': 'success',
            'message': 'Feedback id #{} submitted'. format(
                feedback['id']
            ),
            'data': {'feedback': feedback}
        })
