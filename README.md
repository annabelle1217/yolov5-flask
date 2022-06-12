# Flask REST API

[REST](https://en.wikipedia.org/wiki/Representational_state_transfer) [API](https://en.wikipedia.org/wiki/API)s are
commonly used to expose Machine Learning (ML)  models to other services. This folder contains an example REST API
created using Flask to expose the YOLOv5s model from [PyTorch Hub](https://pytorch.org/hub/ultralytics_yolov5/).

## Requirements
- [Pytorch](https://pytorch.org) >= 1.6. 
- [Pillow](https://pypi.org/project/Pillow/)
- [Flask](https://palletsprojects.com/p/flask/)

Install Pytorch with instruction in https://pytorch.org. Then, install the rest with: 
```shell
$ pip install Flask Pillow
```

## Run

After Flask installation run:

```shell
$ python app.py --model yolov5
```
To use custom model:
```shell
$ python app.py --model best.pt
```

## Use GUI
Use GUI to upload and view resut:
Go to [http://localhost:5000](http://localhost:5000)

## Use Terminal
Use [curl](https://curl.se/) to perform a request (Recommended: Git Bash):

```shell
$ curl -X POST -F image=@images/cat.jpg 'http://localhost:5000/v1/object-detection/yolov5s'
```

The model inference results are returned as a JSON response:

```json
[{"xmin":384.2033081055,"ymin":35.8358840942,"xmax":823.404296875,"ymax":409.2363891602,"confidence":0.8502380848,"class":0,"name":"cat"}]
```

## Reference
- [YOLOv5 Flask REST API](https://github.com/ultralytics/yolov5/tree/master/utils/flask_rest_api)
- [Yolov5 Flask @jzhang533](https://github.com/jzhang533/yolov5-flask)
- [Load YOLOv5 from PyTorch Hub ](https://github.com/ultralytics/yolov5/issues/36)
- [Pytorch Flask API Heroku @avinassh](https://github.com/avinassh/pytorch-flask-api-heroku)

Note: The best.pt provided is self-trained yolov5 model on cats and dogs dataset.