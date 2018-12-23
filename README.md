# README #

vietvivu365 Backend API
### What is this repository for? ###

* Provide API Endpoints


### How do I get set up? 

For **development only**

- copy sample file to local file `cp sample.ini local.ini && cp firebase_adminsdk_credentials.json.sample firebase_adminsdk_credentials.json.local`
- run `mkdir .venv && virtualenv --python=/usr/local/bin/python3.6 .venv && source .venv/bin/activate` to activate python virtual env
- run `./install_local_environment.sh` to init development environment
- run `./localX.sh` to start local python server 
- try `curl -v  -XGET 'http://localhost:30000/v1/welcome' -H 'Api-key:default_key' -H 'Origin: localhost'`


For `stag` or `prod` environment:

- `git pull origin master`
- then, try `./stagX.sh` or `./prodX.sh`


### Contribution guidelines ###

* Writing tests: // Todo
* Code review: // Todo

---

### Endpoints

###Notice: MUST USE 3 headers [Authorization, Api-Key, Origin]
```
allowed_origins=
    localhost,
    http://localhost:3000,
    https://localhost:3000,
    http://vietvivu365.vn,
    https://vietvivu365.vn,
    http://www.vietvivu365.vn,
    https://www.vietvivu365.vn
```


**Response format**

```
{
    'status': 'success' or 'failed'
    'message': 'a message'
    'data': {}
}
```

###User:

**User model**
```
    id = StringField(primary_key=True)
    email = EmailField(required=True, unique=True)
    name = StringField(required=True)
    phone_number = StringField(max_length=20, default='')
    id_number = StringField(default='')
    id_number_images = ListField(default=None)
    status = StringField(required=True, max_length=20)
    created_date = IntField(
        required=True,
        default=datetime.utcnow().timestamp()
    )
    sign_in_provider = StringField()
    avatar = StringField()
    banking_account = StringField()

    """
    {
        "feedbacks": [{
                "id": "ABCDE1234567890",
                "booking_short_id": "XYZ123",
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
                "booking_short_id": "XYZ125",
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
```

#####Get user:
```
curl -X GET 'localhost:30000/v1/user/{$user_id}' \
    -H 'Authorization: Bearer {token}' \
    -H 'Api-Key: vietvivu365.local'
    -H 'Origin: {allowed_origins}'
```

Response:
```
200 OK: {"data": {"user": "{\"_id\": \"N7d5jep8RXYs1zPSDQEJgvMqQ4n1\", \"_cls\": \"User\", \"email\": \"longsymblog@gmail.com\", \"name\": \"long tien\", \"status\": \"active\", \"created_date\": {\"$date\": 1521269527459}, \"sign_in_provider\": \"password\"}"}}

204 No Content

403 Not allow origin
```

#####Edit user information:
```
PUT /v1/user/{user_id}

curl -v -XPUT 'http://localhost:30000/v1/user/NMTy4pl7aZf0bUzegn1w4ISfoIo2' \
        -H'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjZlYThhZmIwMjFjMjEzMDhjNzkzMDI2ZTMzNDA4ZGI3MDc2ODc0MWEifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJpcHgtc3RhZy05MjRlZSIsIm5hbWUiOiJhYmMxMjMiLCJhdWQiOiJ0cmlweC1zdGFnLTkyNGVlIiwiYXV0aF90aW1lIjoxNTIyNDg2NzY1LCJ1c2VyX2lkIjoiTk1UeTRwbDdhWmYwYlV6ZWduMXc0SVNmb0lvMiIsInN1YiI6Ik5NVHk0cGw3YVpmMGJVemVnbjF3NElTZm9JbzIiLCJpYXQiOjE1MjI0ODY3NjUsImV4cCI6MTUyMjQ5MDM2NSwiZW1haWwiOiJ0bGNudHRAeWFob28uY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsidGxjbnR0QHlhaG9vLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.EoDRBZfeoYjrvGCFBMnEiM1kjmWhakaRrAc9XojRhkwl_KyiTG2W8Hmjv5OpbKcHCukVyeCltZLSHBqI96SsBY0-sIb6_O1famSDwEsL51ILdmcI72NQx5C1eG2gBFsUanKxBOOAq5nDDFa3jRfswAYRFD2f4HdH_h4YWsuttLJVUgTbw1PJurbQDIwH_uU8_BighQqbTroudcuKawu7GuXpr6U6uP7il_hQX9QP2hIzy-bmZ03kvfTLL9l41wldsV0tDOu1rfZXB40UsCcnRDNatmeFtYqyW9yCXDK442WtnZE80SjoTweMfuVB8L51F7esmWx8Jc1UrA2rHajzMw' \
        -H'Origin: https://localhost:3000' \
        -H'api-key:vietvivu365.local' \
        -H'content-type:application/json' \
        -d'{"phone_number":"999999999", "id_number":"88888888", "id_number_images":["link1", "link2"]}'
        

```

---


###Vehicle:

