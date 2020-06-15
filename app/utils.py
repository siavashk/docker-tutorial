from typing import Dict, List, Tuple

import cv2
import mysql.connector

from constants import DB_CONFIG, ALLOWED_EXTENSIONS, INSERT_STATEMENT, TIME_STAMP_FORMAT


def allowed_file(filename) -> bool:
    """Function to check the extension of supplied files.

    Args:
        filename (str): Filename for the video

    Returns:
        bool: True if the file extension is supported, False otherwise.

    """
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_logs(config: Dict=DB_CONFIG) -> List[Tuple]:
    """Function to fetch logs from the database.

    Args:
        config (dict): Credential for connecting to the database

    Returns:
        logs (list[tuple]): List of tuples that correspond to timestamps return data for API requests.

    """
    connection = mysql.connector.connect(**config)

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM video_meta')
    results = [(ts.strftime(TIME_STAMP_FORMAT), vn, h, w, fps, count) for (ts, vn, h, w, fps, count) in cursor]
    cursor.close()
    connection.close()

    return results


def process_video(path: str) -> str:
    """Function to proess a video given its path.

    Args:
        path (str): Path to the video file

    Returns:
        meta (tuple): Tuple of meta data (height, width, frames_per_second, frame_count)

    """
    cap = cv2.VideoCapture(path)
    if cap.isOpened():
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return (height, width, fps, frame_count)  # named tuple would be better here.
    else:
        raise IOError("Unable to process the video {:s}. Make sure the video format is correct".format(path))


def insert_into_db(meta: Tuple, config: Dict=DB_CONFIG):
    """Function to insert meta data into the database

    Args:
        config (dict): Credential for connecting to the database

    Returns:
        None

    """
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(INSERT_STATEMENT, meta) # TODO: add try/except
    connection.commit()
    cursor.close()
    connection.close()
