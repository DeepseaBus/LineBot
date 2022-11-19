import requests
import json

LINE_CHANNEL_ACCESS_TOKEN = 'KkQ7I9miG3pzCxo5oHmQCdsYhvGz3yaEuIdPAvFD6HjZ1W2u9KDnR12KfTdGV3Xtunl5TbJWl7BXAYzYsDBDjIC1/U0BtY/T1GqY39eMdsvQ2oquJ1mYYcwlm3XCY6HWzrpgA1PPbhlK5K/7Q5YCbQdB04t89/1O/w1cDnyilFU='

token = LINE_CHANNEL_ACCESS_TOKEN

Authorization_token = "Bearer " + LINE_CHANNEL_ACCESS_TOKEN

headers = {"Authorization": Authorization_token, "Content-Type": "application/json"}

body = {
    "size": {
        "width": 2500,
        "height": 1686
    },
    "selected": True,
    "name": "圖文選單 1",
    "chatBarText": "查看更多資訊",
    "areas": [
        {
            "bounds": {
                "x": 8,
                "y": 0,
                "width": 823,
                "height": 847
            },
            "action": {
                "type": "message",
                "text": "功能目錄"
            }
        },
        {
            "bounds": {
                "x": 840,
                "y": 1,
                "width": 823,
                "height": 847
            },
            "action": {
                "type": "message",
                "text": "工作查詢"
            }
        },
        {
            "bounds": {
                "x": 1667,
                "y": 0,
                "width": 823,
                "height": 847
            },
            "action": {
                "type": "message",
                "text": "動作 3"
            }
        },
        {
            "bounds": {
                "x": 4,
                "y": 839,
                "width": 823,
                "height": 847
            },
            "action": {
                "type": "message",
                "text": "動作 4"
            }
        },
        {
            "bounds": {
                "x": 845,
                "y": 839,
                "width": 823,
                "height": 847
            },
            "action": {
                "type": "message",
                "text": "動作 5"
            }
        },
        {
            "bounds": {
                "x": 1677,
                "y": 839,
                "width": 823,
                "height": 847
            },
            "action": {
                "type": "message",
                "text": "動作 6"
            }
        }
    ]
}

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                       headers=headers, data=json.dumps(body).encode('utf-8'))

print(req.text)

#############

from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi(token)
rich_menu_id = "richmenu-0a3ebb1130868d4a77865e455174010d"  # 設定成我們的 Rich Menu ID

path = r"C:\Users\User\PycharmProjects\LineBot\iconbox\buttons_richmenu-0a3ebb1130868d4a77865e455174010d.jpg"  # 主選單的照片路徑

with open(path, 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)

###################

rich_menu_id = "richmenu-0a3ebb1130868d4a77865e455174010d"  # 設定成我們的 Rich Menu ID
req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/'+rich_menu_id,
                       headers=headers)
print(req.text)

rich_menu_list = line_bot_api.get_rich_menu_list()