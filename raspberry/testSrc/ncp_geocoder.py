import sys
import os
import hashlib
import hmac
import base64
import requests
import time

def make_signature():
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    access_key = "{accessKey}"                # access key id (from portal or sub account)
    secret_key = "{secretKey}"                # secret key (from portal or sub account)
    secret_key = bytes(secret_key, 'UTF-8')

    method = "GET"
    uri = "/photos/puppy.jpg?query1=&query2"

    message = method + " " + uri + "\n" + timestamp + "\n"
    + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey


#https://geolocation.apigw.ntruss.com/geolocation/v2/geoLocation
#https://geolocation.apigw.ntruss.com/geolocation/v2
