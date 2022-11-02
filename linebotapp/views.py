import re

import requests
from django.shortcuts import render

# ngrok domain

domain = 'b0a5-2001-b011-3819-ddb7-7cfb-8a7e-56c1-192a.jp.ngrok.io'

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
from linebotapp.Grain_Merchant import *
from linebotapp.Video_Processing import *

# audio to string
import speech_recognition as sr
from pydub import AudioSegment

# string to audio (MS. Google)
from gtts import gTTS

from liffpy import (
    LineFrontendFramework as LIFF,
    ErrorResponse
)

import os
import string
import time
import random
import csv

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
liff_api = LIFF(settings.LINE_CHANNEL_ACCESS_TOKEN)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        # empty list for return message
        message = []
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        # test request
        print(body)

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
                    if mtext[0] == ' ':  # id first char = ' '
                        tts = gTTS(text=mtext, lang='zh-tw')
                        tts.save("./static/mtext.m4a")
                        # url = 'https://' + domain + '/static/mtext.m4a'
                        url = domain + '/static/mtext.m4a'
                        print(url)
                        message.append(AudioSendMessage(original_content_url=url, duration=330 * len(mtext)))  # 330ms
                        line_bot_api.reply_message(event.reply_token, message)
                    elif 'jobs' in mtext:
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
                    elif 'https://' in mtext:
                        try:
                            # 新增LIFF頁面到LINEBOT中
                            liff_id = liff_api.add(
                                view_type="tall",
                                view_url=mtext)

                            message.append(TextSendMessage(text='https://liff.line.me/' + liff_id))
                            line_bot_api.reply_message(event.reply_token, message)
                        except:
                            print(err.message)

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
                    # message.append(TextSendMessage(text='位置訊息'))
                    address = event.message.address
                    latitude = event.message.latitude
                    longitude = event.message.longitude
                    message.append(TextSendMessage(text='位置訊息'))
                    message.append(grain_merchant(address, latitude, longitude))
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'video':
                    # message.append(TextSendMessage(text='影片訊息'))
                    video_content = line_bot_api.get_message_content(event.message.id)
                    path = './static/video.mp4'
                    with open(path, 'wb') as fd:
                        for chunk in video_content.iter_content():
                            fd.write(chunk)
                    message.append(TextSendMessage(text='影片存檔成功'))
                    image_path, video_path = video_processing(path)
                    message.append(TextSendMessage(text='影片處理完畢'))
                    message.append(VideoSendMessage(original_content_url=domain + video_path[1:],
                                                    preview_image_url=domain + image_path[1:]))
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'sticker':
                    message.append(TextSendMessage(text='貼圖訊息'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'audio':

                    message.append(TextSendMessage(text='聲音訊息'))

                    audio_content = line_bot_api.get_message_content(event.message.id)

                    path = './static/sound.m4a'

                    with open(path, 'wb') as fd:

                        for chunk in audio_content.iter_content():
                            fd.write(chunk)

                    # audio covert to string
                    r = sr.Recognizer()
                    # download https://github.com/BtbN/FFmpeg-Builds/releases => ffmpeg-N-108894-g01b9abd771-win64-gpl-shared.zip
                    AudioSegment.converter = 'C:\\ffmpeg\\bin\\ffmpeg.exe'  # enter ffmpeg.exe path
                    sound = AudioSegment.from_file_using_temporary_files(path)
                    path = os.path.splitext(path)[0] + '.wav'
                    sound.export(path, format="wav")
                    with sr.AudioFile(path) as source:
                        audio = r.record(source)
                    text = r.recognize_google(audio, language='zh-Hant')  # set language

                    # response converted string
                    message.append(TextSendMessage(text=text))
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


@csrf_exempt
def notify(request):
    pattern = 'code=.*&'

    raw_uri = request.get_raw_uri()

    codes = re.findall(pattern, raw_uri)
    for code in codes:
        code = code[5:-1]
        print(code)

    # get user notify token
    user_notify_token_get_url = 'https://notify-bot.line.me/oauth/token'
    params = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'https://cb39-2001-b011-3819-d55a-98da-338d-1db2-20ef.jp.ngrok.io/notify',
        'client_id': 'apc8aGaX4nB6tXbConnhTC',
        'client_secret': 'WJzgZgqXaiZNgOWrOL790ItSKWsnxrgCsaRjcWk7dQy'

    }
    get_token = requests.post(user_notify_token_get_url, params=params)
    print(get_token.json())
    token = get_token.json()['access_token']
    print(token)

    # get user info
    user_info_url = 'https://notify-api.line.me/api/status'
    headers = {'Authorization': 'Bearer ' + token}
    get_user_info = requests.get(user_info_url, headers=headers)
    print(get_user_info.json())
    notify_user_info = get_user_info.json()
    if notify_user_info['targetType'] == 'USER':
        User_Info.objects.filter(name=notify_user_info['target']).update(notify=token)
    elif notify_user_info['targetType'] == 'GROUP':
        pass
    return HttpResponse()


@csrf_exempt
def Weather_Predict(request):
    # use utf-8 decode request
    body = request.body.decode('utf-8')
    print(body)

    text = '雷達回波圖'

    token = 'kQ9M3yeqSaWAUyV3XhABpPVwe3wuc1BKnaHdeUNPKvG'

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    notify_url = "https://notify-api.line.me/api/notify"
    # payload message => text, imageThumbnail => Thumbnail path, imageFullsize = full img path
    payload = {'message': text, 'imageThumbnail': body, 'imageFullsize': body}
    r = requests.post(notify_url, headers=headers, params=payload)
    return HttpResponse()
