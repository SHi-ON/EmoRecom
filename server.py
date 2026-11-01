#!/usr/bin/python3
# -*- coding: utf8 -*-


from tensorflow.keras.utils import img_to_array
from googleplaces import GooglePlaces, types, lang
from tensorflow.keras.models import load_model
from random import randint
from threading import Lock
import time
from flask import *
import os
import numpy as np
import subprocess
import googlemaps
import threading
import requests
import datetime
import imutils
import cv2
# import hack2019


import recom

# parameters for loading data and images
detection_model_path = 'models/face_hyperparams.xml'
emotion_model_path = 'models/Xception_mini106.hdf5'

def get_google_places():
    key = os.environ.get("GOOGLE_PLACES_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GOOGLE_PLACES_API_KEY is required for recommendations")
    return GooglePlaces(key)
lock = Lock()
lock1 = Lock()


# hyper-parameters for bounding boxes shape
# loading models
face_detection = None
emotion_classifier = None
camera1 = None
camera_lock = Lock()

def initialize_camera():
    global face_detection, emotion_classifier, camera1
    with camera_lock:
        if camera1 is not None:
            return
        if not os.path.isfile(detection_model_path) or not os.path.isfile(emotion_model_path):
            raise RuntimeError("Real face detection and emotion model files are required")
        detector = cv2.CascadeClassifier(detection_model_path)
        if detector.empty():
            raise RuntimeError("Invalid face detection model")
        classifier = load_model(emotion_model_path, compile=False)
        camera = cv2.VideoCapture(int(os.environ.get("CAMERA_INDEX", "0")))
        if not camera.isOpened():
            camera.release()
            raise RuntimeError("Cannot open webcam")
        face_detection, emotion_classifier, camera1 = detector, classifier, camera
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised",
            "neutral"]
app = Flask(__name__)

@app.before_request
def local_only():
    # This legacy webcam application is local-only until proper user auth is added.
    if request.remote_addr not in ('127.0.0.1', '::1'):
        abort(403)


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
large = "happy"
finalLarge = ""
finalList = []


def gen():
    global scoreboardframe
    global scorerun
    global large
    initialize_camera()
    while True:
        ok, frame = camera1.read()
        if not ok:
            break
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
        time.sleep(0.05)
    while True:
        lock1.acquire()
        tt = scoreboardframe
        lock1.release()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + tt + b'\r\n\r\n')
        time.sleep(0.1)
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
    if not os.environ.get('GOOGLE_PLACES_API_KEY') or not os.environ.get('GOOGLE_MAPS_BROWSER_KEY'):
        abort(503, description='Google Maps/Places configuration is missing')
    return render_template('map.html', title='Home', user=user, posts=posts,
                           emotion=emotion, maps_browser_key=os.environ['GOOGLE_MAPS_BROWSER_KEY'])

@app.route('/recommendations', methods=['POST'])
def recommendations():
    if not request.is_json:
        abort(415)
    payload = request.get_json(silent=True) or {}
    try:
        lat = float(payload['lat'])
        lng = float(payload['lng'])
    except (KeyError, TypeError, ValueError):
        abort(400, description='Valid latitude/longitude required')
    if not (-90 <= lat <= 90 and -180 <= lng <= 180):
        abort(400, description='Latitude/longitude out of bounds')
    with lock:
        current_emotion = emotion['emo'].lower()
    results = makeSuggestList(current_emotion, MakeLatLNG((lat, lng)))
    return jsonify(results)

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
    if index < 0 or index >= len(places):
        abort(404)
    if len(places) > 0:
        return places[index].name
    print ("ERROR URL")
    return ""


@app.route('/locationURL/<field1>', methods = ['GET'])
def locationURL(field1):
    index = int(field1)
    if index < 0 or index >= len(places):
        abort(404)
    if len(places) > 0 and len(places[index].photos) > 0:
        photo = places[index].photos[0]
        photo.get(maxheight=500, maxwidth=500)
        return photo.url
    print ("ERROR URL")
    return ""

@app.route('/my-link/')
def my_link():
  print('I got clicked!')
  return 'Click.'

@app.route('/getMAP', methods = ['GET'])
def getMAP():
    return jsonify(finalList)

def findSuggestion():
    global finalList
    finalList = makeSuggestList(large)
    # print (json.dumps(finalList))

def makeSuggestList(em, location=None):
    aa = {}
    aa['sad']= "bar"
    aa['disgust']= "bar"
    aa['scared']= "gym"
    aa['neutral']= "restaurant"
    aa['happy']= "gym"
    aa['angry']= "cinema"
    aa['surprised']= "store"
    find = aa.get(em, 'gym')
    if(not find):
        find = 'gym'

    query_result = get_google_places().nearby_search(
         lat_lng = location if location is not None else Lat_LNG,radius=10000,keyword = str(find))
    l = []
    print (find,len(query_result.places),Lat_LNG)
    try:
        for place in query_result.places:
            place.get_details()
            l.append(makeMapArg((place.name,place.formatted_address,place.geo_location['lat'],place.geo_location['lng'])))
    except Exception as e: 
        print(e)

    return l
    

def findPlace(Lat_LNG, RADIUS=50):
    # Lat_LNG=MakeLatLNG((43.1351,-70.9293))
    query_result = get_google_places().nearby_search(
         lat_lng = Lat_LNG,radius=RADIUS)

    try:
        for place in query_result.places:
            place.get_details()
            places.append(place)
    except Exception as e: 
        print(e)
    
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
    raise RuntimeError('Automatic location probing is disabled. Use browser consent.')


if __name__ == '__main__':
    # Browser location is requested only after explicit user interaction.
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    if camera1 is not None:
        camera1.release()
    cv2.destroyAllWindows()
