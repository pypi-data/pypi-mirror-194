#################################################################################
# Copyright (C) 2023
# Juan Carlos Perez Castellanos <cuyopc@gmail.com>
# Maria Frine de la Rosa Gutierrez <frinedlr@gmail.com>
#
# This file is part of fvmouse.
#
# fvmouse can not be copied and/or distributed without the express
# permission of Juan Carlos Perez Castellanos or Maria Frine de la Rosa Gutierrez
##################################################################################

# !/usr/bin/env python3
"""
Face movement detection and execution of mouse movements
Detection covers 68 points in the face, covering jaw, eyes, eyebrows, nose and mouth, to be used to calculate face tilt
"""
import os
import time

import dlib
import cv2 as cv
import numpy as np
import pyautogui
from statistics import mean

ENABLED = False
KILL = False

screen_size_x, screen_size_y = pyautogui.size()
screen_size_x = screen_size_x + 480
screen_size_y = screen_size_y + 150
screen_center_x = screen_size_x // 2
screen_center_y = screen_size_y // 2

last_record_x = 0
last_record_y = 0

last_last_x = 0
last_last_y = 0

this_dir, _ = os.path.split(__file__)
landmarks_dat = os.path.join(this_dir, "data",
                             "shape_predictor_68_face_landmarks.dat")

face_detector = dlib.get_frontal_face_detector()
landmark_detector = dlib.shape_predictor(landmarks_dat)

face_center_x = None
face_offset_x = None
face_center_y = None
face_offset_y = None

# avoid vibrations.
movement_threshold = 8

# don't calculate if:
movement_minimal_thresold = 1.10

# Calibration variables
font = cv.FONT_HERSHEY_SIMPLEX
font_scale = 4
color = (0, 0, 0)
thickness = 4
radius = 50
image = np.zeros([screen_size_y * 2, screen_size_x * 2, 3], dtype=np.uint8)
image.fill(255)
image_backup = image.copy()


# ---------------------- START CALIBRATION SECTION ----------------------------


def generate_calibration_image(center):
    """ Generate a calibration instructions image """
    text = "Please point nose to the red circle"
    coordinates = (screen_center_x * 2 - 1000, screen_center_y * 2 - 300)
    calibration_image = cv.circle(
        image_backup.copy(), center=center,
        radius=radius, color=(0, 0, 255), thickness=-1)
    calibration_image = cv.putText(calibration_image, text, coordinates,
                                   font, font_scale, color, thickness)
    return calibration_image


def capture_calibration_frames(camera, coordinates_countdown, coordinates_now,
                               calibration_image, window_name):
    """ Perform a capture of 20 frames for a user's face fixed position
    """
    cv.imshow(window_name, calibration_image)
    cv.waitKey(1)
    for i in range(3, 0, -1):
        time.sleep(1)
        image_count = cv.putText(calibration_image.copy(), f"{i}",
                                 coordinates_countdown, font, font_scale,
                                 thickness)
        cv.imshow(window_name, image_count)
        cv.waitKey(1)
    time.sleep(1)
    image_count = cv.putText(calibration_image.copy(), "Now!",
                             coordinates_now, font, font_scale, color,
                             thickness)
    cv.imshow(window_name, image_count)
    cv.waitKey(1)
    face_frame_list = []
    # Capture and store 20 frames for each position
    while len(face_frame_list) < 20:
        ret, frame = camera.read()
        face_frame_list.append(frame)
    return face_frame_list


def analyze_calibration_frames(face_frame_list):
    """ Analyze the frames to determine x and y position values for a given set
    of frames
    """
    offset_position_x = []
    offset_position_y = []
    for frame in face_frame_list:
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_gray = cv.equalizeHist(frame_gray)
        faces = face_detector(frame_gray, 0)
        if not faces:
            continue
        all_landmarks = []
        face = faces[0]
        face_dlib_rect = dlib.rectangle(int(face.left()), int(face.top()),
                                        int(face.right()), int(face.bottom()))
        landmarks_detected = landmark_detector(frame_gray, face_dlib_rect)
        all_landmarks.append(landmarks_detected)
        if not all_landmarks and all_landmarks[0].num_parts == 68:
            continue
        landmarks = all_landmarks[0]
        offset_position_x.append(landmarks.part(30).x)
        offset_position_y.append(landmarks.part(30).y)
    position_x_mean = mean(offset_position_x)
    position_y_mean = mean(offset_position_y)
    return position_x_mean, position_y_mean


