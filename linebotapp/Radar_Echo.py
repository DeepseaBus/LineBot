import requests


def weather_pridict():
    url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0058-003?Authorization=rdec-key-123-45678-011121314&format=JSON'
    res_get = requests.get(url)
    radar_echo = res_get.json()

    image_url = radar_echo['cwbopendata']['dataset']['resource']['uri']

    post_url = 'https://2b79-2001-b011-3819-ddb7-3dd0-5d99-6cbb-8eed.jp.ngrok.io/Weather_Predict'
    res_post = requests.post(post_url, image_url)


weather_pridict()
