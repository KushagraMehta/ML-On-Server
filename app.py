from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, send, emit
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import os

count = 0
User_count = 0

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecrete'
socketio = SocketIO(app)


@app.route('/')
def index():
    print("Working")
    return render_template('streamer.html')


@socketio.on('Tunnel')
def connectedUser(message):
    global User_count
    User_count += 1
    print("Current user are "+str(User_count)+",New user is = " + str(message))


@socketio.on('disconnect')
def disconnect(message):
    global User_count
    User_count -= 1
    print("Current user are "+str(User_count) +
          ", Client Get Disconnected with ID="+str(message))


@socketio.on('IMAGE_DATA_FROM_STREAMER')
def image(data):
    global count
    count += 1
    if count < 10:
        return
    image = Image.open(BytesIO(base64.b64decode(data)))
    source = np.array(image)
    face_cascade = cv2.CascadeClassifier(
        os.getcwd() + '\\FaceData\\haarcascade_frontalface_default.xml')
    face_rects = face_cascade.detectMultiScale(source, scaleFactor=1.2)
    for (x, y, w, h) in face_rects:
        cv2.rectangle(source, (x, y), (x + w, y + h), (255, 255, 255), 10)

    pil_img = Image.fromarray(source)
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    new_image_string = "data:image/jpeg;base64," + \
        base64.b64encode(buff.getvalue()).decode("utf-8")
    socketio.emit('face', {"data": new_image_string})


if __name__ == '__main__':
    socketio.run(app)
