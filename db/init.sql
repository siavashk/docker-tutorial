CREATE DATABASE logs;
use logs;

CREATE TABLE video_meta (
  time_stamp TIMESTAMP,
  video_name VARCHAR(255),
  height INT,
  width INT,
  frames_per_second INT,
  frame_count INT
);