#####Vehicle model:
```
    # owner
    owner = StringField()
    # License plate (biển số)
    license_plate = StringField()
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
    # Seat
    seats = IntField()
    # Model
    model = StringField()
    # Description
    description = StringField()
    # Images
    images = ListField()
    # Price
    price_per_day = FloatField()
    # Handover documents
    handover_documents = ListField()
    # Mortgage
    mortgage = ListField()
    # Instant booking
    instant_booking = BooleanField()
    # Deliver
    # - Deliver distance
    # - Deliver fee per km
    # { "deliver_distance": "100 km", "fee_per_km": 30000 }
    delivery = DictField()
    # Limit road
    # - Limit value
    # - Over limit fee per km
    # {"limit_value": 100, "fee_per_km": 30000}
    limit_road = DictField()
    # Licence card
    license_card = StringField()
    # Insurance card
    insurance_card = StringField()
    # Audit card
    audit_card = StringField()
    # Status
    status = StringField()
    # Rating
    rating = FloatField()
    # Number of rating
    number_of_rating = IntField()
```

#####Adding new vehicle:
**Notice**: location must be in the order `[long, lat]`
```
curl -v -XPOST 'localhost:30000/v1/user/vehicle' \
    -H 'Api-Key: vietvivu365.local' \
    -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImRhNWZiMGJkZTJlMzUwMmZkZTE1YzAwMWE0MWIxYzkxNDc4MTI0NzYifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJpcHgtZTk1NWYiLCJuYW1lIjoibG9uZyB0aWVuIiwiYXVkIjoidHJpcHgtZTk1NWYiLCJhdXRoX3RpbWUiOjE1MjExNjQzODksInVzZXJfaWQiOiJON2Q1amVwOFJYWXMxelBTRFFFSmd2TXFRNG4xIiwic3ViIjoiTjdkNWplcDhSWFlzMXpQU0RRRUpndk1xUTRuMSIsImlhdCI6MTUyMTE2NDM5MCwiZXhwIjoxNTIxMTY3OTkwLCJlbWFpbCI6ImxvbmdzeW1ibG9nQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImxvbmdzeW1ibG9nQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.CIP6F3KC6l9e8ohoQWMD_zG-N2fq21SE93s1Wp3pwAdwPURom8BiQ2RG7nVpFivtEaNdZtl6WuJmaY8bVb4cdjb4-PznqboKwID1-SWvo4xR_TAXHQwsFPVn18FGArkjypMW6G5-Ocv6Yxq6gk2Q8jS7WXLD0SFRd82mSA9vvpfmTVj40RZaJZDTAgpfLqUoRpRy-TDK-0mC2duX-pqX4Gq8L8re6KAeeVs7T1aL-IrQZLqXJIdaukP9cSwTdtITKywOOlii8YQcPb4qWzzjKQgb9dfZVZyrEGPY8LnDhfdn7bdNgxGt4lc3p28SA9e1QMfRUTT5ObCBgdtuf102DA' \
    -H 'Content-Type: application/json' \
    -H 'Origin: {allowed_origins}'
    -d '{"license_plate": "72f28821", "address": "vung tau", "location": [107.1106857, 10.3778339], "manufacturer": "bmw", "brand": "bmw", "year": 2019, "transmission": "manual", "engine": "hybrid", "gasoline_consumption_per_100_km": 100, "seats": 5, "model": "xx", "description": "nice car of long ka", "images": ["image1", "image2"], "price_per_day": 10000, "handover_documents": []}'
```
#####Get list all vehicle info of current user

```
GET /v1/user/vehicle
curl -v -XGET 'localhost:30000/v1/user/vehicle' \
        -H 'Api-Key: local' \
        -H 'Origin: {allowed_origins}'
        -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImRhNWZiMGJkZTJlMzUwMmZkZTE1YzAwMWE0MWIxYzkxNDc4MTI0NzYifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJpcHgtZTk1NWYiLCJuYW1lIjoibG9uZyB0aWVuIiwiYXVkIjoidHJpcHgtZTk1NWYiLCJhdXRoX3RpbWUiOjE1MjExNjQzODksInVzZXJfaWQiOiJON2Q1amVwOFJYWXMxelBTRFFFSmd2TXFRNG4xIiwic3ViIjoiTjdkNWplcDhSWFlzMXpQU0RRRUpndk1xUTRuMSIsImlhdCI6MTUyMTI0MDM5NiwiZXhwIjoxNTIxMjQzOTk2LCJlbWFpbCI6ImxvbmdzeW1ibG9nQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImxvbmdzeW1ibG9nQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.aNY7RrbqgvJJYdY-Mcggh9C2eeDYTD8OarmInolLLMBSGu5edlA2av06CvntZqOeJy_tsW8Vgpq2o2MJTN5sXJ_NUNc7vDiJxr52hzAFi0jcbOGN98h4diH9CnggXJ6jkhSSFXO9ahOOHL1tQ6UXHTqLngIL8mXn84vO1rhheGvTnRlysD-9Grv1iEYrmW8O-IIbHYZE73SnaOpS2YhXpK9D8kR95JbNg699f54UEoyHBT-oB2hQJUelIreQKAGflrxgZorgLA31fH071v1zzn24yoJ5Hdzeby6KagKQ2k9Lc8bxdtB18H8UwELL-FI-ek-KLdJx79CCtJlr-iCv9Q'
```

