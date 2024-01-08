from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi('XG2BHeGYWeIAd5H9zX6jM8tdH3dSm3m+vb5kl74qWl5uQpqST8N4m2DiScsIaYi61vjUM3fbjbLmrjkdq7CBJ1oPHh8x8Tlv3HQtP7fx5IuKuYzlr/Y6XIc1XXJeFPSGsjUlRjzky4J/YkmIMPFwQwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8c8eec4610aa229d3112cc45bb1c1b6f')

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
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

if __name__ == '__main__':
    app.run(port=8000,host='0.0.0.0')
