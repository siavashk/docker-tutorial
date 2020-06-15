from datetime import datetime
from flask import Flask, request
import json
import os

from werkzeug.utils import secure_filename

from constants import UPLOAD_FOLDER, TIME_STAMP_FORMAT
from utils import allowed_file, get_logs, insert_into_db, process_video

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/logs',  methods=['GET'])
def logs() -> str:
    return json.dumps({'logs': get_logs()})


@app.route('/video',  methods=['POST'])
def video() -> str:
    file = request.files['file']
    if not file:
        return "Unable to fund a file key in the body of the request."

    if not allowed_file(file.filename):
        return "Unsupported video extension {:s}".format(file.filename)

    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    try:
        height, width, fps, frame_count = process_video(path)
    except IOError as err:
        os.remove(path) # clean up
        return str(err)

    os.remove(path) # clean up

    time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
    meta = (time_stamp, filename, height, width, fps, frame_count)

    insert_into_db(meta) # TODO: add try/except 

    return json.dumps(meta)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
