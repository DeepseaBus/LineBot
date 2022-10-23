from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from linebotapp.models import *

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
        message.append(TextSendMessage(text=str(body)))

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
                    message.append(TextSendMessage(text='文字訊息'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'image':
                    message.append(TextSendMessage(text='圖片訊息'))
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
