from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import requests
import time

cache = {}

CACHE_TTL = 3000

LINE_CHANNEL_ACCESS_TOKEN = "+4d4b4tYuCyHaSPqTi+RGVd1K4UE0jFrJSjRQsXekforo+qlJb0RfcVwy30PGnmyCMEVClafE9kypMNuZl2UIQALoKTVXe0/DQLMmH0wqZ3hVYoptW20Se12ATc172MMtVolDOyPGI4iydPBukjmhAdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "e7d1ccf75b6e25136e6611e800455f80"

user_key = "CWA-F87A3100-C712-40AA-B711-BFDB8BAE52B5" 
doc_name = "F-C0032-001"

url = 'https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/%s?downloadType=WEB&format=JSON&Authorization=%s' % (doc_name,user_key)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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
    print("incoming requests: ",event.message.text)
    county = event.message.text
    output = ""

    # Use cached data if not expired
    now = time.time()
    if county in cache and now - cache[county][0] < CACHE_TTL:
        datas = cache[county][1]
    else:
        print("getting new data from website")
        datas = requests.get(url).json()
        cache[county] = (now, datas)
        print("data collected")

    found = False

    for data in datas['cwaopendata']['dataset']['location']:
        if data['locationName'] == county.replace('台', '臺'):
            found = True
            for i in range(len(data['weatherElement'])):
                output += column[i] + ":" + data['weatherElement'][i]['time'][0]['parameter']['parameterName'] + "\n"
            break

    if not found:
        output = "請輸入正確的地名 (需加上縣市別)"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=output))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
