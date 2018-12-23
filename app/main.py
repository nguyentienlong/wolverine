#!/usr/bin/env python
# -*- coding: utf-8 -*-

import falcon
from mongoengine import connection
import firebase_admin
from firebase_admin import credentials

from app.api.common import base
from app import log
from app import config
from app import errors
from app.middleware import CorsMiddleware
from app.api.v1 import user
from app.api.v1 import vehicle
from app.api.v1 import booking
from app.api.v1 import feedback
from app.service.search.search_handler import SearchHandler

logger = log.get_logger()

application = falcon.API(middleware=[CorsMiddleware()])

# setup db
db = connection.connect(db=config.DB_NAME, port=int(config.DB_PORT))

cred = credentials.Certificate('conf/firebase_adminsdk_credentials.json')
default_app = firebase_admin.initialize_app(cred)

""" base endpoint """
application.add_route('/v1/welcome', base.BaseResource())

""" . """
# on_get get user info
application.add_route('/v1/user/{user_id}', user.UserItem())
# on_get get info of a vehicle of user
application.add_route('/v1/user/vehicle/{vehicle_id}', user.VehicleItem())
# on_get get all vehicle of current user
# on_post create new vehicle
application.add_route('/v1/user/vehicle', user.VehicleCollection())

""" . """
# on get - get all vehicle for public search
application.add_route('/v1/vehicle', vehicle.Collection(SearchHandler()))

# on_get for get vehicle detail by vehicle_id
application.add_route('/v1/vehicle/{vehicle_id}', vehicle.Item())
# on_get get vehicle detail by slug
application.add_route('/v1/vehicle/slug/{slug}', vehicle.ItemSlug())

# booking
application.add_route('/v1/booking/{user_id}/{vehicle_id}', booking.Booking())
application.add_route('/v1/user/booking/{booking_id}', booking.Booking())
# booking history
application.add_route('/v1/booking/history/{user_type}', booking.Booking())
# view renter|owner info of a book
application.add_route(
    '/v1/booking/info/{user_type}/{short_booking_id}/{user_id}',
    booking.UserInfo()
)

# feedbacks
application.add_route('/v1/feedback/{short_booking_id}', feedback.FeedBack())

# manufacturer
application.add_route('/v1/vehicle/manufacturer', vehicle.Manufacturer())
application.add_route('/v1/vehicle/brand/{manufacturer}', vehicle.Brand())
application.add_route('/v1/vehicle/model', vehicle.Model())


""" user subscription """
application.add_route('/v1/user/subscribe', user.Subscription())


""" Error handler """
application.add_error_handler(Exception, errors.Handler.handle)
