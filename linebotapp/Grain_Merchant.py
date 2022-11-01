import requests
from bs4 import BeautifulSoup
import csv
import os
import time

# ======LINE API=========
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
# =======================

from linebotapp.address_to_coordinate import *


# Grain search URL
def grain_merchant(address, latitude_o, longitude_o):
    st_time = time.time()
    print("地址：", address, "緯度：", latitude_o, "經度：", longitude_o)

    url = 'https://data.coa.gov.tw/Service/OpenData/FromM/FoodBusinessData.aspx?$top=500&$skip=0'
    region_list = ['基隆市', '台北市', '新北市', '宜蘭縣', '桃園市', '新竹市', '新竹縣', '苗栗縣', '台中市', '彰化縣', '南投縣', '雲林縣', '嘉義市', '嘉義縣',
                   '台南市', '高雄市', '屏東縣', '花蓮縣', '台東縣', '澎湖縣', '金門縣', '連江縣']

    for region in region_list:
        try:
            if region in address:
                user_region = region
        except:
            return TextSendMessage(text='此位置無法查詢，請再嘗試搜尋其他位置')

    res_get = requests.get(url)
    a = res_get.json()
    contents = dict()
    contents['type'] = 'carousel'
    bubbles = []
    i = 1
    for b in a:
        ed_time = time.time()
        if i <= 10 and user_region in b['營業地址'] and int(ed_time - st_time) <= 15:
            latitude_b, longitude_b = get_latitude_longtitude(b['營業地址'])
            if abs(latitude_o - latitude_b) < 0.1 and abs(longitude_o - longitude_b) < 0.1:
                bubble = {"type": "bubble",
                          "body": {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                  {
                                      "type": "text",
                                      "text": b['公司或商號名稱'],
                                      "weight": "bold",
                                      "size": "xxl",
                                      "margin": "md",
                                      "wrap": True,
                                      "style": "normal"
                                  },
                                  {
                                      "type": "text",
                                      "text": "聯絡資訊",
                                      "margin": "md",
                                      "size": "lg",
                                      "align": "start",
                                      "decoration": "none"
                                  },
                                  {
                                      "type": "separator"
                                  },
                                  {
                                      "type": "box",
                                      "layout": "horizontal",
                                      "contents": [
                                          {
                                              "type": "text",
                                              "text": "電話:" + b['糧商電話號碼'],
                                              "size": "sm",
                                              "wrap": True
                                          }
                                      ],
                                      "margin": "sm"
                                  },
                                  {
                                      "type": "box",
                                      "layout": "horizontal",
                                      "contents": [
                                          {
                                              "type": "text",
                                              "text": "地址:" + b['營業地址'],
                                              "size": "sm"
                                          }
                                      ],
                                      "margin": "sm"
                                  },
                                  {
                                      "type": "separator",
                                      "margin": "xxl"
                                  },
                                  {
                                      "type": "text",
                                      "text": "經營業務種類",
                                      "margin": "md",
                                      "size": "lg",
                                      "align": "start"
                                  },
                                  {
                                      "type": "box",
                                      "layout": "vertical",
                                      "margin": "sm",
                                      "spacing": "sm",
                                      "contents": [
                                          {
                                              "type": "text",
                                              "text": b['經營業務種類'],
                                              "size": "sm",
                                              "wrap": True,
                                              "align": "start"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "separator",
                                      "margin": "xxl"
                                  },
                                  {
                                      "type": "text",
                                      "text": "經營糧食種類",
                                      "margin": "md",
                                      "align": "start",
                                      "size": "lg"
                                  },
                                  {
                                      "type": "box",
                                      "layout": "vertical",
                                      "margin": "sm",
                                      "spacing": "sm",
                                      "contents": [
                                          {
                                              "type": "text",
                                              "text": b['經營糧食種類'],
                                              "size": "sm",
                                              "wrap": True,
                                              "align": "start"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "separator",
                                      "margin": "xxl"
                                  },
                                  {
                                      "type": "box",
                                      "layout": "horizontal",
                                      "margin": "md",
                                      "contents": [
                                          {
                                              "type": "text",
                                              "text": "糧商登記證證號:",
                                              "size": "xs",
                                              "color": "#aaaaaa",
                                              "flex": 0
                                          },
                                          {
                                              "type": "text",
                                              "text": b['糧商登記證證號'],
                                              "color": "#aaaaaa",
                                              "size": "xs",
                                              "align": "end"
                                          }
                                      ]
                                  }
                              ]
                          },
                          "styles": {
                              "footer": {
                                  "separator": True
                              }
                          }
                          }
                bubbles.append(bubble)
                i += 1
                ed_time = time.time()

    if len(bubbles) != 0:
        contents['contents'] = bubbles
        message = FlexSendMessage(alt_text='糧商資訊', contents=contents)
    elif len(bubbles) == 0:
        message = TextSendMessage(text='附近未搜尋到糧商相關資訊')
    return message
