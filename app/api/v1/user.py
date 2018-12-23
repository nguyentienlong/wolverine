#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" UserResource Class """
import falcon
import json
import shortuuid

from datetime import datetime

from mongoengine import NotUniqueError
from mailchimp3 import MailChimp

from app import log
from app import config
from app.hook.common import api_key, authenticate, parse_request_body

from app.model import User, Vehicle, EmailSubscription

from app.utils.helpers import send_email

logger = log.get_logger()

USER_STATUS_ACTIVE = 'active'


class UserItem(object):
    @falcon.before(api_key)
    @falcon.before(authenticate)
    def on_get(self, req, resp, user_id):
        current_auth_user_info = req.context['auth_user']

        if user_id == current_auth_user_info['user_id']:
            logger.info('user view there own info')
            user = self._get_current_user(current_auth_user_info)
        else:
            logger.info('view another user info')
            user = self._get_another_user(user_id)

        if not isinstance(user, User):
            raise falcon.HTTPBadRequest(
                title="User Not Found",
                description="User Not Found"
            )

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'status': 'success',
            'message': 'Success',
            'data': {'user': json.loads(user.to_json())}
        })

    def _get_another_user(self, user_id):
        # todo move restrict field to config file
        return User.objects(id=user_id).\
            only('id', 'name', 'status', 'created_date').first()

    def _get_current_user(self, current_auth_user_info):
        user = User \
            .objects(id=current_auth_user_info['user_id']) \
            .first()
        if not isinstance(user, User):
            user = self._create_new_user(current_auth_user_info)

        return user

    def _create_new_user(self, auth_user_info):
        logger.info('create new user')
        try:
            user = User()

            user.id = auth_user_info['user_id']
            user.email = auth_user_info['email']
            if 'name' in auth_user_info:
                user.name = auth_user_info['name']
            user.status = USER_STATUS_ACTIVE
            # user.created_date = use default
            user.sign_in_provider = \
                auth_user_info['firebase']['sign_in_provider']
            user.save()

            return user
        except Exception as e:
            raise e

    @falcon.before(api_key)
    @falcon.before(authenticate)
    @falcon.before(parse_request_body)
    def on_put(self, req, resp, user_id):
        """
        Update user information
        PUT /v1/user/{user_id}
        :param req:
        :param resp:
        :param user_id:
        :return:
        """

        current_auth_user_id = req.context['auth_user']['user_id']
        if current_auth_user_id != user_id:
            raise Exception(
                "You can't update other user_id {} info".format(user_id)
            )
        try:
            user = User.objects(id=user_id).first()
            data = req.params.get('body')
            logger.info(data)
            if data is None:
                raise Exception(
                    "Data is empty"
                )
            for key in data:
                if not hasattr(user, key):
                    raise Exception(
                        "{} is not valid attribute".format(key)
                    )

                # add disallowed_fields to a list then filter
                if key == 'status':
                    raise Exception(
                        "User can't update this info"
                    )
                setattr(user, key, data.get(key))
            user.save()
        except Exception as e:
            logger.exception(e)
            raise falcon.HTTPBadRequest(
                title="Bad Request",
                description=str(e)
            )

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'status': 'success',
            'message': 'Success',
            'data': {'user': json.loads(user.to_json())}
        })


