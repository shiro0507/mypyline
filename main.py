import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from bs4 import BeautifulSoup
import requests,json

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


#url = 'https://news.yahoo.co.jp/articles/d56ceef87e48131e6c409aee300b942fd943860a'



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

    url=event.message.text
    res = requests.get(url)
    ken = ['北海道','青森','秋田','岩手','宮城','山形','福島','新潟','群馬','埼玉','茨城','栃木','東京','千葉','神奈川','横浜','山梨','長野','富山','石川','福井','静岡','愛知','岐阜','三重','京都','滋賀','和歌山','奈良','大阪','兵庫','岡山','鳥取','島根','広島','山口','香川','高知','愛媛','徳島','福岡','大分','熊本','長崎','宮崎','鹿児島','佐賀','沖縄']
    ken_tag = []

    if res.status_code==200:

      soup = BeautifulSoup(res.text, 'html.parser')
      title_text = soup.find('h1', class_='sc-hzDEsm').get_text()
      time_text = soup.find('time').get_text()
      body_text = soup.find('div', class_='article_body')
      body_text = str(body_text)
      #body_text = body_text.replace("\"","\\\"")
      body_text = body_text.replace("\n", "<br>")
      body_text = body_text.replace("<br><br>", "<br>")
      body_text += "<a href=\""+url+"\">アーカイブ元</a>"
      body_text += "<p>配信日 "+time_text+"</p>"

      for k in ken:      
        if body_text.find(k)!=-1:
          ken_tag.append(k)
        else:
          print('なし')

      for k_tag in ken_tag:
        print(k_tag)

      image = soup.find('img', class_='sc-fMiknA')
      image = image['src']


      json_data =  {'title': title_text, 'description':body_text,'url': url, 'time':time_text, 'image':image}

      to_url="https://velvet-osabori.ssl-lolipop.jp/sexcrime/fromheroku.php"
      headers = { 'Content-Type': 'application/json' }
      response = requests.post( to_url, data=json.dumps(json_data), headers=headers )

      status="status:" + str(response.status_code)
      print( "status:", response.status_code )
      print("aaaaa")

      
      
    elif res.status_code==404:
      print('NOT OK:' + url)



    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=status))



if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)




