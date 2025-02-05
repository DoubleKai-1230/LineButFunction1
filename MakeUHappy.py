from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai
import os

line_bot_api = LineBotApi(os.environ.get('Channel_Access_Token'))
handler = WebhookHandler(os.environ.get('Channel_Secret'))

genai.configure(api_key=os.environ.get("API_KEY"))

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
    
    model = genai.GenerativeModel("gemini-1.5-flash",
                              system_instruction="你是一個充滿正能量的 AI 助手，請在每次回應時包含積極、鼓勵的語氣，並且幫助使用者以最正向的方式解決問題。長話短說，給予最有力量的文句。")
    chat = model.start_chat(history=[])
    response = chat.send_message(mtext)
    message = TextSendMessage(
        text = response.text
    )
    line_bot_api.reply_message(event.reply_token,message)
    


if __name__ == '__main__':
    app.run()