class VehicleItem(object):
    @falcon.before(api_key)
    @falcon.before(authenticate)
    def on_get(self, req, resp, vehicle_id):
        """
        Get info of a vehicle of current user
        GET /v1/user/vehicle/{vehicle_id}

        :param req:
        :param resp:
        :param vehicle_id:
        :return:
        """
        logger.info('get vehicle detail of current user')

        try:
            vehicle = Vehicle.objects(
                id=vehicle_id,
                owner=req.context['auth_user']['user_id']
            ).first()

            if not vehicle:
                raise falcon.HTTPError(status=falcon.HTTP_204)
        except Exception as e:
            raise e

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'status': 'success',
            'message': 'Success',
            'data': {'vehicle': json.loads(vehicle.to_json())}
        })

    @falcon.before(api_key)
    @falcon.before(authenticate)
    @falcon.before(parse_request_body)
    def on_put(self, req, resp, vehicle_id):
        """
        Update vehicle information of owner
        PUT /v1/user/vehicle/{vehicle_id}
        :param req:
        :param resp:
        :param vehicle_id:
        :return:
        """
        current_auth_user_info = req.context['auth_user']

        try:
            vehicle = Vehicle.objects(
                id=vehicle_id, owner=current_auth_user_info['user_id']
            ).first()
            if not isinstance(vehicle, Vehicle):
                raise Exception("Vehicle {} not found".format(vehicle_id))

            data = req.params.get('body')
            for key in data:
                if not hasattr(vehicle, key):
                    raise Exception(
                        "{} is not valid attribute".format(key)
                    )
                if key == 'status':
                    raise Exception(
                        "Only admin can change the status"
                    )
                setattr(vehicle, key, data.get(key))

            # update status to unverified after owner change
            # their vehicle info
            vehicle.status = 'unverified'
            vehicle.updated_at = datetime.now().timestamp()
            if vehicle.short_id is None:
                vehicle.short_id = shortuuid.ShortUUID(
                    alphabet=config.UUID_ALPHABET
                ).random(length=config.WOLVERINE_ID_LENGTH)
            vehicle.slug = "{year}-{manufacturer}-{brand}-{short_id}".\
                format(
                    year=vehicle.year,
                    manufacturer=vehicle.manufacturer,
                    brand=vehicle.brand,
                    short_id=vehicle.short_id
                )
            vehicle.save()

            send_email(
                to_email=config.EMAIL_OPERATION_MAIL_LIST,
                subject="[Edit] Xe cần duyệt: {}".
                format(vehicle.license_plate),
                content="{mizu_base_url}/vehicle/{id}".format(
                    mizu_base_url=config.MIZU_BASE_URL,
                    id=vehicle.id
                )
            )
        except Exception as e:
            logger.exception(e)
            raise falcon.HTTPBadRequest(
                title="Bad Request",
                description=str(e)
            )

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'status': 'success',
            'message': 'Success',
            'data': {'vehicle': json.loads(vehicle.to_json())}
        })

    @falcon.before(api_key)
    @falcon.before(authenticate)
    def on_delete(self, req, resp, vehicle_id):
        """
        ?? do we need this
        DELETE /v1/user/vehicle/{vehicle_id}
        :param req:
        :param resp:
        :param vehicle_id:
        :return:
        """
        raise falcon.HTTPBadRequest(
            title='Not implemented', description='not implement')