#####Get one vehicle info of current user
```
GET /v1/user/vehicle/{vehicle_id}
curl -v -XGET 'localhost:30000/v1/user/vehicle/5aac51d8737671235eca4657' \
        -H 'Api-Key: local' \
        -H 'Origin: {allowed_origins}' \
        -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImRhNWZiMGJkZTJlMzUwMmZkZTE1YzAwMWE0MWIxYzkxNDc4MTI0NzYifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJpcHgtZTk1NWYiLCJuYW1lIjoibG9uZyB0aWVuIiwiYXVkIjoidHJpcHgtZTk1NWYiLCJhdXRoX3RpbWUiOjE1MjExNjQzODksInVzZXJfaWQiOiJON2Q1amVwOFJYWXMxelBTRFFFSmd2TXFRNG4xIiwic3ViIjoiTjdkNWplcDhSWFlzMXpQU0RRRUpndk1xUTRuMSIsImlhdCI6MTUyMTI0MDM5NiwiZXhwIjoxNTIxMjQzOTk2LCJlbWFpbCI6ImxvbmdzeW1ibG9nQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImxvbmdzeW1ibG9nQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.aNY7RrbqgvJJYdY-Mcggh9C2eeDYTD8OarmInolLLMBSGu5edlA2av06CvntZqOeJy_tsW8Vgpq2o2MJTN5sXJ_NUNc7vDiJxr52hzAFi0jcbOGN98h4diH9CnggXJ6jkhSSFXO9ahOOHL1tQ6UXHTqLngIL8mXn84vO1rhheGvTnRlysD-9Grv1iEYrmW8O-IIbHYZE73SnaOpS2YhXpK9D8kR95JbNg699f54UEoyHBT-oB2hQJUelIreQKAGflrxgZorgLA31fH071v1zzn24yoJ5Hdzeby6KagKQ2k9Lc8bxdtB18H8UwELL-FI-ek-KLdJx79CCtJlr-iCv9Q'
```

#####Get vehicle info of another user (public info)

```
GET /v1/vehicle/{vehicle_id}
# with headers

same as above, but limit the returned fields
```

#####Get public info by slug
```
GET /v1/vehicle/slug/{slug}
# with headers
return vehicle info with limited info
```

#####Edit vehicle info of current user

```
PUT /v1/user/vehicle/{vehicle_id}

curl -v -XPUT 'localhost:30000/v1/user/vehicle/5ab1c34873767115e93b638f' -H'Content-Type:application/json' \ 
            -d '{"delivery":{ "enabled": true, "deliver_distance": "100 km", "fee_per_km": 5000 }, "limit_road":{"enabled": true, "limit_value": 100, "fee_per_km": 5000}, "insurance_card":"test"}'\
            -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImRhNWZiMGJkZTJlMzUwMmZkZTE1YzAwMWE0MWIxYzkxNDc4MTI0NzYifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJpcHgtZTk1NWYiLCJuYW1lIjoibG9uZyBuZ3V5ZW4iLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDQuZ29vZ2xldXNlcmNvbnRlbnQuY29tLy0zMmpGbXVuQnJnOC9BQUFBQUFBQUFBSS9BQUFBQUFBQUNXSS92SG5wUWFWZ05tay9waG90by5qcGciLCJhdWQiOiJ0cmlweC1lOTU1ZiIsImF1dGhfdGltZSI6MTUyMTU1OTAxMiwidXNlcl9pZCI6IjByblk1NUFocXJaYjdUM2QwWUFQeHNCamdSYjIiLCJzdWIiOiIwcm5ZNTVBaHFyWmI3VDNkMFlBUHhzQmpnUmIyIiwiaWF0IjoxNTIxNzMzNjQ2LCJleHAiOjE1MjE3MzcyNDYsImVtYWlsIjoibmd1eWVudGllbmxvbmc4OEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjEwNDYzNTM5NzQ3ODI3OTI5NTUyNCJdLCJlbWFpbCI6WyJuZ3V5ZW50aWVubG9uZzg4QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.MseW3xdezEwd01mcAproC-IYWTnbSp8puEHi1d2uQxgMh8aBC38qS6xcNlMzr04zlV1uJ92lG3zv40mgipcUVX9qG3XBgIQAH2JQ9ealo8xjijGi9IoZdZYXoKVBg9jYEc_SC9pdxEL5cgWvgDXfDXHcjHL_N_rl8oR8u7X7pxSvvmDwIs87Gt-OSSUoGr-ChfFqu1GVNyTMgYgqqC3UNWGVi7zH8I5FWRF5aoYwfMA-ddToQno8HpMEM6z9ryZomldyAo0nY5Ps8InyhrKRBKJLcIwu-UK2r2hCrC_SuvA-J5k7YuxO7FAF3sJDIrn84d2sj4hlLtpCUJQXJ_vX3Q' \
            -H 'Api-Key: vietvivu365.local'\
            -H 'Origin: localhost'
            
200 OK - if success
400 Bad Request - if data not valid, attribute not valid
```
#####Delete vehicle of current user
```
DELETE /v1/user/vehicle/{vehicle_id}
// -H 'Origin: {allowed_origins}'
// todo add more desc
```

