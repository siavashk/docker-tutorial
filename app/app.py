import cv2
from datetime import datetime
from flask import Flask, request, Response
import json
import mysql.connector
import os
import sys
from typing import List, Dict, Tuple
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['mp4'])

DB_CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'logs'
}

TIME_STAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

DB_CONNECTION = mysql.connector.connect(**DB_CONFIG)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_logs() -> List[Tuple]:
    cursor = DB_CONNECTION.cursor()
    cursor.execute('SELECT * FROM video_meta')
    results = [(ts.strftime(TIME_STAMP_FORMAT), vn, h, w, fps, count) for (ts, vn, h, w, fps, count) in cursor]
    cursor.close()

    return results


def process_video(path: str) -> str:
    cap = cv2.VideoCapture(path)
    if cap.isOpened():
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return (height, width, fps, frame_count)  # named tuple would be better here.
    else:
        raise IOError("Unable to process the video {:s}. Make sure the video format is correct".format(path))



@app.route('/logs',  methods=['GET'])
def logs() -> str:
    return json.dumps({'logs': get_logs()})


@app.route('/video',  methods=['POST'])
def video() -> str:
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        height, width, fps, frame_count = process_video(path)
        time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        os.remove(path) # clean up
        sql = "INSERT INTO video_meta (time_stamp, video_name, height, width, frames_per_second, frame_count) VALUES (%s, %s, %s, %s, %s, %s)"
        meta = (time_stamp, filename, height, width, fps, frame_count)
        cursor = DB_CONNECTION.cursor()
        cursor.execute(sql, meta)
        DB_CONNECTION.commit()
        return json.dumps(meta)
    else:
        return "Something went wrong"



if __name__ == '__main__':
    app.run(host='0.0.0.0')
