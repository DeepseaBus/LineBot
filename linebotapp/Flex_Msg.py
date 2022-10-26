# 2022/10/26

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from linebotapp.models import *


def jobs_progress(uid):
    contents=dict()
    contents['type']='carousel'
    bubbles=[]
    datas = Jobs.objects.filter(uid=uid)
    i=0
    config_color = [#顏色列表
        '#00DB00',
        '#02DF82',
        '#921AFF',
        '#00E3E3',
        '#921AFF',
    ]
    for data in datas:
        color = config_color[i]#以i取顏色
        i+=1#每次迴圈+1
        label = data.job_name
        percentage = data.percentage
        text = data.description
        bubble= {   "type": "bubble",
                    "size": "nano",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": label,
                            "color": "#ffffff",
                            "align": "start",
                            "size": "md",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": str(percentage)+"%",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "xs",
                            "gravity": "center",
                            "margin": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "filler"
                                }
                                ],
                                "width": str(percentage)+"%",
                                "backgroundColor": "#0D8186",
                                "height": "6px"
                            }
                            ],
                            "backgroundColor": "#9FD8E36E",
                            "height": "6px",
                            "margin": "sm"
                        }
                        ],
                        "backgroundColor": color,
                        "paddingTop": "19px",
                        "paddingAll": "12px",
                        "paddingBottom": "16px"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "text": text,
                                "color": "#8C8C8C",
                                "size": "sm",
                                "wrap": True
                            }
                            ],
                            "flex": 1
                        }
                        ],
                        "spacing": "md",
                        "paddingAll": "12px"
                    },
                    "styles": {
                        "footer": {
                        "separator": False
                        }
                    }
                }
        bubbles.append(bubble)
    contents['contents']=bubbles
    message=FlexSendMessage(alt_text='工作進度',contents=contents)
    return message

def flex_message_example():
    content = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://i.imgur.com/jQqLaas.jpg",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "http://linecorp.com/"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "What's New",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Data",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": "OilPrice",
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "CALL",
                        "uri": "https://linecorp.com"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "WEBSITE",
                        "uri": "https://linecorp.com"
                    }
                }
            ],
            "flex": 0
        }
    }

    message = FlexSendMessage(alt_text='FlexMessage範例', contents=content)
    return message
