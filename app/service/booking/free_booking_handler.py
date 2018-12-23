#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shortuuid

from . import AbstractStateHandler
from app import log
from app.model import Booking, Vehicle, User
from app import config
from datetime import datetime
from app.utils import send_email

logger = log.get_logger()
SERVICE_TYPE = 'free'

STATE_ORDER = {
    # renter book a vehicle
    AbstractStateHandler.BOOKING_PHASE_INITIALIZED: 1,

    # owner accepted the deal with renter
    AbstractStateHandler.BOOKING_PHASE_ACCEPTED: 2,

    # owner rejected the deal after discussion
    AbstractStateHandler.BOOKING_PHASE_REJECTED: 2,

    # client cancel after booking initialized, owner cancel after accepting
    AbstractStateHandler.BOOKING_PHASE_CANCELED: 3,

    # renter gave vehicle back to owner, both side give feed back to each other
    AbstractStateHandler.BOOKING_PHASE_DONE: 4
}


def validate_status(status):
    if status not in STATE_ORDER:
        raise Exception('{} is not a valid'.format(status))


class InitializedStateHandler(AbstractStateHandler):
    def handle(self, **kwargs):
        logger.info('{} InitializedStateHandler'.format(SERVICE_TYPE))

        vehicle_id = kwargs['vehicle_id']
        renter_id = kwargs['user_id']
        dt_range_from = kwargs['dt_range_from']
        dt_range_to = kwargs['dt_range_to']
        total_price = kwargs['total_price']

        # check if booking user has phone or id info
        renter = User.objects(id=renter_id).first()
        if (not renter.id_number) and (not renter.phone_number):
            raise Exception(
                "Either id_number or phone_number can't be empty"
            )

        # check total unfinished trip < max num trips from config
        unfinished_trips = Booking.objects(
            __raw__={
                "renter": {"$eq": renter_id},
                "current_phase": {
                    "$nin": [
                        AbstractStateHandler.BOOKING_PHASE_DONE,
                        AbstractStateHandler.BOOKING_PHASE_REJECTED,
                        AbstractStateHandler.BOOKING_PHASE_CANCELED,
                    ]
                }
            }
        )

        if len(unfinished_trips) >= int(config.MAXIMUM_UNFINISHED_TRIPS):
            raise Exception(
                "User {} reach maximum of unfinished trips".
                format(renter.name)
            )

        # check if vehicle existed
        vehicle = Vehicle.objects(id=vehicle_id).first()
        if not isinstance(vehicle, Vehicle):
            raise Exception(
                "Vehicle id {} "
                "is not existed".format(vehicle_id)
            )

        if vehicle.owner == renter_id:
            raise Exception(
                "Renter {} can't book his/her vehicle_id {}".format(
                    renter.name, vehicle_id
                )
            )

        if dt_range_from >= dt_range_to:
            raise Exception("date_time range is not valid")

        # if all fine, insert into booking collection with phase = init
        # check if reserved_date_time is available for this vehicle
        # todo: this can be improved
        # todo: by using __raw__ query same as search handler
        for item in vehicle.reserved_list:
            if (item['from'] <= dt_range_from <= item['to']) or \
                    (item['from'] <= dt_range_to <= item['to']):
                raise Exception("Booking date has been reserved")

        booking = Booking()
        booking.short_id = shortuuid.ShortUUID(
            alphabet=config.UUID_ALPHABET
        ).random(length=config.BOOKING_ID_LENGTH)

        booking.renter = renter_id
        booking.owner = vehicle.owner

        # only show vehicle image
        images = [
            image for image in vehicle.images
            if 'type' in image and
               image['type'] == config.VEHICLE_IMAGE_VEHICLE_TYPE
        ]

        booking.vehicle = {
            "id": vehicle_id,
            "short_id": vehicle.short_id,
            'slug': vehicle.slug,
            "images": images,
            "manufacturer": vehicle.manufacturer,
            "brand": vehicle.brand,
            "model": vehicle.model,
            "year": vehicle.year,
            "description": vehicle.description
        }
        booking.phases[AbstractStateHandler.BOOKING_PHASE_INITIALIZED] = {
            "date_time": datetime.now().timestamp()
        }

        booking.current_phase = AbstractStateHandler. \
            BOOKING_PHASE_INITIALIZED
        booking.reserved_date_time = {
            "from": dt_range_from,
            "to": dt_range_to
        }
        # fixme, TODO, calculate by server side,
        # todo, then compare with the price send from client
        booking.total_price = float(total_price)
        booking.save()

        # TODO booking status changed to initialized - IMPROVE LATER
        # can use publishing (observers design patterns here)
        # send email to renter
        send_email(
            to_email=renter.email,
            # todo localization
            subject="Yêu cầu thuê xe {} đã được gửi".format(booking.short_id),
            # todo localization
            content="Vui lòng chờ phản hồi từ chủ xe!"
        )
        # send email to owner
        owner = User.objects(id=booking.owner).first()

        send_email(
            to_email=owner.email,
            # todo localization
            subject="Có yêu cầu thuê xe {}".format(booking.short_id),
            # todo localization
            content="Có yêu cầu thuê xe {} từ {}".format(
                vehicle.license_plate,
                renter.name
            )
        )

        return booking


