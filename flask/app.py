from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import requests

user_key = "CWA-F87A3100-C712-40AA-B711-BFDB8BAE52B5" 
doc_name = "F-C0032-001"

url = 'https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/%s?downloadType=WEB&format=JSON&Authorization=%s' % (doc_name,user_key)

line_bot_api = LineBotApi('XG2BHeGYWeIAd5H9zX6jM8tdH3dSm3m+vb5kl74qWl5uQpqST8N4m2DiScsIaYi61vjUM3fbjbLmrjkdq7CBJ1oPHh8x8Tlv3HQtP7fx5IuKuYzlr/Y6XIc1XXJeFPSGsjUlRjzky4J/YkmIMPFwQwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8c8eec4610aa229d3112cc45bb1c1b6f')

column = ['天氣狀況','最高溫','最低溫','舒適度','降雨機率(%)']

@app.route("/helloworld",methods=['GET'])
def hendle_helloworld():
    return "Hola"

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
    county = event.message.text
    output = ""
    
    datas = requests.get(url).json()
    
    for data in datas['cwaopendata']['dataset']['location']:
        if data['locationName'] == county.replace('台', '臺'):
            for i in range(len(data['weatherElement'])):
                output = output + column[i] + ":" + data['weatherElement'][i]['time'][0]['parameter']['parameterName'] + "\n"
            break
    else:
        output = "請輸入正確的地名(需加上縣市別)"
    
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=output))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
