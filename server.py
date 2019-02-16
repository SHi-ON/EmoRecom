#!/usr/bin/python3
# -*- coding: utf8 -*-

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Chao'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/my-link/')
def my_link():
  print('I got clicked!')

  return 'Click.'

if __name__ == '__main__':
  app.run(debug=True)