class AcceptedStateHandler(AbstractStateHandler):
    def handle(self, **kwargs):
        logger.info('{} AcceptedStateHandler'.format(SERVICE_TYPE))

        req_user_id = kwargs['req_user_id']
        booking_id = kwargs['booking_id']
        status = kwargs['status']

        validate_status(status)

        booking_info = Booking.objects.get(short_id=booking_id)

        # check ìf current user allow to approve this
        vehicle = Vehicle.objects(id=booking_info.vehicle['id']).first()

        if vehicle.owner != req_user_id:
            raise Exception(
                "Only vehicle owner can accept the booking request"
            )

        if status in booking_info.phases:
            raise Exception('Status {} already set'.format(status))

        if booking_info.current_phase == \
                AbstractStateHandler.BOOKING_PHASE_REJECTED:
            raise Exception(
                "Can't accept after rejected the booking"
            )

        booking_info.current_phase = status
        booking_info.phases[status] = {
            "date_time": datetime.now().timestamp()
        }
        booking_info.save()

        renter = User.objects(id=booking_info.renter).first()
        owner = User.objects(id=booking_info.owner).first()

        # send email to renter
        send_email(
            to_email=renter.email,
            # todo localize
            subject="Yêu cầu thuê xe {} đã được đồng ý".
            format(booking_info.short_id),
            # todo localize
            content="Bạn có thể liên hệ chủ xe qua số điện thoại: {} "
                    "hoặc email {}".format(owner.phone_number, owner.email)
        )
        # send email to owner
        send_email(
            to_email=owner.email,
            # todo localize
            subject="Đồng ý cho thuê chuyến {} thành công".
            format(booking_info.short_id),
            content="Bạn có thể liên hệ khách thuê qua số điện thoại: {} "
                    "hoặc email: {}".format(renter.phone_number, renter.email)
        )
        # update vehicle reserved_list
        vehicle = Vehicle.objects.get(id=booking_info.vehicle['id'])
        if booking_info.reserved_date_time not in vehicle.reserved_list:
            vehicle.reserved_list.append(booking_info.reserved_date_time)
            vehicle.save()

        return booking_info


class RejectedStateHandler(AbstractStateHandler):
    def handle(self, **kwargs):
        logger.info('{} RejectedStateHandler'.format(SERVICE_TYPE))
        booking_id = kwargs['booking_id']
        status = kwargs['status']
        req_user_id = kwargs['req_user_id']

        validate_status(status)

        booking_info = Booking.objects.get(short_id=booking_id)
        # check ìf current user allow to reject the booking
        vehicle = Vehicle.objects(id=booking_info.vehicle['id']).first()

        if vehicle.owner != req_user_id:
            raise Exception(
                "Only vehicle owner can reject the booking request"
            )

        if status in booking_info.phases:
            raise Exception('Status {} already set'.format(status))

        if booking_info.current_phase == \
                AbstractStateHandler.BOOKING_PHASE_ACCEPTED:
            raise Exception(
                "Can't reject after accepting the booking"
            )

        booking_info.current_phase = status
        booking_info.phases[status] = {
            "date_time": datetime.now().timestamp()
        }
        booking_info.save()

        renter = User.objects(id=booking_info.renter).first()
        owner = User.objects(id=booking_info.owner).first()

        # send email to renter
        send_email(
            to_email=renter.email,
            # todo localize
            subject="Yêu cầu thuê xe {} đã bị từ chối".
            format(booking_info.short_id),
            content="Yêu cầu thuê xe {} đã bị từ chối bởi {}".
            format(booking_info.short_id, owner.name)
        )
        # send email to owner
        send_email(
            to_email=owner.email,
            # todo localize
            subject="Bạn đã từ chối yêu cầu thuê {}".
            format(booking_info.short_id),
            content="Bạn đã từ chối yêu cầu thuê {}".
            format(booking_info.short_id),
        )

        return booking_info