#####Get vehicle list:
No need token to get vehicle list
```
curl -v -XGET 'localhost:30000/v1/vehicle' \
    -H 'Api-Key: vietvivu365.local' \
    -H 'Origin: {allowed_origins}' \
    -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImRhNWZiMGJkZTJlMzUwMmZkZTE1YzAwMWE0MWIxYzkxNDc4MTI0NzYifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJpcHgtZTk1NWYiLCJuYW1lIjoibG9uZyB0aWVuIiwiYXVkIjoidHJpcHgtZTk1NWYiLCJhdXRoX3RpbWUiOjE1MjExNjQzODksInVzZXJfaWQiOiJON2Q1amVwOFJYWXMxelBTRFFFSmd2TXFRNG4xIiwic3ViIjoiTjdkNWplcDhSWFlzMXpQU0RRRUpndk1xUTRuMSIsImlhdCI6MTUyMTE2NDM5MCwiZXhwIjoxNTIxMTY3OTkwLCJlbWFpbCI6ImxvbmdzeW1ibG9nQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImxvbmdzeW1ibG9nQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.CIP6F3KC6l9e8ohoQWMD_zG-N2fq21SE93s1Wp3pwAdwPURom8BiQ2RG7nVpFivtEaNdZtl6WuJmaY8bVb4cdjb4-PznqboKwID1-SWvo4xR_TAXHQwsFPVn18FGArkjypMW6G5-Ocv6Yxq6gk2Q8jS7WXLD0SFRd82mSA9vvpfmTVj40RZaJZDTAgpfLqUoRpRy-TDK-0mC2duX-pqX4Gq8L8re6KAeeVs7T1aL-IrQZLqXJIdaukP9cSwTdtITKywOOlii8YQcPb4qWzzjKQgb9dfZVZyrEGPY8LnDhfdn7bdNgxGt4lc3p28SA9e1QMfRUTT5ObCBgdtuf102DA' \
```

#####Search vehicle
Search by timestamp

For pagination, append `page=x&item_perpage=y` into url query string


Search by `from_ts` to `to_ts`
```
 curl -XGET 'localhost:30000/v1/vehicle?from_ts=1522908043&to_ts=1523070554' \
 -H'origin:localhost'\
 -H'api-key:vietvivu365.local'
```

Search by `from_ppd`, `to_ppd` (ppd=price per day)
```
curl -XGET -H'origin:localhost' \
    -H'api-key:vietvivu365.local' \
    'localhost:30000/v1/vehicle?from_ts=1522908043&to_ts=1523070554&from_ppd=9000&to_ppd=10000'
```

Search by `instant_booking`, only accept value range for True: `['true', '1']` from client side
```
curl -XGET -H'origin:localhost' \
    -H'api-key:vietvivu365.local' \
    'localhost:30000/v1/vehicle?from_ts=1522908043&to_ts=1523070554&from_ppd=9000&to_ppd=10000&instant_booking=true'
```

Search by `delivery` (delivery.enabled=True), only accept value range for True: `['true', '1']` from client side
```
curl -XGET -H'origin:localhost' \
    -H'api-key:vietvivu365.local' \
    'localhost:30000/v1/vehicle?from_ts=1522908043&to_ts=1523070554&from_ppd=9000&to_ppd=10000&delivery=true'
```

Search by `seats`. [4,7] is available value for search

Search by multiple seat option `seats=4,7`
```
curl -XGET -H'origin:localhost' \
    -H'api-key:vietvivu365.local' \
    'localhost:30000/v1/vehicle?from_ts=1522908043&to_ts=1523070554&from_ppd=9000&to_ppd=10000&seats=4,7'
```

Search by `['manufacturer', 'brand', 'year', 'transmission', 'engine', 'model', 'seats']`
```
curl -XGET -H'origin:localhost' \
    -H'api-key:vietvivu365.local' \
    'localhost:30000/v1/vehicle?from_ts=1522908043&to_ts=1523070554&from_ppd=9000&to_ppd=10000&engine=hybrid&transmission=auto'
```

Search by `long, lat, r`
if `r` is not specified, default r is `30` km
```
curl -v -XGET 'localhost:30000/v1/vehicle?location=100.1,10,30' \
    -H'origin:localhost' \
    -H'api-key:vietvivu365.local'
```

##### Manufacturer, brand, model

**Manufacturer**

For pagination, append `page=x&item_perpage=y` into url query string
```
curl -XGET 'localhost:30000/v1/vehicle/manufacturer' \
    -H'origin:localhost' \
    -H'api-key:vietvivu365.local'
```
**Brand**

For pagination, append `page=x&item_perpage=y` into url query string

```
curl -XGET 'localhost:30000/v1/vehicle/brand/bmw' \
    -H'origin:localhost' \
    -H'api-key:vietvivu365.local'
```

**Model**

For pagination, append `page=x&item_perpage=y` into url query string

```
curl -XGET 'localhost:30000/v1/vehicle/model' \
    -H'origin:localhost' \
    -H'api-key:vietvivu365.local'
```

#####User subscription
```
Request:
    
    POST /v1/user/subscribe \
        -H 'Api-Key: {client_key}'
        -H 'Content-Type: application/json' -d 'data.json'
        -H 'Origin: {allowed_origins}'

Response:
    
        200 OK
        400 Bad Request
        403 Not allow origin domain
    
```

---

