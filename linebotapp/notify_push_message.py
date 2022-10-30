import requests


def LineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)


token = 'kQ9M3yeqSaWAUyV3XhABpPVwe3wuc1BKnaHdeUNPKvG'
msg = 'DataBot is online ヽ(✿ﾟ▽ﾟ)ノ'
LineNotifyMessage(token, msg)
