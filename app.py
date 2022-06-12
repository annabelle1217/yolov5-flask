import io
import base64
from PIL import Image
import torch
from flask import Flask, jsonify, url_for, render_template, request, redirect
from pathlib import Path
import sys
import argparse

app = Flask(__name__)
DETECTION_URL = "/v1/object-detection/yolov5s"

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # current directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

model = torch.hub.load(
            "ultralytics/yolov5", "yolov5s", pretrained=True, force_reload=True
        )
model.eval()


def get_prediction(img_bytes):
    img = Image.open(io.BytesIO(img_bytes))
    imgs = [img]  # batched list of images

    # Inference
    results = model(imgs, size=640)  # reduce size to get faster inference
    return results

def save_result(results):
    results.render()
    # results.save()  # save as runs\detect\exp<no>\image0.jpg
    for im in results.imgs:
        im_base64 = Image.fromarray(im)
        im_base64.save("static/result.jpg", format="JPEG")


@app.route("/", methods=["GET", "POST"])
def predict_gui():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files.get("file")
        if not file:
            return redirect(request.url)

        img_bytes = file.read()
        results = get_prediction(img_bytes)
        save_result(results)
        return render_template("result.html")
    return render_template("index.html")


@app.route(DETECTION_URL, methods=["POST"])
def predict():
    if request.method != "POST":
        return

    if request.files.get("image"):
        im_file = request.files["image"]
        im_bytes = im_file.read()
        results = get_prediction(im_bytes)
        save_result(results)
        return results.pandas().xyxy[0].to_json(orient="records")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
    parser.add_argument(
        "--model",
        default="yolov5",
        type=str,
        help="Model option 'yolov5' or a custom model path.",
    )
    parser.add_argument("--port", default=5000, type=int, help="port number")
    opt = parser.parse_args()

    if opt.model == "yolov5":
        model = torch.hub.load(
            "ultralytics/yolov5", "yolov5s", pretrained=True, force_reload=True
        )
    else:
        model = torch.hub.load("ultralytics/yolov5", "custom", path=opt.model)
    model.eval()

    app.run(host="localhost", port=opt.port)  # debug=True causes Restarting with stat