#####Booking
**Create a booking**
```
curl -v -XPOST 'http://localhost:30000/v1/booking/dsXpLWe5bLQdeX1ONSjeNPFBw0f2/5adc40f0737671396a8174c4' \
                    -H'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ5NGQ1ZjMyZTE4NmRjMWUxNjA0MjhiZDdhODE1NDI2ZjI3NDg4MmIifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJpcHgtc3RhZy05MjRlZSIsIm5hbWUiOiJsb25na2EiLCJhdWQiOiJ0cmlweC1zdGFnLTkyNGVlIiwiYXV0aF90aW1lIjoxNTI1NTY5MzkxLCJ1c2VyX2lkIjoiZHNYcExXZTViTFFkZVgxT05TamVOUEZCdzBmMiIsInN1YiI6ImRzWHBMV2U1YkxRZGVYMU9OU2plTlBGQncwZjIiLCJpYXQiOjE1MjU1NjkzOTEsImV4cCI6MTUyNTU3Mjk5MSwiZW1haWwiOiJuZ3V5ZW4udGllbi5sb25nQGlwcmljZWdyb3VwLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm5ndXllbi50aWVuLmxvbmdAaXByaWNlZ3JvdXAuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.XCM6pqnJcWBssMbypyoI1ytZkPTgAQ00fyds8pyP2Fxuh6zj4GzROuW1I0HJLmCKhm5UxyrTxsc3YlRoQNZGQ-irW8jfIo0eDahgksAumvpWMdbHXU_vFn8wbPHGb0j7pzSlEhA6ZARYaTon-GsAVgviUqKGYMvU_2oKk62BLR0mion_nx4hQKYPdebtlsLunosa9JJXagKgOLG7JFn75M2wFZqP3uoSDTduPlOPWQBw8zBSguNtteWyzwGk6e5rnRlrriAPvXaR3hXHSWrhXtESB-qIzhYRPzqI6N2LBGN8TvzFLZgISsGaq0YWMXHGdKfQD7TdeiqLb3YzMqrXzg' \
                    -H'Origin: http://localhost:3000' \
                    -H'api-key:vietvivu365.local' \
                    -H'content-type:application/json' \
                    -d'{"from":1535914180, "to":1536346180, "total_price":100000, "service_type":"free"}'
```
                    
**Response:**

```
//short_id is the same as order_id concept (for eg: #XYZ123)

{
  "status": "success",
  "message": "Booking number #VMX5WE initialized",
  "data": {
    "booking": {
      "_id": {
        "$oid": "5aee6129737671433a78f04f"
      },
      "short_id": "VMX5WE",
      "user": "dsXpLWe5bLQdeX1ONSjeNPFBw0f2",
      "vehicle": "5adc40f0737671396a8174c4",
      "phases": [
        {
          "initialized": {
            "date_time": 1525546681.083708
          }
        }
      ],
      "current_phase": "initialized",
      "reserved_date_time": {
        "from": 1535914180,
        "to": 1536346180
      },
      "created_date_time": 1525546636
    }
  }
}

```

**Update:**
```
update status:
    + from: initialized -> accepted/rejected/cancled -> canceled/done
    
curl -v -XPUT 'http://localhost:30000/v1/user/booking/V7HSUF' \
                -H'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ5NGQ1ZjMyZTE4NmRjMWUxNjA0MjhiZDdhODE1NDI2ZjI3NDg4MmIifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJpcHgtc3RhZy05MjRlZSIsIm5hbWUiOiJsb25na2EiLCJhdWQiOiJ0cmlweC1zdGFnLTkyNGVlIiwiYXV0aF90aW1lIjoxNTI1NTY5MzkxLCJ1c2VyX2lkIjoiZHNYcExXZTViTFFkZVgxT05TamVOUEZCdzBmMiIsInN1YiI6ImRzWHBMV2U1YkxRZGVYMU9OU2plTlBGQncwZjIiLCJpYXQiOjE1MjU1NjkzOTEsImV4cCI6MTUyNTU3Mjk5MSwiZW1haWwiOiJuZ3V5ZW4udGllbi5sb25nQGlwcmljZWdyb3VwLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm5ndXllbi50aWVuLmxvbmdAaXByaWNlZ3JvdXAuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.XCM6pqnJcWBssMbypyoI1ytZkPTgAQ00fyds8pyP2Fxuh6zj4GzROuW1I0HJLmCKhm5UxyrTxsc3YlRoQNZGQ-irW8jfIo0eDahgksAumvpWMdbHXU_vFn8wbPHGb0j7pzSlEhA6ZARYaTon-GsAVgviUqKGYMvU_2oKk62BLR0mion_nx4hQKYPdebtlsLunosa9JJXagKgOLG7JFn75M2wFZqP3uoSDTduPlOPWQBw8zBSguNtteWyzwGk6e5rnRlrriAPvXaR3hXHSWrhXtESB-qIzhYRPzqI6N2LBGN8TvzFLZgISsGaq0YWMXHGdKfQD7TdeiqLb3YzMqrXzg' \
                -H'Origin: http://localhost:3000' \
                -H'api-key:vietvivu365.local' \
                -H'content-type:application/json' \
                -d'{"status": "canceled", "service_type":"free"}'
```

---

**Get booking history**

