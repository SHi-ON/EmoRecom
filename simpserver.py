#!/usr/bin/python3
# -*- coding: utf8 -*-

from flask import *
from camera import VideoCamera
from random import randint
import datetime

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


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
@app.route('/start')
def stanford_page():
    return render_template('start.html', user=user)

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera') 
def camera():
    return render_template('camera.html', title='Home', user=user, posts=posts, emotion=emotion)


@app.route('/index') 
def index():
    return render_template('index.html', title='Home', user=user, posts=posts, emotion=emotion)

last_i = -1
@app.route('/message', methods = ['GET'])
def message():
    global last_i
    message = 'Hi ' + user['username'] + '!'
    i = randint(0, 4)
    while (i == last_i):
        i = randint(0, 4)
    last_i = i
    if i == 1:
        message = 'You look ' + emotion['emo']
    if i == 2:
        currentDT = datetime.datetime.now()
        message = 'It is now ' + currentDT.strftime("%I:%M:%S %p")
    if i == 3:
        message = 'Chao you are so handsome!'
    return message



if __name__ == '__main__':
  app.run(debug=True)