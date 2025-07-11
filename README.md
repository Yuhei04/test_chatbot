# LINE Bot + YOLOv5 による人数カウントアプリケーション

このプロジェクトは，**YOLOv5を用いたリアルタイム人物検出**と，**LINE Botを通じた混雑状況の通知**を組み合わせたアプリケーションです．Webカメラで検出された人物数を常時監視し，ユーザーがLINEで「人数を教えて」と尋ねると現在の人数を返信します．

---

## 特徴

- YOLOv5（`ultralytics/yolov5`）によるリアルタイム人物検出
- LINE Bot連携によるチャットインターフェース
- 混雑度を段階的に通知（空いている／混雑／大変混雑）
- FlaskによるWebhookサーバー
- マルチスレッドでFlaskとカメラ処理を同時実行

---

## 使用技術

- Python 3.8+
- Flask
- OpenCV
- Torch / PyTorch
- YOLOv5 (`torch.hub`経由で`ultralytics/yolov5`)
- LINE Messaging API

---