***Renter***
```
GET /v1/booking/history/renter

curl -v -XGET 'http://localhost:30000/v1/booking/history/renter' \
-H'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjhiZjA2YWU3MGJhMjVkNzZiNWM0ZjMyYTk4YTU0N2JlYjE4YmM0MGUifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJpcHgtc3RhZy05MjRlZSIsIm5hbWUiOiJsb25na2EiLCJhdWQiOiJ0cmlweC1zdGFnLTkyNGVlIiwiYXV0aF90aW1lIjoxNTI0MDEyNTQ1LCJ1c2VyX2lkIjoielBURnhQYjk2Q05KelhHcnpGMDhWWUxyN3MyMyIsInN1YiI6InpQVEZ4UGI5NkNOSnpYR3J6RjA4VllMcjdzMjMiLCJpYXQiOjE1MjYwMDU1OTksImV4cCI6MTUyNjAwOTE5OSwiZW1haWwiOiJuZ3V5ZW50aWVubG9uZzg4QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImZhY2Vib29rLmNvbSI6WyIxMDIwOTA0MjY1OTAyMzI2NyJdLCJlbWFpbCI6WyJuZ3V5ZW50aWVubG9uZzg4QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6ImZhY2Vib29rLmNvbSJ9fQ.KlckvRMQfWemy818m2P8nhxlwi43qG0P49D98PzMgSkpxkMt6FS6FU8ASIty6PcZR1MA9Qtfv-7SvaqTaycYcNBQzIrEuAzywFtQFe6WV0XJ9yqDihzuCqdtY6ZMW9OY3I-Z8J0JWR_xgN85Tp6eoalQb_hdOAJCF3ym8PxnAwmOk6Lgs9xCmN7CGsZXR8qyH6DJdTdznJZMUuJg4M8__r-Xkj5cIQ4J930DQ8za63ZpNbRVMI1rDHGjtsmkA7JXW548opQ3U1Lu-d-QEzKcoCDkw5xZ1IihOR5N0-k5KfdWDytecGfyyopt3gUnhLVhu2OVBsqb47fDAEzW-T5Y1A' \
-H'Origin: https://localhost:3000' \
-H'api-key:vietvivu365.local'

```

***Vehicle owner***
```
Get all booking history of all vehicles

GET /v1/booking/history/owner

curl -v -XGET 'http://localhost:30000/v1/booking/history/owner' \
-H'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjhiZjA2YWU3MGJhMjVkNzZiNWM0ZjMyYTk4YTU0N2JlYjE4YmM0MGUifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJpcHgtc3RhZy05MjRlZSIsIm5hbWUiOiJsb25na2EiLCJhdWQiOiJ0cmlweC1zdGFnLTkyNGVlIiwiYXV0aF90aW1lIjoxNTI0MDEyNTQ1LCJ1c2VyX2lkIjoielBURnhQYjk2Q05KelhHcnpGMDhWWUxyN3MyMyIsInN1YiI6InpQVEZ4UGI5NkNOSnpYR3J6RjA4VllMcjdzMjMiLCJpYXQiOjE1MjYwMDU1OTksImV4cCI6MTUyNjAwOTE5OSwiZW1haWwiOiJuZ3V5ZW50aWVubG9uZzg4QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImZhY2Vib29rLmNvbSI6WyIxMDIwOTA0MjY1OTAyMzI2NyJdLCJlbWFpbCI6WyJuZ3V5ZW50aWVubG9uZzg4QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6ImZhY2Vib29rLmNvbSJ9fQ.KlckvRMQfWemy818m2P8nhxlwi43qG0P49D98PzMgSkpxkMt6FS6FU8ASIty6PcZR1MA9Qtfv-7SvaqTaycYcNBQzIrEuAzywFtQFe6WV0XJ9yqDihzuCqdtY6ZMW9OY3I-Z8J0JWR_xgN85Tp6eoalQb_hdOAJCF3ym8PxnAwmOk6Lgs9xCmN7CGsZXR8qyH6DJdTdznJZMUuJg4M8__r-Xkj5cIQ4J930DQ8za63ZpNbRVMI1rDHGjtsmkA7JXW548opQ3U1Lu-d-QEzKcoCDkw5xZ1IihOR5N0-k5KfdWDytecGfyyopt3gUnhLVhu2OVBsqb47fDAEzW-T5Y1A' \
-H'Origin: https://localhost:3000' \
-H'api-key:vietvivu365.local'

```

```
Get all booking history of a vehicle

GET /v1/booking/history/owner?vehicle_id=﻿{vehicle_id}
GET /v1/booking/history/owner?vehicle_slug=﻿{vehicle_slug}
GET /v1/booking/history/owner?short_id=﻿{short_id}

curl -v -XGET 'http://localhost:30000/v1/booking/history/owner?vehicle_id=﻿5af319161d41c84557affa90' \
-H'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjhiZjA2YWU3MGJhMjVkNzZiNWM0ZjMyYTk4YTU0N2JlYjE4YmM0MGUifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJpcHgtc3RhZy05MjRlZSIsIm5hbWUiOiJsb25na2EiLCJhdWQiOiJ0cmlweC1zdGFnLTkyNGVlIiwiYXV0aF90aW1lIjoxNTI0MDEyNTQ1LCJ1c2VyX2lkIjoielBURnhQYjk2Q05KelhHcnpGMDhWWUxyN3MyMyIsInN1YiI6InpQVEZ4UGI5NkNOSnpYR3J6RjA4VllMcjdzMjMiLCJpYXQiOjE1MjYwMDU1OTksImV4cCI6MTUyNjAwOTE5OSwiZW1haWwiOiJuZ3V5ZW50aWVubG9uZzg4QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImZhY2Vib29rLmNvbSI6WyIxMDIwOTA0MjY1OTAyMzI2NyJdLCJlbWFpbCI6WyJuZ3V5ZW50aWVubG9uZzg4QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6ImZhY2Vib29rLmNvbSJ9fQ.KlckvRMQfWemy818m2P8nhxlwi43qG0P49D98PzMgSkpxkMt6FS6FU8ASIty6PcZR1MA9Qtfv-7SvaqTaycYcNBQzIrEuAzywFtQFe6WV0XJ9yqDihzuCqdtY6ZMW9OY3I-Z8J0JWR_xgN85Tp6eoalQb_hdOAJCF3ym8PxnAwmOk6Lgs9xCmN7CGsZXR8qyH6DJdTdznJZMUuJg4M8__r-Xkj5cIQ4J930DQ8za63ZpNbRVMI1rDHGjtsmkA7JXW548opQ3U1Lu-d-QEzKcoCDkw5xZ1IihOR5N0-k5KfdWDytecGfyyopt3gUnhLVhu2OVBsqb47fDAEzW-T5Y1A' \
-H'Origin: https://localhost:3000' \
-H'api-key:vietvivu365.local'

```

