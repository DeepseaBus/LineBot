import requests
import urllib.request
import json
import time

GOOGLE_API_KEY = 'AIzaSyAo43MRwSk1RG2H5Jy_-KbnwwwSyrNFFSY'


def get_latitude_longtitude(address):
    # decode url
    address = urllib.request.quote(address)
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address + '&key=' + GOOGLE_API_KEY

    while True:
        res = requests.get(url)
        js = json.loads(res.text)

        if js["status"] != "OVER_QUERY_LIMIT":
            time.sleep(1)
            break

    result = js["results"][0]["geometry"]["location"]
    lat = result["lat"]
    lng = result["lng"]
    print(lat, lng)
    return lat, lng
get_latitude_longtitude("新北市樹林區太元街69號")