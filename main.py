from bs4 import BeautifulSoup
import requests

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

"""
url = 'https://news.yahoo.co.jp/articles/d56ceef87e48131e6c409aee300b942fd943860a'
res = requests.get(url)

if res.status_code==200:

  soup = BeautifulSoup(res.text, 'html.parser')
  title_text = soup.find('h1', class_='sc-exkUMo').get_text()
  time_text = soup.find('time').get_text()
  body_text = soup.find('div', class_='article_body')
  body_text = str(body_text)
  body_text = body_text.replace("\"","\\\"")
  body_text = body_text.replace("\n", "<br>")
  body_text = body_text.replace("<br><br>", "<br>")

  content =  '{'
  content += ' \"status\": \"OK\", '
  content += ' \"totalResults\": \"1\", '
  content += ' \"articles\": [ '
  content += ' { '
  content += ' \"source\": { '
  content += ' \"id\": null, '
  content += ' \"name\": "Yahoo.co.jp" '
  content += ' }, '
  content += ' \"author\": null,'
  content += ' \"title\": \"' + title_text + '\", '
  content += ' \"description\": \"' + body_text + '\",'
  content += ' \"url\": \"' + url + '\",'
  content += ' \"urlToImage\": null,'
  content += ' \"publishedAt\": null,'
  content += ' \"content\": null}]'
  content += '}'

  
  
elif res.status_code==404:
  print('NOT OK:' + url)
"""

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="aaaa"))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)




