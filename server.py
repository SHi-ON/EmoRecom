#!/usr/bin/python3
# -*- coding: utf8 -*-

from flask import Flask, render_template, Response
from camera import Camera

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
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
@app.route('/start')
def stanford_page():
    return render_template('start.html', user=user)

# @app.route('/')
# def video_feed():
#     return Response(gen(Camera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/index') 
# what is this?
def index():
    
    return render_template('index.html', title='Home', user=user, posts=posts, emotion=emotion)






@app.route('/my-link/')
def my_link():
  print('I got clicked!')

  return 'Click.'

if __name__ == '__main__':
  app.run(debug=True)