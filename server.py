#!/usr/bin/python3
# -*- coding: utf8 -*-


from keras.preprocessing.image import img_to_array
from googleplaces import GooglePlaces, types, lang
from keras.models import load_model
from random import randint
from threading import Lock
from flask import *
import numpy as np
import subprocess
import googlemaps
import threading
import requests
import datetime
import imutils
import cv2
import json



detection_model_path = 'models/haarcascade_frontalface_default.xml'
emotion_model_path = 'models/_mini_XCEPTION.106-0.65.hdf5'
APIKEY = "AIzaSyAYkThdY9kCPUIEyOMsus2TINTn6mT2ROg"
google_places = GooglePlaces(APIKEY)
lock = Lock()
lock1 = Lock()



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
        'author': {'username': 'Shawn'},
        'body': 'The Avengers movie was so cool!'
    }
]

scoreboardframe = ""
scorerun = True
Lat_LNG = ""
places = []
large = ""
finalLarge = ""


def gen():
    global scoreboardframe
    global scorerun
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

        lock1.acquire()
        scoreboardframe = cv2.imencode('.jpg', scoreboard)[1].tobytes()
        scorerun = False
        lock1.release()

        # tt = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + tt + b'\r\n\r\n')

    

def gen1():
    while scorerun:
        pass
    while True:
        lock1.acquire()
        tt = scoreboardframe
        lock1.release()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + tt + b'\r\n\r\n')


@app.route('/')
@app.route('/start')
def stanford_page():
    return render_template('start.html', user=user)


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed1')
def video_feed1():
    return Response(gen1(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/map')
def map():
    return render_template('map.html', title='Home', user=user, posts=posts, emotion=finalLarge )

@app.route('/camera') 
def camera():
    return render_template('camera.html', title='Home', user=user, posts=posts, emotion=emotion)

@app.route('/backend') 
def backend():
    return render_template('backend.html', title='Home', user=user, posts=posts, emotion=emotion)


@app.route('/index') 
def index():
    return render_template('index.html', title='Home', user=user, posts=posts, emotion=emotion)

@app.route('/Location1') 
def Location1():
    return render_template('Location1.html', title='Home')

@app.route('/Location2') 
def Location2():
    return render_template('Location2.html', title='Home')


@app.route('/message', methods = ['GET'])
def message():
    lock.acquire()
    em = emotion['emo']
    lock.release()
    return em

@app.route('/locationNAME/<field1>', methods = ['GET'])
def locationNAME(field1):
    index = int(field1)
    if len(places) > 0:
        return places[index].name
    print ("ERROR URL")
    return ""


@app.route('/locationURL/<field1>', methods = ['GET'])
def locationURL(field1):
    index = int(field1)
    if len(places) > 0 and len(places[index].photos) > 0:
        photo = places[index].photos[0]
        photo.get(maxheight=500, maxwidth=500)
        return photo.url
    print "ERROR URL"
    return ""

@app.route('/my-link/')
def my_link():
  print('I got clicked!')
  return 'Click.'

@app.route('/getMAP', methods = ['GET'])
def getMAP():
    l = []
    for place in places:
        l.append(makeMapArg(place.name,place.formatted_address,place.lat_lng['lat'],place.lat_lng['lng']))
    print json.dumps(l)
    return json.dumps(l)

def findPlace(Lat_LNG, RADIUS=50):
    # Lat_LNG=MakeLatLNG((43.1351,-70.9293))
    query_result = google_places.nearby_search(
         lat_lng = Lat_LNG,radius=RADIUS)

    try:
        for place in query_result.places:
            place.get_details()
            places.append(place)
    except expression as identifier:
        print identifier
    
        # print place.name
        # print place.place_id
        # print place.types[0]
        # print place.rating
        # print place.geo_location
        # if len(place.photos) > 0:
        #     photo = place.photos[0]
        #     photo.get(maxheight=500, maxwidth=500)
        #     print photo.url
def makeMapArg(mapARG):
    return { "locationName" : mapARG[0],
      "address" : mapARG[1],
      "lat" : mapARG[2],
      "long" : mapARG[3]
    }




def MakeLatLNG(LOCATION):
    return {"lat" : LOCATION[0],"lng" : LOCATION[1]}


def findLocation():
    global Lat_LNG
    temp = subprocess.Popen(["./whereami", ""], stdout=subprocess.PIPE).communicate()[0].split()
    Lat_LNG = MakeLatLNG((temp[1],temp[3]))
    findPlace(Lat_LNG)


if __name__ == '__main__':
    thread1 = threading.Thread(target=findLocation)
    thread1.start()
    app.run(debug=True)
    thread1.join()
    camera1.release()
    cv2.destroyAllWindows()