class VehicleCollection(object):
    @falcon.before(api_key)
    @falcon.before(authenticate)
    def on_get(self, req, resp):
        """
        Get info of a vehicle of current user
        GET /v1/user/vehicle

        :param req:
        :param resp:
        :return:
        """
        logger.info('get ALL vehicle detail of current user')

        vehicle = Vehicle.objects(owner=req.context['auth_user']['user_id'])

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'status': 'success',
            'message': 'Success',
            'data': {
                'total_items': vehicle.count(),
                'vehicle': json.loads(vehicle.to_json())
            }
        })

    @falcon.before(api_key)
    @falcon.before(authenticate)
    @falcon.before(parse_request_body)
    def on_post(self, req, resp):
        """
        POST /v1/user/vehicle
        -H 'Authorization: Bearer {token}'
        -H 'api_key: key'
        -d '{json_data}'

        :param req:
        :param resp:
        :return:
        """
        data = req.params.get('body')
        current_user_id = req.context['auth_user']['uid']
        # todo move create vehicle into a service
        vehicle = self.create_vehicle(data, current_user_id)

        send_email(
            to_email=config.EMAIL_OPERATION_MAIL_LIST,
            subject='[New] Xe mới cần duyệt: {}'.
            format(vehicle.license_plate),
            content="{mizu_base_url}/vehicle/{id}".format(
                mizu_base_url=config.MIZU_BASE_URL,
                id=vehicle.id
            )
        )

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'status': 'success',
            'message': 'Vehicle created',
            'data': {'vehicle': json.loads(vehicle.to_json())}
        })

    @staticmethod
    def create_vehicle(data, current_user_id):
        if 'status' in data:
            raise falcon.HTTPBadRequest(
                title=falcon.HTTP_BAD_REQUEST,
                description="Changing status is not allow "
                            "to set when creating a vehicle"
            )
        try:
            # get user by auth_user uid
            current_user = User.objects.get(id=current_user_id)
            logger.info(current_user.phone_number)
            if (not current_user.phone_number) and \
                    (not current_user.banking_account):
                raise Exception(
                    "Either phone_number or "
                    "banking account is empty"
                )

            vehicle = Vehicle.from_json(json.dumps(data))
            # - Seat: 4 or 7.
            # If 4 then return all 2, 3, 4, 5 seats-cars
            # If 7 then return all 6, 7, 8, 9 seats-cars
            if vehicle.seats in range(2, 6):
                vehicle.searchable_seats = 4
            if vehicle.seats in range(6, 10):
                vehicle.searchable_seats = 7
            # default status = not_verified todo move to const
            # unverified, verified
            vehicle.status = 'unverified'
            vehicle.owner = current_user.id
            vehicle.short_id = shortuuid.ShortUUID(
                alphabet=config.UUID_ALPHABET
            ).random(length=config.WOLVERINE_ID_LENGTH)
            vehicle.slug = "{year}-{manufacturer}-{brand}-{short_id}".\
                format(
                    year=vehicle.year,
                    manufacturer=vehicle.manufacturer,
                    brand=vehicle.brand,
                    short_id=vehicle.short_id
                )
            vehicle.save()
        except NotUniqueError as e:
            logger.exception(e)
            raise falcon.HTTPBadRequest(
                title="Bad Request",
                description=str(e)
            )
        except Exception as e:
            logger.exception(e)
            raise falcon.HTTPBadRequest(
                title="Bad Request",
                description=str(e)
            )
        return vehicle


class Subscription(object):
    def __init__(self):
        pass

    @falcon.before(api_key)
    @falcon.before(parse_request_body)
    def on_post(self, req, resp):
        """
        #####User subscription
        Request:
            ```
            POST /v1/user/subscribe \
                -H 'api_key: {client_key}'
                -H 'Content-Type: application/json' -d 'data.json'
            ```
        Response:
            ```
                200 OK
                400 Bad Request
            ```
        :param req:
        :param resp:
        :return:
        """
        data = req.params.get('body')
        subscription = EmailSubscription.from_json(json.dumps(data))

        # save to mailchimp
        from mailchimp3.mailchimpclient import MailChimpError
        try:
            mailchimp_client = MailChimp(config.MC_API_KEY)
            mailchimp_client.lists.members.create(config.MC_CAMPAIGN_ID, {
                'email_address': subscription.email,
                'status': 'subscribed',
                'merge_fields': {
                    'IP_INFO': json.dumps(subscription.ip)
                },
            })

        except TypeError:
            raise falcon.HTTPBadRequest('Oops!',
                                        'A valid JSON document is required.')
        except MailChimpError as e:
            logger.error(e)
            raise falcon.HTTPBadRequest(
                title="Email existed", description="Email existed")

        # save to vietvivu365 db
        try:
            subscription.create_date = datetime.now()
            subscription.save()
        except NotUniqueError as e:
            logger.error('Email {} already subscribe'.format(
                subscription.email))
            raise falcon.HTTPBadRequest(
                title="Email existed", description="Email existed")

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'status': 'success',
            'message': 'User subscribed successfully',
            'data': {'subscription': json.loads(subscription.to_json())}
        })
