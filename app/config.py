import os
import configparser

INI_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '../conf/app.ini'
)

CONFIG = configparser.ConfigParser()
CONFIG.read(INI_FILE)

# APP ENV
APP_ENV = CONFIG['env']['app_env']

# Logger
LOG_LEVEL = CONFIG['logging']['level']

# Auth
AUTH_SECRET = CONFIG['auth']['secret']
AUTH_TOKEN_EXPIRATION_SECONDS = CONFIG['auth']['token_expiration_seconds']
AUTH_DEFAULT_TOKEN_OPTS = {"name": "x-token", "location": "header"}
AUTH_ALGORITHM = CONFIG['auth']['algorithm']

# DB connection
DB_HOST = CONFIG['mongodb']['host']
DB_NAME = CONFIG['mongodb']['name']
DB_PORT = CONFIG['mongodb']['port']

# Mailchimp api
MC_API_KEY = CONFIG['mailchimp']['api_key']
MC_CAMPAIGN_ID = CONFIG['mailchimp']['campaign_id']

# CORS
ALLOWED_ORIGINS = CONFIG['cors']['allowed_origins']
ALLOWED_HEADERS = CONFIG['cors']['allowed_headers']
ALLOWED_METHODS = CONFIG['cors']['allowed_methods']

# maximum unfinished_trip
MAXIMUM_UNFINISHED_TRIPS = CONFIG['booking']['maximum_unfinished_trips']

# item_per_page
ITEM_PER_PAGE = 20

# Email
EMAIL_PROVIDER = CONFIG['email']['provider']
EMAIL_API_KEY = CONFIG['email']['api_key']
FROM_EMAIL = CONFIG['email']['from']
EMAIL_OPERATION_MAIL_LIST = CONFIG['email']['operation_mail_list']

# UUID
UUID_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZ"
WOLVERINE_ID_LENGTH = 5
BOOKING_ID_LENGTH = 6
FEEDBACK_ID_LENGTH = 6

# MIZU
MIZU_BASE_URL = CONFIG['mizu']['base_url']


# VEHICLE IMAGE TYPES
VEHICLE_IMAGE_VEHICLE_TYPE = "vehicle"
VEHICLE_IMAGE_LICENSE_TYPE = "license"
VEHICLE_IMAGE_INSURANCE_TYPE = "insurance"
VEHICLE_IMAGE_AUDIT_TYPE = "audit"

RENTER = 'renter'
OWNER = 'owner'

# HOURS BEFORE LAST DAY OF A BOOKING
HOURS_TO_GIVE_VEHICLE_BACK_TO_OWNER = 2

# Allowed API keys
ALLOWED_API_KEYS = CONFIG['api_keys']
