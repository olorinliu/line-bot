from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('3uYnPgcC2TsP3fBXx7qMbx0ljkUVN5ex7Z2XTcM7MV6KnTmhw4GYB3rWiTayt8KobPOXWmLEUfJIk/INR3QkrQgBwhROXm3/CkWndQ33v6mxFQxqXVhBic6Xw0owqj/oREFzG9HmGzOZtL6zqEYxTgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('05b447cb6b1f6868ba95340efcc568d3')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = "我看不懂你在說什麼"
    
    if "給我貼圖" in msg:
        sticker_message = StickerSendMessage(
            package_id='51626502',
            sticker_id='51626502'
        )
        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)
        return

    if msg in ["hi", "Hi"]:
        r = "嗨"
    elif msg == "你在幹嘛":
        r = "在想你啊<3"
    elif msg == "你吃飯了嗎":
        r = "我不用吃飯"
    elif msg == "你是誰":
        r = "喜歡你的人"
    elif "訂位" in msg:
        r = "您想訂位，是嗎？"


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()