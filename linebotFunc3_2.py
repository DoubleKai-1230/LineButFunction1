from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationSendMessage, TemplateSendMessage, MessageTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn
import os

line_bot_api = LineBotApi(os.environ.get('Channel_Access_Token'))
handler = WebhookHandler(os.environ.get('Channel_Secret'))

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
    if mtext == '@轉盤樣板':
        sendCarousel(event)

    elif mtext == '@圖片轉盤':
        sendImgCarousel(event)
    
    elif mtext == '@星巴克位置':
        sendLocation(event)

    elif mtext == '@菜單':
        sendMenu(event)

    elif mtext == '@我想吃東西':
        sendDrink(event)

    elif mtext == '@我想喝飲料':
        sendEat(event)

def sendCarousel(event):  #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                        title='這是樣板一',
                        text='第一個轉盤樣板',
                        actions=[
                            MessageTemplateAction(
                                label='文字訊息一',
                                text='我們有賣披薩'
                            ),
                            URITemplateAction(
                                label='連結文淵閣網頁',
                                uri='http://www.e-happy.com.tw'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/qaAdBkR.png',
                        title='這是樣板二',
                        text='第二個轉盤樣板',
                        actions=[
                            MessageTemplateAction(
                                label='文字訊息二',
                                text='我們有賣飲料'
                            ),
                            URITemplateAction(
                                label='連結台大網頁',
                                uri='http://www.ntu.edu.tw'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendImgCarousel(event):  #圖片轉盤
    try:
        message = TemplateSendMessage(
            alt_text='圖片轉盤樣板',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/4QfKuz1.png',
                        action=MessageTemplateAction(
                            label='文字訊息',
                            text='我們有賣披薩'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/qaAdBkR.png',
                        action=URITemplateAction(
                            label='連結星巴克',
                            uri='https://www.starbucks.com.tw/home/index.jspx'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/Qg0rsSk.jpg',
                        action=MessageTemplateAction(
                            label='座標位置',
                            text='@星巴克位置'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendEat(event):  #圖片轉盤
    try:
        message = TemplateSendMessage(
            alt_text='圖片轉盤樣板',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/4QfKuz1.png',
                        action=MessageTemplateAction(
                            label='吃披薩',
                            text='我要吃披薩'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/LUP77pz.jpg',
                        action=MessageTemplateAction(
                            label='吃漢堡',
                            text='我要吃漢堡'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/1ZfVXdX.jpg',
                        action=MessageTemplateAction(
                            label='吃薯條',
                            text='我要吃薯條'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendDrink(event):  #圖片轉盤
    try:
        message = TemplateSendMessage(
            alt_text='圖片轉盤樣板',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/iDDalFF.jpg',
                        action=MessageTemplateAction(
                            label='咖啡',
                            text='我要喝咖啡'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/SJC26Rn.jpg',
                        action=MessageTemplateAction(
                            label='紅茶',
                            text='我要喝紅茶'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/LYRmeLG.jpg',
                        action=MessageTemplateAction(
                            label='可樂',
                            text='我要喝可樂'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendMenu(event):  #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                        title='我們有好多吃的',
                        text='披薩、漢堡、薯條',
                        actions=[
                            MessageTemplateAction(
                                label='想要吃',
                                text='@我想吃東西'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/qaAdBkR.png',
                        title='我們還有飲料',
                        text='紅茶、咖啡、可樂',
                        actions=[
                            MessageTemplateAction(
                                label='想要喝',
                                text='@我想喝飲料'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendLocation(event):
    try:
        message = LocationSendMessage(
            title='星巴克 景美門市', 
            address='116台北市文山區景興路185號1-2F', 
            latitude=24.99301856466003,
            longitude=121.54439425767183
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

if __name__ == '__main__':
    app.run()
