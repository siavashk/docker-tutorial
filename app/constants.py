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

INSERT_STATEMENT = "INSERT INTO video_meta (time_stamp, video_name, height, width, frames_per_second, frame_count) VALUES (%s, %s, %s, %s, %s, %s)"
