#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_pi import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

def gen(camera, genType="video"):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        if genType == "photo":
            break;


@app.route('/video-feed')
def videoFeed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video')
def videoStream():
    return render_template('video-stream.html')


@app.route('/photo-feed')
def photoFeed():
    return Response(gen(Camera(), genType="photo"),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/photo')
def photoCapture():
    return render_template('photo-capture.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
