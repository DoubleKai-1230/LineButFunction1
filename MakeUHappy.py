from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import random

import os

line_bot_api = LineBotApi(os.environ.get('Channel_Access_Token','YzwOno6QuUc+LFOCGAwZZWrHs9t9M89QPXbycGrYBtBfDNCIgOphhp55Q4fGDiUhOS3yxtVALZMLhOktQRDu/kwC7Xv55ULmaT+fWwUD3BEk27+1WqDB47QjXhoauyV2rXN4uwjcUP5IoxplGUFvagdB04t89/1O/w1cDnyilFU='))
handler = WebhookHandler(os.environ.get('Channel_Secret','a97c5fd8154d67e02a4ebcd665550e30'))

happyList = ["鞥比腦婆，我愛妳喔!","鞥比腦婆，你是最棒的!","鞥比腦婆，你是大美呂!","鞥比腦婆，可愛寶寶!","鞥比腦婆，呱!"]

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    if mtext == "我需要正能量":
        message = TextSendMessage(
            text = random.choice(happyList)
        )
        line_bot_api.reply_message(event.reply_token,message)
    


if __name__ == '__main__':
    app.run()
