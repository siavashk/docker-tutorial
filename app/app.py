from typing import List, Dict
from flask import Flask
import mysql.connector
import json

app = Flask(__name__)


def logs() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'logs'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM video_meta')
    results = [{time_stamp: [video_name, frame_height, frame_width, frames_per_second, number_of_frames]}
        for (time_stamp, video_name, frame_height, frame_width, frames_per_second, number_of_frames) in cursor]
    cursor.close()
    connection.close()

    return results


@app.route('/logs')
def index() -> str:
    return json.dumps({'logs': logs()})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