def calibrate_offsets() -> None:
    """ Use the camera and show instructions on screen to calibrate view offsets
    """
    global face_center_x, face_center_y, face_offset_x, face_offset_y
    camera = init_camera()

    # Common definitions for calibration background image
    window_name = 'Image'
    cv.namedWindow(window_name, cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty(window_name, cv.WND_PROP_FULLSCREEN, cv.WINDOW_NORMAL)
    cv.setWindowProperty(window_name, cv.WND_PROP_TOPMOST, 1)
    coordinates_countdown = (
        screen_center_x * 2 - 40, screen_center_y * 2 - 100)
    coordinates_now = (screen_center_x * 2 - 110, screen_center_y * 2 - 100)

    # -----------------------CENTER--------------------------------------------
    image_center_center = generate_calibration_image(
        (screen_center_x * 2, screen_center_y * 2))
    face_frame_list = capture_calibration_frames(camera,
                                                 coordinates_countdown,
                                                 coordinates_now,
                                                 image_center_center,
                                                 window_name)

    face_center_x, face_center_y = analyze_calibration_frames(face_frame_list)

    # ----------------------CENTER RIGHT---------------------------------------
    image_center_right = generate_calibration_image(
        (screen_size_x * 2 - radius, screen_center_y * 2))
    face_frame_list = capture_calibration_frames(camera,
                                                 coordinates_countdown,
                                                 coordinates_now,
                                                 image_center_right,
                                                 window_name)

    offset_position_x, _ = analyze_calibration_frames(face_frame_list)
    face_offset_x = abs(face_center_x - offset_position_x)

    # -----------------------CENTER BOTTOM-------------------------------------
    image_center_bottom = generate_calibration_image(
        (screen_center_x * 2, screen_size_y * 2 - radius))
    face_frame_list = capture_calibration_frames(camera,
                                                 coordinates_countdown,
                                                 coordinates_now,
                                                 image_center_bottom,
                                                 window_name)

    _, offset_position_y = analyze_calibration_frames(face_frame_list)
    face_offset_y = abs(face_center_y - offset_position_y)

    # Terminate window and print values
    cv.destroyWindow(window_name)
    cv.waitKey(1)

    print(f"face_center_x: {face_center_x}\n"
          f"face_center_y: {face_center_y}\n"
          f"face_offset_x: {face_offset_x}\n"
          f"face_offset_y: {face_offset_y}")


# ---------------------- END CALIBRATION SECTION ------------------------------


def calculate_fixed_cursor_position(landmarks):
    """ Calculate the current cursor position based on face position """
    global last_record_x, last_last_x
    global last_record_y, last_last_y
    if last_record_x:
        if last_last_x:
            abs_x = abs(last_record_x - landmarks.part(30).x)
            print('movement: ', abs_x)
            if abs_x < movement_threshold:
                if abs_x < movement_minimal_thresold:
                    print("inner if")
                    # 0 or non significant movement. Ignore
                    last_record_x, last_record_y = landmarks.part(
                        30).x, landmarks.part(30).y
                    return False, False
                # average current and two last records to get position.
                # TODO: Probar con mas frames (crear una queue) y comparar con todos
                # TODO: Probar con mas frames y SIN thresholds
                # landmarks.part(30).x = (last_last_x + last_record_x + landmarks.part(30).x) // 3
            if abs(last_record_y - landmarks.part(30).y) < movement_threshold:
                if abs(last_record_y - landmarks.part(
                        30).y) < movement_minimal_thresold:
                    last_record_x, last_record_y = landmarks.part(
                        30).x, landmarks.part(30).y
                    return False, False
                # landmarks.part(30).y = (last_last_y + last_record_y + landmarks.part(30).y) // 3
        last_last_x, last_last_y = last_record_x, last_record_y
    last_record_x, last_record_y = landmarks.part(30).x, landmarks.part(30).y
    # print(landmarks.part(30).x, landmarks.part(30).y)
    landmarks_offset_x = landmarks.part(30).x - face_center_x
    screen_position_x = screen_center_x - (
            (landmarks_offset_x * screen_center_x) // face_offset_x)
    landmarks_offset_y = landmarks.part(30).y - face_center_y
    screen_position_y = screen_center_y + (
            (landmarks_offset_y * screen_center_y) // face_offset_y)
    return screen_position_x, screen_position_y


def update_cursor_position(cursor_position, move=False) -> None:
    """ Update cursor position in screen """
    if cursor_position == (False, False):
        return
    if move:
        pyautogui.move(cursor_position[0], cursor_position[1])
    else:
        pyautogui.moveTo(cursor_position[0], cursor_position[1])


def add_facial_landmarks(frame, landmarks, point_start, point_end,
                         is_closed=False) -> None:
    """ Add the specified landmark points to the frame """
    points = [(landmarks.part(i).x, landmarks.part(i).y) for i in
              range(point_start, point_end + 1)]
    cv.polylines(frame, [np.array(points, dtype=np.int32)], is_closed,
                 (0, 200, 0), thickness=2, lineType=cv.LINE_8)


def annotate_frame(frame, landmarks) -> None:
    """ Annotate frame by drawing all the landmark components with fixed indexes for each section of the face """
    add_facial_landmarks(frame, landmarks, 0, 16)  # jaw
    add_facial_landmarks(frame, landmarks, 17, 21)  # eyebrow (left)
    add_facial_landmarks(frame, landmarks, 22, 26)  # eyebrow (right)
    add_facial_landmarks(frame, landmarks, 27, 30)  # nose (vertical)
    add_facial_landmarks(frame, landmarks, 30, 35,
                         is_closed=True)  # nose (horizontal)
    add_facial_landmarks(frame, landmarks, 36, 41, is_closed=True)  # eye (left)
    add_facial_landmarks(frame, landmarks, 42, 47,
                         is_closed=True)  # eye (right)
    add_facial_landmarks(frame, landmarks, 48, 59,
                         is_closed=True)  # mouth (external lip)
    add_facial_landmarks(frame, landmarks, 60, 67,
                         is_closed=True)  # mouth (internal lip)


def analyze_frame(frame) -> None:
    """ Perform analysis and annotate a captured frame, then calculate and update mouse position """
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    faces = face_detector(frame_gray, 0)
    if not faces:
        return
    all_landmarks = []
    face = faces[0]
    face_dlib_rect = dlib.rectangle(int(face.left()), int(face.top()),
                                    int(face.right()), int(face.bottom()))
    landmarks_detected = landmark_detector(frame_gray, face_dlib_rect)
    all_landmarks.append(landmarks_detected)
    if not all_landmarks and all_landmarks[0].num_parts == 68:
        return
    landmarks = all_landmarks[0]
    current_cursor_position = calculate_fixed_cursor_position(landmarks)
    update_cursor_position(current_cursor_position)
    annotate_frame(frame, landmarks)
    # Disabled imshow to work on threads
    # cv.imshow('Face landmarks detection', frame)


def init_camera():
    """ Initialize camera device with the best possible settings """
    camera_device = 0
    camera = cv.VideoCapture(camera_device)
    camera.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    camera.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    camera.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    camera.set(cv.CAP_PROP_FPS, 30)
    width = int(camera.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = camera.get(cv.CAP_PROP_FPS)
    print(f"Setting camera resolution to {width}x{height} at {int(fps)} FPS")
    if not camera.isOpened:
        print('Error opening video device')
        exit(0)
    return camera


def capture_frame() -> None:
    """ Capture frame and send it for processing """
    camera = None
    while True:
        if KILL:
            break
        if not ENABLED:
            if camera:
                camera.release()
            camera = None
            continue
        if not camera:
            camera = init_camera()
        ret, frame = camera.read()
        if frame is None:
            print('No captured frame. Exiting...')
            break
        analyze_frame(frame)
        try:
            if cv.waitKey(10) == 27:
                break
        except:
            pass


def main() -> None:
    capture_frame()


if __name__ == "__main__":
    main()