**Get renter|owner information in booking history**

**Request**

```
GET /v1/booking/info/{user_type}/{booking_short_id}/{user_id}

curl -v -XGET 'http://localhost:30000/v1/booking/info/renter/E62R69/zPTFxPb96CNJzXGrzF08VYLr7s23' \
-H'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjhiZjA2YWU3MGJhMjVkNzZiNWM0ZjMyYTk4YTU0N2JlYjE4YmM0MGUifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJpcHgtc3RhZy05MjRlZSIsIm5hbWUiOiJsb25na2EiLCJhdWQiOiJ0cmlweC1zdGFnLTkyNGVlIiwiYXV0aF90aW1lIjoxNTI1NTY5MzkxLCJ1c2VyX2lkIjoiZHNYcExXZTViTFFkZVgxT05TamVOUEZCdzBmMiIsInN1YiI6ImRzWHBMV2U1YkxRZGVYMU9OU2plTlBGQncwZjIiLCJpYXQiOjE1MjYwOTkwMTAsImV4cCI6MTUyNjEwMjYxMCwiZW1haWwiOiJuZ3V5ZW4udGllbi5sb25nQGlwcmljZWdyb3VwLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm5ndXllbi50aWVuLmxvbmdAaXByaWNlZ3JvdXAuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.PYIirihTGRbedjYXp3slHolMPUddl0dht1F-OuOJ3JFSbYl3SsJNqLKeKSDhFk4d2l9OzotSctkItPgiMDtuZocAWJUrMy8Yzqpyae-YQUmOfF-D_IkwpV8DFa-9FnlTozmcik5W_rJmNO13_5YbzoQhsanoFTbWZ8LtAflnLvbdmlXWk7-jVOOeBcQ_vIihhLSrittUVivwSmHTLg5-YDmAboI9PM-9FZqVrVMANc97dYTCSnarp3xA9Hm98nL0jDJbNtoEEjJog3KLsRouzvkNSC9D_PY4BEiO6rU-IEfQx86EBOIqxKnaQb21Zya_88svfYTEwmYfF25eg5Xs-Q' \
-H'Origin: https://localhost:3000' \
-H'api-key:vietvivu365.local'


curl -v -XGET 'http://localhost:30000/v1/booking/info/owner/E7U6NL/dsXpLWe5bLQdeX1ONSjeNPFBw0f2' \
-H'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjhiZjA2YWU3MGJhMjVkNzZiNWM0ZjMyYTk4YTU0N2JlYjE4YmM0MGUifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJpcHgtc3RhZy05MjRlZSIsIm5hbWUiOiJsb25na2EiLCJhdWQiOiJ0cmlweC1zdGFnLTkyNGVlIiwiYXV0aF90aW1lIjoxNTI1NTY5MzkxLCJ1c2VyX2lkIjoiZHNYcExXZTViTFFkZVgxT05TamVOUEZCdzBmMiIsInN1YiI6ImRzWHBMV2U1YkxRZGVYMU9OU2plTlBGQncwZjIiLCJpYXQiOjE1MjYwOTkwMTAsImV4cCI6MTUyNjEwMjYxMCwiZW1haWwiOiJuZ3V5ZW4udGllbi5sb25nQGlwcmljZWdyb3VwLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm5ndXllbi50aWVuLmxvbmdAaXByaWNlZ3JvdXAuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.PYIirihTGRbedjYXp3slHolMPUddl0dht1F-OuOJ3JFSbYl3SsJNqLKeKSDhFk4d2l9OzotSctkItPgiMDtuZocAWJUrMy8Yzqpyae-YQUmOfF-D_IkwpV8DFa-9FnlTozmcik5W_rJmNO13_5YbzoQhsanoFTbWZ8LtAflnLvbdmlXWk7-jVOOeBcQ_vIihhLSrittUVivwSmHTLg5-YDmAboI9PM-9FZqVrVMANc97dYTCSnarp3xA9Hm98nL0jDJbNtoEEjJog3KLsRouzvkNSC9D_PY4BEiO6rU-IEfQx86EBOIqxKnaQb21Zya_88svfYTEwmYfF25eg5Xs-Q' \
-H'Origin: https://localhost:3000' \
-H'api-key:vietvivu365.local'
```
**Response**

***Owner view renter info of a booking***

