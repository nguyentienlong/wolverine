""" Vehicle Model """

from mongoengine import *

import datetime


class Vehicle(Document):
    """ . """
    short_id = StringField(unique=True)
    # owner
    owner = StringField()
    # License plate (biển số)
    license_plate = StringField(required=True, unique=True)
    # Address string
    address = StringField()
    # Address location
    location = PointField()
    # Manufacturer
    manufacturer = StringField()
    # Brand
    brand = StringField()
    # Year
    year = IntField()
    # Transmission: auto or manual
    transmission = StringField()
    # Engine: gas/diesel/hybrid
    engine = StringField()
    # gasoline consumption per 100 km
    gasoline_consumption_per_100_km = IntField()
    # Seat - 4 cho [4,5,6] - 5 cho [5,6,7]
    seats = IntField()
    # for search
    # - Seat: 4 or 7.
    # If 4 then return all 2, 3, 4, 5 seats-cars
    # If 7 then return all 6, 7, 8, 9 seats-cars
    searchable_seats = IntField()
    # Model
    model = StringField()
    # Description
    description = StringField()
    # Images
    images = ListField()
    # Price
    price_per_day = FloatField()
    # price on weekend
    price_on_weekend = FloatField()
    # Handover documents
    handover_documents = ListField()
    # Mortgage
    mortgage = ListField()
    # Instant booking
    instant_booking = BooleanField(default=False)
    # Deliver
    # - Deliver distance
    # - Deliver fee per km
    # {"enabled": true/false, "deliver_distance": "100 km",
    # "fee_per_km": 5000 }
    delivery = DictField(default={})
    # Limit road
    # - Limit value
    # - Over limit fee per km
    # {"enabled": true/false, "limit_value": 100, "fee_per_km": 5000}
    limit_road = DictField(default={})
    # Status - only show vehicle is verified on search result
    status = StringField()
    # Rating
    rating = FloatField()
    # Number of rating
    number_of_rating = IntField()
    # reserved_list refer to booking.reserved_date_time
    # only insert here - when user deposit / for mvp pre_accepted
    # only delete here - when user canceled/done
    reserved_list = ListField()

    created_date_time = IntField(
        required=True,
        default=datetime.datetime.now().timestamp()
    )

    updated_at = IntField(
        default=datetime.datetime.now().timestamp()
    )

    slug = StringField()

    """
    {
        "feedbacks": [{
                "id": "ABCDE1234567890",
                "short_booking_id": "XYZ123",
                "user": {
                    "id": "hRNMPVsIWYTbis9Ox92gpeAh1Bl1",
                    "name": "Teo",
                    "avatar": "image"
                },
                "vehicle": {
                    "id": "5ad17f611d41c824a9b7348b"
                },
                "rating": 5,
                "comment": "Good service",
                "created_date_time": 12567899
    
            },
            {
                "id": "1BCDE1234567890",
                "short_booking_id": "XYZ125",
                "user": {
                    "id": "hRNMPVsIWYTbis9Ox92gpeAh1Bl1",
                    "name": "Teo",
                    "avatar": "image"
                },
                "vehicle": {
                    "id": "5ad17f611d41c824a9b7348b"
                },
                "rating": 5,
                "comment": "Good service",
                "created_date_time": 12567899
    
            }
        ]
    }
    """
    feedbacks = ListField(default=None)
