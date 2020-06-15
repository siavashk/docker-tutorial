CREATE DATABASE logs;
use logs;

CREATE TABLE video_meta (
  time_stamp VARCHAR(25),
  video_name VARCHAR(255),
  frame_height INT,
  frame_width INT,
  frames_per_second INT,
  number_of_frames INT
);

INSERT INTO video_meta
  (time_stamp, video_name, frame_height, frame_width, frames_per_second, number_of_frames)
VALUES
  ('2020-06-14 17:55:44', 'some_video.mp4', 480, 640, 60, 1800),
  ('2020-06-14 17:59:12', 'some_other_video.mp4', 720, 1280, 30, 150);
