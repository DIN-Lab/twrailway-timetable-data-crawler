import os
import hmac
import base64
import requests

from time import mktime
from hashlib import sha1
from datetime import datetime
from dotenv import load_dotenv
from wsgiref.handlers import format_date_time

load_dotenv()

PTX_TIMETABLE_JSON_BASE_URL = os.environ.get('PTX_TIMETABLE_JSON_BASE_URL')


class Auth():
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_headers(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'X-Date': xdate
        }


def get_trains(date_string, app_id, app_key):
    auth = Auth(app_id, app_key)
    url = PTX_TIMETABLE_JSON_BASE_URL.format(date_string)
    response = requests.get(url, headers=auth.get_auth_headers())
    return response.json()
