
import falcon
import json

from app.hook.common import authenticate, api_key
from app.model import Vehicle, User, Manufacturer as VManufacturer, Brand as VBrand, Model as VModel
from app import log
from app import config
from app.utils.helpers import Pagination, paginate, calculate_feedback

logger = log.get_logger()

public_vehicle_fields = (
    'id', 'manufacturer',
    'brand', 'year', 'transmission',
    'engine', 'gasoline_consumption_per_100_km', 'seats',
    'model', 'description', 'images',
    'price_per_day', 'instant_booking', 'delivery',
    'limit_road', 'status', 'rating',
    'number_of_rating',
    'short_id', 'slug'
)


class Collection(object):

    def __init__(self, _search_handler):
        self._search_handler = _search_handler

    @falcon.before(api_key)
    def on_get(self, req, resp):
        """
        Get all vehicle and basic info for public search
        GET /v1/vehicle
        :param req:
        :param resp:
        :return:
        """
        params = req.params
        vehicles = self._search_handler.search(params)

        page = 1
        item_per_page = config.ITEM_PER_PAGE
        if 'page' in req.params:
            page = int(req.params.get('page'))
        if 'item_per_page' in req.params:
            item_per_page = int(req.params.get('item_per_page'))

        vehicles_paginator = paginate(
            queryset=vehicles,
            page=page,
            item_per_page=item_per_page
        )

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'status': 'success',
            'message': 'Success',
            'data': {
                'total_items': vehicles_paginator.total_items,
                'page': vehicles_paginator.page,
                'item_per_page': vehicles_paginator.item_per_page,
                'total_pages': vehicles_paginator.total_pages,
                'vehicle': json.loads(
                    vehicles_paginator.items().to_json()
                )
            }
        })


class Item(object):
    @falcon.before(api_key)
    def on_get(self, req, resp, vehicle_id):
        """
        GET /v1/vehicle/{id}

        return public info of vehicle

        :param req:
        :param resp:
        :param vehicle_id:
        :return:
        """
        vehicle = Vehicle.\
            objects(id=vehicle_id).\
            first()

        total_rating, total_comments, rating = calculate_feedback(vehicle)
        feedback_summary = dict()
        feedback_summary['rating'] = rating
        feedback_summary['total_rating'] = total_rating
        feedback_summary['total_comments'] = total_comments

        if not isinstance(vehicle, Vehicle):
            raise Exception('vehicle with {} not found'.format(vehicle_id))

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'status': 'success',
            'message': 'Success',
            'data': {
                'vehicle': json.loads(vehicle.to_json()),
                'vehicle_feedback_summary': feedback_summary
            }
        })


class Manufacturer(object):
    @falcon.before(api_key)
    def on_get(self, req, resp):
        """
        GET /v1/vehicle/manufacturer \
            -H'origin:localhost' \
            -H'api-key:vietvivu365.local'

        params:
            page = 1
            item_per_page=10
        :param req:
        :param resp:
        :return:
        """
        page = 1
        item_per_page = config.ITEM_PER_PAGE
        if 'page' in req.params:
            page = int(req.params.get('page'))
        if 'item_per_page' in req.params:
            item_per_page = int(req.params.get('item_per_page'))

        query_set = VManufacturer.objects
        manufacturer_paginator = paginate(
            queryset=query_set,
            page=page,
            item_per_page=item_per_page
        )

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'status': 'success',
            'message': 'Success',
            'data': {
                'total_items': manufacturer_paginator.total_items,
                'page': manufacturer_paginator.page,
                'item_per_page': manufacturer_paginator.item_per_page,
                'total_pages': manufacturer_paginator.total_pages,
                'manufacturers': json.loads(
                    manufacturer_paginator.items().to_json()
                )
            }
        })


class Brand(object):
    @falcon.before(api_key)
    def on_get(self, req, resp, manufacturer):
        """
        GET /v1/vehicle/brand/{manufacturer}
            -H'origin:localhost' \
            -H'api-key:vietvivu365.local'
        params:
            page = 1
            item_per_page=10
        :param req:
        :param resp:
        :param manufacturer:
        :return:
        """
        page = 1
        item_per_page = config.ITEM_PER_PAGE
        if 'page' in req.params:
            page = int(req.params.get('page'))
        if 'item_per_page' in req.params:
            item_per_page = int(req.params.get('item_per_page'))

        query_set = VBrand.objects(manufacturer=manufacturer)

        brand_paginator = paginate(
            queryset=query_set,
            page=page,
            item_per_page=item_per_page
        )

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'status': 'success',
            'message': 'Success',
            'data': {
                'total_items': brand_paginator.total_items,
                'page': brand_paginator.page,
                'item_per_page': brand_paginator.item_per_page,
                'total_pages': brand_paginator.total_pages,
                'brands': json.loads(brand_paginator.items().to_json())
            }
        })


class Model(object):
    @falcon.before(api_key)
    def on_get(self, req, resp):
        """
        GET /v1/vehicle/model
            -H'origin:localhost' \
            -H'api-key:vietvivu365.local'
        params:
            page = 1
            item_per_page=10
        :param req:
        :param resp:
        :return:
        """

        page = 1
        item_per_page = config.ITEM_PER_PAGE
        if 'page' in req.params:
            page = int(req.params.get('page'))
        if 'item_per_page' in req.params:
            item_per_page = int(req.params.get('item_per_page'))

        query_set = VModel.objects
        model_paginator = paginate(
            queryset=query_set,
            page=page,
            item_per_page=item_per_page
        )

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'status': 'success',
            'message': 'Success',
            'data': {
                'total_items': model_paginator.total_items,
                'page': model_paginator.page,
                'item_per_page': model_paginator.item_per_page,
                'total_pages': model_paginator.total_pages,
                'models': json.loads(model_paginator.items().to_json())
            }
        })


class ItemSlug(object):
    @falcon.before(api_key)
    def on_get(self, req, resp, slug):
        """
        GET /v1/vehicle/slug/{slug}

        return public info of vehicle

        :param req:
        :param resp:
        :param slug:
        :return:
        """
        vehicle = Vehicle.objects(slug=slug)
        if not isinstance(vehicle.first(), Vehicle):
            raise Exception('vehicle with slug {} not found'.format(slug))

        owner = User.objects(id=vehicle.first().owner).\
            only('avatar', 'name').\
            first()
        if not isinstance(owner, User):
            raise Exception(
                "Can't find owner id {owner_id} info of vehicle with "
                "slug {slug}".format(owner_id=vehicle.owner, slug=slug)
            )

        # limit info
        vehicle = vehicle.first()

        total_rating, total_comments, rating = calculate_feedback(vehicle)
        feedback_summary = dict()
        feedback_summary['rating'] = rating
        feedback_summary['total_rating'] = total_rating
        feedback_summary['total_comments'] = total_comments

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'status': 'success',
            'message': 'Success',
            'data': {
                'vehicle': json.loads(vehicle.to_json()),
                'vehicle_feedback_summary': feedback_summary,
                'owner': json.loads(owner.to_json())
            }
        })
