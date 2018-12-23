#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson import ObjectId

from app.model import Vehicle
from app import log

logger = log.get_logger()

exclude_vehicle_fields = (
    'owner',
    'created_date_time'
)


class SearchHandler(object):
    def search(self, params):
        logger.info("Search params: {}".format(params))
        query = {"status": "verified"}
        if params:
            query = self.build_query(params)
        logger.info("Search Query: {}".format(query))
        return Vehicle.\
            objects(__raw__=query).\
            exclude(*exclude_vehicle_fields)

    def build_query(self, params):
        query = {"$and": []}
        query["$and"].append({"status": "verified"})

        if 'vehicle_id' in params:
            query["$and"].append(
                {"_id": ObjectId(params['vehicle_id'])}
            )

        if ('from_ts' in params) and ('to_ts' in params):
            query["$and"].append(
                self.build_ts_query(params['from_ts'], params['to_ts'])
            )
        if ('from_ppd' in params) and ('to_ppd' in params):
            query["$and"].append(
                self.build_price_per_day_query(
                    params['from_ppd'],
                    params['to_ppd']
                )
            )
        if 'instant_booking' in params:
            query["$and"].append(
                self.build_instant_booking_query(
                    params['instant_booking']
                )
            )
        if 'delivery' in params:
            query["$and"].append(
                self.build_delivery_query(
                    params['delivery']
                )
            )

        if 'location' in params:
            query["$and"].append(
                self.build_location_query(
                    params['location']
                )
            )

        # simple list query
        for param in ['manufacturer', 'brand', 'year',
                      'transmission', 'engine', 'model',
                      'seats']:
            if param in params:
                query["$and"].append(
                    self.build_simple_list_query(param, params[param])
                )

        return query

    def build_ts_query(self, from_ts, to_ts):
        """
        build timestamp query
        :param from_ts:
        :param to_ts:
        :return:
        """
        if int(from_ts) >= int(to_ts):
            raise Exception(
                "Datetime range is not valid"
            )
        query = {"$or": [
                    {"reserved_list": []},
                    {"reserved_list.from": {"$gt": int(to_ts)}},
                    {"reserved_list.to": {"$lt": int(from_ts)}}
                ]}
        return query

    def build_price_per_day_query(self, from_ppd, to_ppd):
        """
        build price per day query
        :param from_ppd:
        :param to_ppd:
        :return:
        """
        if float(from_ppd) > float(to_ppd):
            raise Exception(
                "Price per day range is not valid"
            )
        query = {
            "$and": [
                {"price_per_day": {"$gte": float(from_ppd)}},
                {"price_per_day": {"$lte": float(to_ppd)}}
            ]
        }
        return query

    def build_instant_booking_query(self, instant_booking):
        if instant_booking in ['true', '1']:
            return {
                "instant_booking": True
            }

        return {
            "instant_booking": False
        }

    def build_delivery_query(self, delivery):
        if delivery in ['true', '1']:
            return {
                "delivery.enabled": True
            }

        return {
            "delivery.enabled": False
        }

    def build_simple_list_query(self, key, value):
        if key == 'seats':
            return {
                'searchable_seats': {
                    '$in': [
                        int(item) for item in value
                    ]
                }
            }
        if (key == 'transmission') and isinstance(value, list):
            return {
                'transmission': {
                    '$in': [item for item in value]
                }
            }
        return {
            key: value
        }

    def build_location_query(self, location):
        if len(location) < 2:
            raise Exception('Invalid location param {}'.format(location))

        long = float(location[0])
        lat = float(location[1])
        r = 30  # move this to config TODO
        if len(location) == 3:
            r = float(location[2])

        return {
            'location': {
                '$geoWithin': {
                    '$center': [
                        [long, lat], r
                    ]
                }
            }
        }
