from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import base64
import numpy as np
import cv2
import os
count = 0


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecrete'
socketio = SocketIO(app)


@app.route('/')
def index():
    print("Working")
    return render_template('./streamer.html')


@socketio.on('Tunnel')
def connectedUser(message):
    print("User id is = " + str(message))


@socketio.on('IMAGE_DATA_FROM_STREAMER')
def image(data):
    global count
    count += 1
    img = base64.b64decode(data['image'].split(',')[1])
    npimg = np.frombuffer(img, dtype=np.uint8)
    source = cv2.imdecode(npimg, 1)
    # face_cascade = cv2.CascadeClassifier(
    #     os.getcwd() + '\\FaceData\\haarcascade_frontalface_default.xml')
    # face_img = source.copy()
    # face_rects = face_cascade.detectMultiScale(face_img, scaleFactor=1.2)
    print(str(data['time']))
    # if len(face_rects) != 0:
    #     print("WORKING@@@@@@@@@@@@@ "+ str(data['time']))
        # socketio.emit('face', {'data': face_rects}, broadcast=True)
    # for (x, y, w, h) in face_rects:
    #     cv2.rectangle(face_img, (x, y), (x + w, y + h), (255, 255, 255), 10)
    # cv2.imwrite(os.getcwd() + '\\image\\data' + str(count) + '.jpg', source)


# send( msg, broadcast= True)
if __name__ == '__main__':
    socketio.run(app)
