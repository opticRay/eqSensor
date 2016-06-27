from flask import render_template
from app import app
from flask import Flask, jsonify
from flask import request
from flask import abort
from werkzeug import secure_filename
import os
import uuid
import json


eqEvent = {
        'case': u'00',
        'magnitude': u'00',
        'degree': u'00',
        'max': u'00',
        'color':u'1'
    }


UPLOAD_FOLDER = 'app/static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           case=eqEvent['case'],
                           magnitude=eqEvent['magnitude'],
                           degree=eqEvent['degree'],
                           max=eqEvent['max'],
                           color=eqEvent['color'])


@app.route('/timeline')
def timeline():
    return render_template('timeline.html',
                           title='timeline')


@app.route('/tables')
def tables():
    return render_template('tables.html',
                           title='tables')


@app.route('/earthquakeExm/api/v1.0/event', methods=['POST'])
def create_event():
    if not request.json or not 'case' in request.json:
        abort(400)
    case1 = request.json['case']
    print case1

    eqEvent['case'] = request.json['case']
    eqEvent['magnitude'] = request.json['magnitude']
    eqEvent['degree'] = request.json['degree']
    eqEvent['max'] = request.json['max']
    eqEvent['color'] = request.json['color']
    return jsonify({'eqEvent': eqEvent}), 201


@app.route('/tables2', methods=['POST'])
def upload_img():
    if request.method == 'POST':
        file = request.files['file']
        print file.filename
        # extension = os.path.splitext(file.filename)[1]
        # f_name = str(uuid.uuid4()) + extension
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
        return json.dumps({'filename':filename})

 # @app.route('/earthquakeExm/api/v1.0/img', methods=['POST'])
 # def upload():
    # if request.method == 'POST':
    #     file = request.files['file']
    #     extension = os.path.splitext(file.filename)[1]
    #     f_name = str(uuid.uuid4()) + extension
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
    #     return json.dumps({'filename':f_name})



@app.route('/checkEvent', methods=['GET'])
def get_tasks():
    return jsonify({'eqEvent': eqEvent})
