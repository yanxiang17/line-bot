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

app = Flask(__name__)

line_bot_api = LineBotApi('64GNKQCRGKh800L3Dc/Hj+gV8V3mnevdP8Drj9T6Q9AoWZyKt6edlbIfm370Wch75D7ifND/IILOuQpPkma6fxLQWn2Ga96+Kabup50o8syWZ4D5hMnPaG/EEfSi8eL2yA3GTEH52+HuniBHfjjtygdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('498258515471c7275dfe5ede4a7fc94e')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
