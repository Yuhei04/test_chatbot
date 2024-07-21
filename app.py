# from flask import Flask, request, abort
# import os
# from linebot import LineBotApi, WebhookHandler
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage

# app = Flask(__name__)

# line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
# handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# @app.route("/callback", methods=['POST'])
# def callback():
#     signature = request.headers['X-Line-Signature']
#     body = request.get_data(as_text=True)

#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)

#     return 'OK'

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text='Message received')
#     )

# if __name__ == "__main__":
#     # Get the port from the environment variable, default to 8080
#     port = int(os.getenv('PORT', 10000))
#     app.run(host='0.0.0.0', port=port, debug=True)


import os
import threading

import cv2
import torch
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 環境変数からLINEのチャネルシークレットとアクセストークンを読み込む
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'YOUR_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_CHANNEL_ACCESS_TOKEN')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# グローバル変数
num_persons = 0


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     global num_persons
#     if event.message.text == "人数を教えて":
#         reply = f"現在の人数は{num_persons}人です。"
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text=reply)
#         )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global num_persons
    if event.message.text == "人数を教えて":
        if num_persons <= 4:
            reply = f"現在の人数は{num_persons}人です。空いています。"
        elif num_persons <= 8:
            reply = f"現在の人数は{num_persons}人です。混雑しています。"
        else:
            reply = f"現在の人数は{num_persons}人です。大変混雑しています。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )


def yolo_camera():
    global num_persons

    # YOLOv5モデルのロード
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    # ウェブカメラのキャプチャ開始
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream or file")
        return

    while True:
        # フレームをキャプチャ
        ret, frame = cap.read()
        if not ret:
            break

        # フレームに対してYOLOv5モデルを実行
        results = model(frame)

        # 検出された人数をカウント
        detected_persons = results.pandas().xyxy[0]
        num_persons = len(detected_persons[detected_persons['name'] == 'person'])

        # 検出結果を描画
        results.render()

        # フレームを表示
        cv2.imshow('YOLOv5 Webcam', frame)

        # 'q'キーが押されたらループを終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # キャプチャを解放し、ウィンドウを閉じる
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Flaskアプリケーションを別スレッドで実行
    threading.Thread(target=lambda: app.run(port=5000, use_reloader=False)).start()

    # YOLOカメラ処理をメインスレッドで実行
    yolo_camera()