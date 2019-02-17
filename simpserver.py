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

@app.route('/map') 
def map():
    return render_template('map.html', title='Home', user=user, posts=posts, emotion=emotion)

@app.route('/fakejson')
def fakejson():
    return "[{‘locationName’: u’Bamee Restaurant’, ‘lat’: Decimal(‘43.1349243’), ‘long’: Decimal(‘-70.9261436’), ‘address’: u'12 Jenkins Court ste 1, Durham, NH 03824, USA’}, {‘locationName’: u’Little Lebanon To Go’, ‘lat’: Decimal(‘43.2006966’), ‘long’: Decimal(‘-70.875303’), ‘address’: u'547 Central Ave, Dover, NH 03820, USA’}, {‘locationName’: u’Ember Wood Fired Grill’, ‘lat’: Decimal(‘43.1954104’), ‘long’: Decimal(‘-70.8752133’), ‘address’: u'1 Orchard St, Dover, NH 03820, USA’}, {‘locationName’: u’La Festa Brick & Brew’, ‘lat’: Decimal(‘43.1941592’), ‘long’: Decimal(‘-70.87481509999999’), ‘address’: u'300 Central Ave, Dover, NH 03820, USA’}, {‘locationName’: u'2 Home Cooks’, ‘lat’: Decimal(‘43.19592979999999’), ‘long’: Decimal(‘-70.8765659’), ‘address’: u'40 Chestnut St, Dover, NH 03820, USA’}, {‘locationName’: u’Chapel + Main Restaurant|Brewery’, ‘lat’: Decimal(‘43.1979735’), ‘long’: Decimal(‘-70.87259330000001’), ‘address’: u'83 Main St, Dover, NH 03820, USA’}, {‘locationName’: u’Saigon & Tokyo Dover , nh’, ‘lat’: Decimal(‘43.2185432’), ‘long’: Decimal(‘-70.88413700000001’), ‘address’: u'892B Central Ave, Dover, NH 03820, USA’}, {‘locationName’: u’Dos Amigos Burritos - Dover’, ‘lat’: Decimal(‘43.193436’), ‘long’: Decimal(‘-70.87432799999999’), ‘address’: u'286 Central Ave, Dover, NH 03820, USA’}, {‘locationName’: u”Patty B’s Italian Restaurant”, ‘lat’: Decimal(‘43.1734103’), ‘long’: Decimal(‘-70.86100949999999’), ‘address’: u'34 Dover Point Rd, Dover, NH 03820, USA’}, {‘locationName’: u’The Gyro Spot’, ‘lat’: Decimal(‘43.1968492’), ‘long’: Decimal(‘-70.87400599999999’), ‘address’: u'421 Central Ave, Dover, NH 03820, USA’}, {‘locationName’: u”Franz’s Food”, ‘lat’: Decimal(‘43.1342638’), ‘long’: Decimal(‘-70.926053’), ‘address’: u'46 Main St, Durham, NH 03824, USA’}, {‘locationName’: u”Jonny Boston’s International Restaurant”, ‘lat’: Decimal(‘43.0776908’), ‘long’: Decimal(‘-70.9375484’), ‘address’: u'170 Main St, Newmarket, NH 03857, USA’}, {‘locationName’: u”Earth’s Harvest Kitchen & Juicery”, ‘lat’: Decimal(‘43.216483’), ‘long’: Decimal(‘-70.8801917’), ‘address’: u'835 Central Ave, Dover, NH 03820, USA’}, {‘locationName’: u'99 Restaurants’, ‘lat’: Decimal(‘43.223181’), ‘long’: Decimal(‘-70.890096’), ‘address’: u'8 Hotel Drive, Dover, NH 03820, USA’}, {‘locationName’: u’The Oak House’, ‘lat’: Decimal(‘43.0791593’), ‘long’: Decimal(‘-70.93634159999999’), ‘address’: u'110 Main St, Newmarket, NH 03857, USA’}, {‘locationName’: u’Khaophums’, ‘lat’: Decimal(‘43.20079339999999’), ‘long’: Decimal(‘-70.8754399’), ‘address’: u'555 Central Ave, Dover, NH 03820, USA’}, {‘locationName’: u’Fat Dog Kitchen’, ‘lat’: Decimal(‘43.1983671’), ‘long’: Decimal(‘-70.8748751’), ‘address’: u'20 Third St, Dover, NH 03820, USA’}, {‘locationName’: u”Newick’s Lobster House”, ‘lat’: Decimal(‘43.1211092’), ‘long’: Decimal(‘-70.8325777’), ‘address’: u'431 Dover Point Rd, Dover, NH 03820, USA’}, {‘locationName’: u”Tucker’s”, ‘lat’: Decimal(‘43.2233817’), ‘long’: Decimal(‘-70.8880166’), ‘address’: u'238 Indian Brook Rd, Dover, NH 03820, USA’}, {‘locationName’: u”Applebee’s Grill + Bar”, ‘lat’: Decimal(‘43.22364779999999’), ‘long’: Decimal(‘-70.88868479999999’), ‘address’: u'232 Indian Brook Rd, Dover, NH 03820, USA’}]"



if __name__ == '__main__':
  app.run(debug=True)