```

HTTP/1.1 200 OK

{
   "data" : {
      "renter" : {
         "feedbacks" : [
            {
               "user" : {
                  "name" : "Teo",
                  "avatar" : "image",
                  "id" : "hRNMPVsIWYTbis9Ox92gpeAh1Bl1"
               },
               "rating" : 5,
               "comment" : "Good service",
               "created_date_time" : 1526101785
            },
            {
               "rating" : 5,
               "user" : {
                  "name" : "Ti",
                  "avatar" : "image",
                  "id" : "hRNMPVsIWYTbis9Ox92gpeAh1Bl1"
               },
               "comment" : "Good service",
               "created_date_time" : 1526101785
            }
         ],
         "phone_number" : "999999999",
         "_id" : "zPTFxPb96CNJzXGrzF08VYLr7s23",
         "avatar" : "https://google.com/longka",
         "email" : "nguyentienlong88@gmail.com",
         "created_date" : 1524357655,
         "id_number" : "88888888",
         "_cls" : "User",
         "name" : "longka"
      },
   },
   "status" : "success"
}

```

***Renter view an owner info of a booking***
```
HTTP/1.1 200 OK

{
   "status" : "success",
   "data" : {
      "owner" : {
         "created_date" : 1526291918,
         "name" : "longka",
         "email" : "nguyen.tien.long@ipricegroup.com",
         "_id" : "dsXpLWe5bLQdeX1ONSjeNPFBw0f2",
         "_cls" : "User"
      },
      "vehicle" : [
         {
            "license_plate" : "123F",
            "feedbacks" : [
               {
                  "comment" : "test",
                  "short_booking_id" : "3MDA2R",
                  "created_date_time" : 1526631613,
                  "rating" : 5,
                  "id" : "7Y36C2",
                  "user" : {
                     "name" : "longka",
                     "id" : "dsXpLWe5bLQdeX1ONSjeNPFBw0f2",
                     "avatar" : null
                  }
               },
               {
                  "created_date_time" : 1526631720,
                  "comment" : "test",
                  "short_booking_id" : "3MDA2R",
                  "user" : {
                     "name" : "longka",
                     "avatar" : null,
                     "id" : "dsXpLWe5bLQdeX1ONSjeNPFBw0f2"
                  },
                  "id" : "L8LPK1",
                  "rating" : 5
               }
            ],
            "address" : "vung tau"
         }
      ]
   }
}
```

**Error**
```
HTTP/1.1 400 Bad Request
{
   "message" : "Owner zPTFxPb96CNJzXGrzF08VYLr7s23 can't view info of this renter zPTFxPb96CNJzXGrzF08VYLr7s23",
   "status" : "failed"
}
```
---

#####Feedback

**Give feed back**

Owner give feedback to renter
Renter give feedback vehicle of owner

```
** Request **
    
    POST /v1/feedback/booking_short_id
        -d '{"rating":5.0, "comment":"test"}' \
        -H 'origin: https://stag-web.vietvivu365.vn' \
        -H 'api-key:vietvivu365.local' \
        -H 'content-type:application/json' \
        -H 'Authorization: Bearer {token}' 

** Response **

    200 with valid json string IF success
```

***example: renter give feedback to a vehicle ***
```
curl -v -XPOST 'https://stag-api.vietvivu365.vn/v1/feedback/UC75HB' \
-d '{"rating":5.0, "comment":"good nak"}' \
-H 'origin: https://stag-web.vietvivu365.vn' \
-H 'api-key:vietvivu365.local' \
-H 'content-type:application/json' \
-H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjEyMDUwYzMxN2ExMjJlZDhlMWZlODdkN2FhZTdlMzk3OTBmNmMwYjQifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJpcHgtc3RhZy05MjRlZSIsIm5hbWUiOiJMZSB0cnVuZyBoaWV1IiwiYXVkIjoidHJpcHgtc3RhZy05MjRlZSIsImF1dGhfdGltZSI6MTUyNjkxOTk2OSwidXNlcl9pZCI6IlprRk1aOWl2WEFUTkNzWU1XQk5lMmlmS25vVzIiLCJzdWIiOiJaa0ZNWjlpdlhBVE5Dc1lNV0JOZTJpZktub1cyIiwiaWF0IjoxNTI2OTE5OTc0LCJleHAiOjE1MjY5MjM1NzQsImVtYWlsIjoibGV0cnVuZ2hpZXUzN0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJsZXRydW5naGlldTM3QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.JLmHO7IKYypLE7e74GWHFTz8sEdsi7Zf-AcBTCPJ6GKMitasQ1Z5SYIkUPinnKmrIH-Q37WX2z7aL6OiK-AX-Cc5523KUaUGEZnOQre413NU7zG2TVK_BVHyarC2vOK0VIJfqjHRNfFfwS0-LYKP_16UbC-YyDdHkG-GvoEm8nC1yj78mSwjIONVJcmP-lKkZIcunPXViLF1PwLViN1L_QorE1ChxLPsSAU6TaarAirQFm4n4jEFqWWfVD3tEtAzqVUAKiiD0hfvFDOcKrqYdgVqf2JMpD4SXK2ZOClMhrlULlnSZjb74PdufJnEvxPGLVcTXeGBQfc0GKLfKYhgRA'
```

```
**response of example**


{
   "status" : "success",
   "message" : "Feedback id #A5W3ZN submitted",
   "data" : {
      "feedback" : {
         "rating" : 5,
         "vehicle" : {
            "id" : "5adc40f0737671396a8174c4"
         },
         "user" : {
            "name" : "longka",
            "avatar" : null,
            "id" : "zPTFxPb96CNJzXGrzF08VYLr7s23"
         },
         "comment" : "test",
         "created_date_time" : 1526619675,
         "short_booking_id" : "3MDA2R",
         "id" : "A5W3ZN"
      }
   }
}
```
