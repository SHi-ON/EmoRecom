#!/usr/bin/python3
# -*- coding: utf8 -*-

from flask import *
from keras.preprocessing.image import img_to_array
import imutils
import cv2
from threading import Lock
from keras.models import load_model
import numpy as np
from random import randint
import datetime

lock = Lock()


# parameters for loading data and images
detection_model_path = 'models/haarcascade_frontalface_default.xml'
emotion_model_path = 'models/_mini_XCEPTION.106-0.65.hdf5'

# hyper-parameters for bounding boxes shape
# loading models
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
emotion_classifier._make_predict_function()
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised",
            "neutral"]
camera1 = cv2.VideoCapture(0)

app = Flask(__name__)


user = {'username': 'Monkie'}
emotion = {'emo': 'Happy'}
posts = [
    {
        'author': {'username': 'Monkie'},
        'body': 'Beautiful day in Durham!'
    },
    {
        'author': {'username': 'Shayan'},
        'body': 'The Avengers movie was so cool!'
    }
]

scoreboardframe = ""
scorerun = True
large = ""

def gen():
    while True:
        frame = camera1.read()[1]
        # reading the frame
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                                flags=cv2.CASCADE_SCALE_IMAGE)
        # emotion classification result screen
        scoreboard = np.zeros((250, 300, 3), dtype="uint8")
        # camera frame
        camera_frame = frame.copy()
        if len(faces) > 0:
            faces = sorted(faces, reverse=True,
                            key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces
            # Extract the ROI of the face from the grayscale image, resize it to a fixed 48x48 pixels, and then prepare
            # the ROI for classification via the CNN
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (48, 48))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            preds = emotion_classifier.predict(roi)[0]
            emotion_probability = np.max(preds)
            label = EMOTIONS[preds.argmax()]
            score = 0
            for (i, (ee, prob)) in enumerate(zip(EMOTIONS, preds)):
                # construct the label text
                text = "{}: {:.2f}%".format(ee, prob * 100)
                # probability of classes of emotion
                
                w = int(prob * 300)
                if w > score:
                    score = w
                    large = ee
                    

                cv2.rectangle(scoreboard, (7, (i * 35) + 5),
                                (w, (i * 35) + 35), (0, 0, 255), -1)
                cv2.putText(scoreboard, text, (10, (i * 35) + 23),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                            (255, 255, 255), 2)
                cv2.rectangle(camera_frame, (fX, fY), (fX + fW, fY + fH),
                                (0, 0, 255), 2)
                cv2.putText(camera_frame, label, (fX, fY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            lock.acquire()
            emotion['emo'] = str(large)
            lock.release()

        # cv2.imshow('Face Cam', camera_frame)
        # cv2.imshow("Likelihoods", scoreboard)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        tt = cv2.imencode('.jpg', camera_frame)[1].tobytes()

        # tt = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + tt + b'\r\n\r\n')

    camera.release()
    cv2.destroyAllWindows()



@app.route('/')
@app.route('/start')
def stanford_page():
    return render_template('start.html', user=user)

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera') 
def camera():
    return render_template('camera.html', title='Home', user=user, posts=posts, emotion=emotion)


@app.route('/index') 
def index():
    return render_template('index.html', title='Home', user=user, posts=posts, emotion=emotion)


@app.route('/message', methods = ['GET'])
def message():
    lock.acquire()
    em = emotion['emo']
    lock.release()
    message = 'You look ' + em
    return message

# last_i = -1
# @app.route('/message', methods = ['GET'])
# def message():
#     global last_i
#     print ("DDDDDDD")
#     message = 'Hi ' + user['username'] + '!'
#     i = randint(0, 4)
#     while (i == last_i):
#         i = randint(0, 4)
#     last_i = i
#     if i == 1:
#         message = 'You look ' + emotion['emo']
#     if i == 2:
#         currentDT = datetime.datetime.now()
#         message = 'It is now ' + currentDT.strftime("%I:%M:%S %p")
#     if i == 3:
#         message = 'Chao you are so handsome!'
#     return message





@app.route('/my-link/')
def my_link():
  print('I got clicked!')
  return 'Click.'




if __name__ == '__main__':
  app.run(debug=True)