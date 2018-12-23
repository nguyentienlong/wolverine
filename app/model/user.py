""" User Model """

from mongoengine import *
from datetime import datetime

STATUS = ('active', 'not_active', 'banned')


class User(Document):
    id = StringField(primary_key=True)
    email = EmailField(required=True, unique=True)
    name = StringField(required=True)
    phone_number = StringField(max_length=20, default='')
    id_number = StringField(default='')
    id_number_images = ListField(default=None)
    status = StringField(required=True, max_length=20)
    created_date = IntField(
        required=True,
        default=datetime.now().timestamp()
    )
    sign_in_provider = StringField()
    avatar = StringField()
    banking_account = StringField()

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

    meta = {'allow_inheritance': True}


class CarOwner(User):
    info = StringField()