class CanceledStateHandler(AbstractStateHandler):
    def handle(self, **kwargs):
        logger.info('{} CanceledStateHandler'.format(SERVICE_TYPE))

        booking_id = kwargs['booking_id']
        status = kwargs['status']
        req_user_id = kwargs['req_user_id']

        validate_status(status)
        booking_info = Booking.objects.get(short_id=booking_id)

        # only renters can cancel their booking
        # todo change req_user_id to renter_id
        if booking_info.renter != req_user_id:
            raise Exception(
                "Only renters can cancel their own booking"
            )

        if status in booking_info.phases:
            raise Exception('Status {} already set'.format(status))

        # todo - reuse this for owner
        # if booking_info.current_phase != \
        #         AbstractStateHandler.BOOKING_PHASE_ACCEPTED:
        #     raise Exception(
        #         'Need to set status {} before {}'.
        #         format(
        #             AbstractStateHandler.BOOKING_PHASE_ACCEPTED,
        #             status
        #         )
        #     )

        booking_info.current_phase = status
        booking_info.phases[status] = {
            "date_time": datetime.now().timestamp()
        }
        booking_info.save()

        vehicle = Vehicle.objects.get(id=booking_info.vehicle['id'])
        if booking_info.reserved_date_time in vehicle.reserved_list:
            vehicle.reserved_list.remove(booking_info.reserved_date_time)
            vehicle.save()

        renter = User.objects(id=booking_info.renter).first()
        owner = User.objects(id=booking_info.owner).first()

        # send email to renter
        send_email(
            to_email=renter.email,
            # todo localize
            subject="Bạn đã huỷ chuyến {}".format(booking_info.short_id),
            content="Bạn đã huỷ chuyến {}".format(booking_info.short_id)
        )
        # send email to owner
        send_email(
            to_email=owner.email,
            subject="Khách thuê {} đã huỷ chuyến {}".
            format(renter.name, booking_info.short_id),
            content="Khách thuê {} đã huỷ chuyến {}".
            format(renter.name, booking_info.short_id)
        )

        return booking_info


class DoneStateHandler(AbstractStateHandler):
    def handle(self, **kwargs):
        logger.info('{} DoneStateHandler'.format(SERVICE_TYPE))

        booking_id = kwargs['booking_id']
        status = kwargs['status']
        validate_status(status)
        booking_info = Booking.objects.get(short_id=booking_id)

        if datetime.now().timestamp() < \
                booking_info.reserved_date_time.get('to') - \
                (config.HOURS_TO_GIVE_VEHICLE_BACK_TO_OWNER * 3600):
            raise Exception(
                "Done status can only set after the last date of booking"
            )

        if status in booking_info.phases:
            raise Exception('Status {} already set'.format(status))

        if booking_info.current_phase != \
                AbstractStateHandler.BOOKING_PHASE_ACCEPTED:
            raise Exception(
                'Need to set status {} before {}'.
                format(AbstractStateHandler.BOOKING_PHASE_ACCEPTED, status)
            )

        booking_info.current_phase = status
        booking_info.phases[status] = {
            "date_time": datetime.now().timestamp()
        }
        booking_info.save()

        vehicle = Vehicle.objects.get(id=booking_info.vehicle['id'])
        if booking_info.reserved_date_time in vehicle.reserved_list:
            vehicle.reserved_list.remove(booking_info.reserved_date_time)
            vehicle.save()

        renter = User.objects(id=booking_info.renter).first()
        owner = User.objects(id=booking_info.owner).first()

        # send email to renter
        send_email(
            to_email=renter.email,
            # todo localize
            subject="Bạn đã hoàn thành chuyến {}".
            format(booking_info.short_id),
            content="Bạn đã hoàn thành chuyến {}".
            format(booking_info.short_id)
        )
        # send email to owner
        send_email(
            to_email=owner.email,
            # todo localize
            subject="Chuyến {} đã hoàn thành!".format(booking_info.short_id),
            content="Chuyến {} đã hoàn thành!".format(booking_info.short_id)
        )

        return booking_info
