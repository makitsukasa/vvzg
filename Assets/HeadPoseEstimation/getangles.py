#!/usr/bin/env python

# https://www.learnopencv.com/head-pose-estimation-using-opencv-and-dlib/
# https://qiita.com/TaroYamada/items/e3f3d0ea4ecc0a832fac

import cv2
import numpy as np

def get_angles(face_shape):
	#2D image points.
	image_points = np.array([
		(face_shape.part(30).x, face_shape.part(30).y),     # Nose tip
		(face_shape.part(8).x,  face_shape.part(8).y),      # Chin
		(face_shape.part(36).x, face_shape.part(36).y),     # Left eye left corner
		(face_shape.part(45).x, face_shape.part(45).y),     # Right eye right corner
		(face_shape.part(48).x, face_shape.part(48).y),     # Left Mouth corner
		(face_shape.part(54).x, face_shape.part(54).y),     # Right mouth corner
	], dtype = "double")

	# 3D model points.
	model_points = np.array([
		(0.0, 0.0, 0.0),             # Nose tip
		(0.0, -330.0, -65.0),        # Chin
		(-225.0, 170.0, -135.0),     # Left eye left corner
		(225.0, 170.0, -135.0),      # Right eye right corne
		(-150.0, -150.0, -125.0),    # Left Mouth corner
		(150.0, -150.0, -125.0)      # Right mouth corner
	])

	# Camera internals
	camera_matrix = np.array([
		[480, 0, 240],
		[0, 480, 320],
		[0, 0, 1]
	], dtype = "double")

	dist_coeffs = np.zeros((4, 1)) # Assuming no lens distortion
	(_, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)

	rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
	proj_matrix = np.zeros(12).reshape((3, 4))
	proj_matrix[0:3, 0:3] = rotation_matrix
	euler_angles = cv2.decomposeProjectionMatrix(proj_matrix)[-1]
	# print("(pitch, yaw, roll):", euler_angles[0][0], euler_angles[1][0], euler_angles[2][0])

	(nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 500.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
	p1 = (int(image_points[0][0]), int(image_points[0][1]))
	p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

	return euler_angles, p1, p2
