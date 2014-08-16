# -*- coding: utf-8 -*-

import os
import hashlib
import hmac
import requests
from urlparse import urljoin
import time
import json

from django.conf import settings

def call_api(url, body=None, api_key=None, secret_key=None):

    if not api_key:
        api_key = settings.COINBASE_API_KEY
    if not secret_key:
        secret_key = settings.COINBASE_API_KEY_SECRET

    opener = urllib2.build_opener()
    nonce = int(time.time() * 1e6)
    message = str(nonce) + url + ('' if body is None else body)
    signature = hmac.new(secret_key, message, hashlib.sha256).hexdigest()


    headers = {
        'ACCESS_KEY' : api_key,
        'ACCESS_SIGNATURE': signature,
        'ACCESS_NONCE': nonce,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # If we are passing data, a POST request is made. Note that content_type is specified as json.
    if body:
        req = requests.post(url, headers=headers, params=body)
    # If body is nil, a GET request is made.
    else:
        req = requests.get(url, headers=headers)

    return req.json()
