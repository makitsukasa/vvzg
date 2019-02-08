#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://qiita.com/Kazuhito/items/4c8899d3784695726f3d

import os
import sys
import dlib
import cv2
import numpy
from PIL import ImageFont, ImageDraw, Image
import linecache
from getangles import get_angles

HEIGHT = 480
WIDTH = 640
RESIZE_RATE = 1
TRIM_RATE = 1/5
SHOW_IMAGE = True
SHOW_DOTS = False
SHOW_REAL = False
# http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
PREDICTOR_PATH = os.path.dirname(__file__) + "/shape_predictor_68_face_landmarks.dat"
WINDOW_RESIZEABLE = True

DETECTOR = dlib.get_frontal_face_detector()
PREDICTOR = dlib.shape_predictor(PREDICTOR_PATH)

VIDEO_INPUT = cv2.VideoCapture(0)

IMG = cv2.imread("Assets/vzg.png", cv2.IMREAD_UNCHANGED)
IMG_HEIGHT, IMG_WIDTH, _ = IMG.shape

while VIDEO_INPUT.isOpened():
	_, input_frame = VIDEO_INPUT.read()

	# trim center
	input_frame = input_frame[int(HEIGHT * TRIM_RATE) : -int(HEIGHT * TRIM_RATE),
		int(WIDTH * TRIM_RATE) : -int(WIDTH * TRIM_RATE)]

	# reduct for load reduction
	input_height, input_width = input_frame.shape[:2]
	input_frame = cv2.resize(input_frame,
			(int(input_width / RESIZE_RATE), int(input_height / RESIZE_RATE)))

	# mirrored
	input_frame = cv2.flip(input_frame, 1)

	# detect face
	dets = DETECTOR(input_frame, 1)

	for det in dets:
		shape = PREDICTOR(input_frame, det)
		euler_angles, p1, p2 = get_angles(shape)
		print(euler_angles, flush = True)

	cv2.waitKey(10)

linecache.clearcache()
VIDEO_INPUT.release()
cv2.destroyAllWindows()
