from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from linebotapp.models import *
from linebotapp.Flex_Msg import *
from linebotapp.image_processing import *
from linebotapp.superpix import *

import os
import string
import time
import random
import csv

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        # empty list for return message
        message = []
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        # put request.body in return message for debug
        # print requestbody
        # message.append(TextSendMessage(text=str(body)))
        # quick_reply
        # message = TextSendMessage(
        #     text="文字訊息",
        #     quick_reply=QuickReply(
        #         items=[
        #             QuickReplyButton(
        #                 action=PostbackAction(label="Postback", data="回傳資料")
        #             ),
        #             QuickReplyButton(
        #                 action=MessageAction(label="文字訊息", text="回傳文字")
        #             ),
        #             QuickReplyButton(
        #                 action=DatetimePickerAction(label="時間選擇", data="時間選擇", mode='datetime')
        #             ),
        #             QuickReplyButton(
        #                 action=CameraAction(label="拍照")
        #             ),
        #             QuickReplyButton(
        #                 action=CameraRollAction(label="相簿")
        #             ),
        #             QuickReplyButton(
        #                 action=LocationAction(label="傳送位置")
        #             )
        #         ]
        #     )
        # )
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                print(event.message.type)
                if event.message.type == 'text':
                    # message.append(TextSendMessage(text='文字訊息'))
                    uid = event.source.user_id
                    profile = line_bot_api.get_profile(uid)
                    name = profile.display_name
                    mtext = event.message.text
                    if 'jobs' in mtext:
                        # mtext = event.message.text
                        if 'jobs' in mtext:
                            job = mtext.split(',')
                            Jobs.objects.create(uid=uid,
                                                name=name,
                                                job_name=job[1],
                                                percentage=job[2],
                                                description=job[3])
                            message.append(TextSendMessage(text='收到的工作內容為：' + str(job)))
                            message.append(TextSendMessage(text='建立工作內容完成'))
                            line_bot_api.reply_message(event.reply_token, message)
                    elif "工作查詢" in mtext:
                        message.append(jobs_progress(uid))
                        line_bot_api.reply_message(event.reply_token, message)
                    elif 'FlexMessage測試' in mtext:
                        message.append(flex_message_example())
                        line_bot_api.reply_message(event.reply_token, message)
                    else:
                        message.append(TextSendMessage(text='文字訊息'))
                        line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'image':
                    # message.append(TextSendMessage(text='圖片訊息'))
                    # line_bot_api.reply_message(event.reply_token, message)
                    image_name = ''.join(
                        random.choice(string.ascii_letters + string.digits) for x in range(4))  # build random img name
                    image_content = line_bot_api.get_message_content(event.message.id)
                    image_name = image_name.upper() + '.jpg'  # build image name ext = jpg
                    path = './static/' + image_name
                    with open(path, 'wb') as fd:  # write image into path
                        for chunk in image_content.iter_content():
                            fd.write((chunk))
                    # save image as gray and binary
                    domain = 'cb39-2001-b011-3819-d55a-98da-338d-1db2-20ef.jp.ngrok.io'
                    gray, binary, contour = image_processing_1(image_name, path)
                    gray = 'https://' + domain + gray[1:]
                    binary = 'https://' + domain + binary[1:]
                    contour = 'https://' + domain + contour[1:]
                    # message.append(ImageSendMessage(original_content_url=gray, preview_image_url=gray))
                    # message.append(ImageSendMessage(original_content_url=binary, preview_image_url=binary))
                    # message.append(ImageSendMessage(original_content_url=contour, preview_image_url=contour))

                    # superpix
                    slic = SLIC(image_name, path)
                    seeds = SEEDS(image_name, path)
                    lsc = LSC(image_name, path)
                    # slic = 'https://' + domain + slic[1:]
                    # seed = 'https://' + domain + seed[1:]
                    # lsc = 'https://' + domain + lsc[1:]
                    message.append(ImageSendMessage(original_content_url=slic, preview_image_url=slic))
                    message.append(ImageSendMessage(original_content_url=seeds, preview_image_url=seeds))
                    message.append(ImageSendMessage(original_content_url=lsc, preview_image_url=lsc))

                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'location':
                    message.append(TextSendMessage(text='位置訊息'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'video':
                    message.append(TextSendMessage(text='影片訊息'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'sticker':
                    message.append(TextSendMessage(text='貼圖訊息'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'audio':
                    message.append(TextSendMessage(text='聲音訊息'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'file':
                    message.append(TextSendMessage(text='檔案訊息'))
                    line_bot_api.reply_message(event.reply_token, message)

            elif isinstance(event, FollowEvent):
                print('加入好友')
                line_bot_api.reply_message(event.reply_token, message)

            elif isinstance(event, UnfollowEvent):
                print('取消好友')

            elif isinstance(event, JoinEvent):
                print('進入群組')
                line_bot_api.reply_message(event.reply_token, message)

            elif isinstance(event, LeaveEvent):
                print('離開群組')
                line_bot_api.reply_message(event.reply_token, message)

            elif isinstance(event, MemberJoinedEvent):
                print('有人入群')
                line_bot_api.reply_message(event.reply_token, message)

            elif isinstance(event, MemberLeftEvent):
                print('有人退群')
                line_bot_api.reply_message(event.reply_token, message)

            elif isinstance(event, PostbackEvent):
                print('PostbackEvent')
            # if isinstance(event, MessageEvent):
            #     mtext = event.message.text
            #     uid = event.source.user_id
            #     profile = line_bot_api.get_profile(uid)
            #     name = profile.display_name
            #     pic_url = profile.picture_url
            #
            #     if User_Info.objects.filter(uid=uid).exists() == False:
            #         User_Info.objects.create(uid=uid, name=name, pic_url=pic_url, mtext=mtext)
            #         message.append(TextSendMessage(text='會員資料新增完畢'))
            #     elif User_Info.objects.filter(uid=uid).exists() == True:
            #         message.append(TextSendMessage(text='已經有建立會員資料囉'))
            #         user_info = User_Info.objects.filter(uid=uid)
            #         for user in user_info:
            #             info = 'UID=%s\nNAME=%s\n大頭貼=%s' % (user.uid, user.name, user.pic_url)
            #             message.append(TextSendMessage(text=info))
            #     line_bot_api.reply_message(event.reply_token, message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
