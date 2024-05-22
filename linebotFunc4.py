from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, PostbackEvent, TextSendMessage, ImagemapSendMessage, BaseSize, MessageImagemapAction, URIImagemapAction, ImagemapArea, TemplateSendMessage, ButtonsTemplate, DatetimePickerTemplateAction
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
    if mtext == '@圖片地圖':
        sendImgmap(event)

    elif mtext == '@日期時間':
        sendDatetime(event)

    elif mtext == '看漫畫':
        sendComics(event)

@handler.add(PostbackEvent)  #PostbackTemplateAction觸發此事件
def handle_postback(event):
    data=event.postback.data
    action,mode=data.split('^')  #取得data資料
    if action == 'DateTimePicker':
        sendData_sell(event, mode)

def sendComics(event):  #圖片地圖
    try:
        image_url = 'https://i.imgur.com/AbHP3Wc.png'  #圖片位址
        imgwidth = 1040  #原始圖片寛度一定要1040
        imgheight = 1040
        message = ImagemapSendMessage(
            base_url=image_url,
            alt_text="四格漫畫",
            base_size=BaseSize(height=imgheight, width=imgwidth),  #圖片寬及高
            actions=[
                MessageImagemapAction(  #顯示文字訊息
                    text='男孩驚慌地從床上醒來，看到時鐘指向早上8:45，驚呼：“哦不！我要遲到了！',
                    area=ImagemapArea(  #設定圖片範圍:左方1/4區域
                        x=0, 
                        y=0, 
                        width=520, 
                        height=520   
                    )
                ),
                MessageImagemapAction(  #顯示文字訊息
                    text='男孩匆忙地準備好出門，來到學校卻發現教室空無一人，心想：“今天不是有課嗎？',
                    area=ImagemapArea(  #設定圖片範圍:左方1/4區域
                        x=520, 
                        y=0, 
                        width=520, 
                        height=520   
                    )
                ),
                MessageImagemapAction(  #顯示文字訊息
                    text='男孩在教室裡坐下，看著手機發現一條信息提醒他“今天是假日！”他自言自語：“我真笨！',
                    area=ImagemapArea(  #設定圖片範圍:左方1/4區域
                        x=0, 
                        y=520, 
                        width=520, 
                        height=520 
                    )
                ),
                MessageImagemapAction(  #顯示文字訊息
                    text='男孩回家後並且回到房間裡，決定繼續睡覺，他說：“既然今天是假日，讓我們再睡一會兒吧！',
                    area=ImagemapArea(  #設定圖片範圍:左方1/4區域
                        x=520, 
                        y=520, 
                        width=520, 
                        height=520  
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendImgmap(event):  #圖片地圖
    try:
        image_url = 'https://i.imgur.com/Yz2yzve.jpg'  #圖片位址
        imgwidth = 1040  #原始圖片寛度一定要1040
        imgheight = 300
        message = ImagemapSendMessage(
            base_url=image_url,
            alt_text="圖片地圖範例",
            base_size=BaseSize(height=imgheight, width=imgwidth),  #圖片寬及高
            actions=[
                MessageImagemapAction(  #顯示文字訊息
                    text='你點選了紅色區塊！',
                    area=ImagemapArea(  #設定圖片範圍:左方1/4區域
                        x=0, 
                        y=0, 
                        width=imgwidth*0.25, 
                        height=imgheight  
                    )
                ),
                URIImagemapAction(  #開啟網頁
                    link_uri='http://www.e-happy.com.tw',
                    area=ImagemapArea(  #右方1/4區域(藍色1)
                        x=imgwidth*0.75, 
                        y=0, 
                        width=imgwidth*0.25, 
                        height=imgheight  
                    )
                ),
            ]
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendDatetime(event):  #日期時間
    try:
        message = TemplateSendMessage(
            alt_text='日期時間範例',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/VxVB46z.jpg',
                title='日期時間示範',
                text='請選擇：',
                actions=[
                    DatetimePickerTemplateAction(
                        label="選取日期",
                        data="DateTimePicker^date",  #觸發postback事件
                        mode="date",  #選取日期
                        initial="2020-10-01",  #顯示初始日期
                        min="2020-10-01",  #最小日期
                        max="2021-12-31"  #最大日期
                    ),
                    DatetimePickerTemplateAction(
                        label="選取時間",
                        data="DateTimePicker^time",
                        mode="time",  #選取時間
                        initial="10:00",
                        min="00:00",
                        max="23:59"
                    ),
                    DatetimePickerTemplateAction(
                        label="選取日期時間",
                        data="DateTimePicker^datetime",
                        mode="datetime",  #選取日期時間
                        initial="2020-10-01T10:00",
                        min="2020-10-01T00:00",
                        max="2021-12-31T23:59"
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendData_sell(event, mode):  #Postback,顯示日期時間
    try:
        if mode == 'date':
            dt = '日期為：' + event.postback.params.get('date')  #讀取日期
        elif mode == 'time':
            dt = '時間為：' + event.postback.params.get('time')  #讀取時間
        elif mode == 'datetime':
            date,time = event.postback.params.get('datetime').split('T')  #讀取日期時間
            dt = f'日期為：{date}\n時間為：{time}' #轉為字串
        message = TextSendMessage(
            text=dt
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

if __name__ == '__main__':
    app.run()
