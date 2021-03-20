import math
import os
import threading
import time
import urllib.parse
import webbrowser
import winsound

import cv2
import imutils
import numpy as np
import pyttsx3
import requests

# Import necessary modules
import speech_recognition as sr
from imutils.video import FPS, VideoStream

from .log import logerr, loginfo
from .voice import speak, speak_err

start_detection = False


def realtime_detection(
    classes,
):
    start_detection = True
    cap = cv2.VideoCapture(0)
    fps = cv2.CAP_PROP_FPS  # Frame Rate
    frame_count = 0
    detected = []

    loginfo("Loading YOLO V3 Model...")
    net = cv2.dnn.readNet("yolo_files/yolov3.weights", "yolo_files/yolov3.cfg")
    loginfo("Loaded YOLO V3 Model!")

    while start_detection:
        ret, frame_orig = cap.read()
        if ret:
            frame_count += 1
            if frame_count % 60 == 0:
                frame = cv2.resize(frame_orig, (640, 480))
                (H, W) = frame.shape[:2]
                scale = 1 / 255.0

                blob = cv2.dnn.blobFromImage(
                    frame,
                    scale,
                    (416, 416),
                    (0, 0, 0),
                    swapRB=True,
                    crop=False,
                )

                net.setInput(blob)

                outs = net.forward(get_output_layers(net))

                class_ids = []
                confidences = []
                boxes = []
                centers = []
                conf_threshold = 0.5
                nms_threshold = 0.4

                for out in outs:
                    for detection in out:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        if confidence > 0.5:
                            centerX = int(detection[0] * W)
                            centerY = int(detection[1] * H)

                            w = int(detection[2] * W)
                            h = int(detection[3] * H)
                            x = centerX - (w / 2)
                            y = centerY - (h / 2)
                            class_ids.append(class_id)
                            confidences.append(float(confidence))
                            boxes.append([x, y, w, h])
                            centers.append((centerX, centerY))

                indices = cv2.dnn.NMSBoxes(
                    boxes,
                    confidences,
                    conf_threshold,
                    nms_threshold,
                )
                texts = []

                for i in indices:
                    i = i[0]
                    box = boxes[i]
                    x = box[0]
                    y = box[1]
                    w = box[2]
                    h = box[3]
                    draw_prediction(
                        frame,
                        class_ids[i],
                        confidences[i],
                        round(x),
                        round(y),
                        round(x + w),
                        round(y + h),
                        round(H),
                        round(W),
                        fps,
                        classes,
                    )
                    if frame_count % 30 == 0:
                        centerX, centerY = centers[i][0], centers[i][1]

                        if centerX <= W / 3:
                            W_pos = "left "
                        elif centerX <= (W / 3 * 2):
                            W_pos = "center "
                        else:
                            W_pos = "right "

                        if centerY <= H / 3:
                            H_pos = "top "
                        elif centerY <= (H / 3 * 2):
                            H_pos = "mid "
                        else:
                            H_pos = "bottom "
                        texts.append(H_pos + W_pos + classes[class_ids[i]].capitalize())
                        detected.append(classes[class_ids[i]].capitalize())

                cv2.imshow("Live Detection", frame)
                loginfo(f"Objects Detected: {detected}")
                loginfo(f"Detections: {texts}")

                for obj in texts:
                    speak(texts[obj])

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):

                    break
    cap.release()
    cv2.destroyAllWindows()
    start_detection = False


# Function for object detection
# Returns whether object found or not, its degree and direction if found
def objectdetection(objname, CLASSES_Mobile_DNN):
    timeout = time.time() + 15

    # Load the files - model and prototxt
    prototxt_file = "mobile_net_models/MobileNetSSD_deploy.prototxt.txt"
    model_file = "mobile_net_models/MobileNetSSD_deploy.caffemodel"
    confidence_value = 0.3  # Confidence Level to recognize the object

    COLORS = np.random.uniform(
        0,
        255,
        size=(len(CLASSES_Mobile_DNN), 3),
    )  # Load Colors for each class

    loginfo("Loading model...")
    net = cv2.dnn.readNetFromCaffe(
        prototxt_file,
        model_file,
    )  # Load the DNN Model from Caffe files
    loginfo("Model information obtained!")

    loginfo("Starting video stream...")
    webcam = VideoStream(src=0).start()  # Start Webcam
    time.sleep(2.0)
    fps = FPS().start()

    frame_width = 600  # Resize width for each fram in video
    user_x = frame_width / 2
    user_y = frame_width

    while True:
        frame = webcam.read()  # Read from Webcam
        frame = imutils.resize(
            frame,
            width=frame_width,
        )  # Resize image read from webcam frame by frame
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)),
            0.007843,
            (300, 300),
            127.5,
        )
        net.setInput(blob)
        detections = net.forward()  # Start detections
        fl = False
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if (
                confidence > confidence_value
            ):  # Only work if confidence value is above specified
                idx = int(detections[0, 0, i, 1])
                if objname in CLASSES_Mobile_DNN[idx]:
                    fl = True  # Object found = True
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    label = f"{CLASSES_Mobile_DNN[idx]}: {confidence * 100:.2f}%"
                    cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(
                        frame,
                        label,
                        (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        COLORS[idx],
                        2,
                    )
                    centerX = (endX + startX) / 2
                    centerY = (endY + startY) / 2
                    cv2.line(
                        frame,
                        (int(user_x), int(user_y)),
                        (int(centerX), int(centerY)),
                        (255, 0, 0),
                        7,
                    )
                    dir = 0
                    if centerX > user_x:
                        dir = 1
                    elif centerX < user_x:
                        dir = -1
                    deg = math.degrees(
                        math.atan(abs(centerX - user_x) / abs(centerY - user_y)),
                    )

        cv2.imshow("Camera", frame)  # Don't open Frame Window to show live detections!
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if time.time() >= timeout:
            break
        fps.update()

    fps.stop()  # Stop counting FPS
    loginfo(f"Elapsed Time: {fps.elapsed():.2f}")
    loginfo(f"Approx. FPS: {fps.fps():.2f}")
    cv2.destroyAllWindows()  # Destroy Created Windows
    webcam.stop()  # Stop webcam
    return fl, deg, dir


def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers


# Draw Boxes on objects to identify them
def draw_prediction(
    img,
    class_id,
    confidence,
    x,
    y,
    x_plus_w,
    y_plus_h,
    frame_height,
    frame_width,
    fps,
    classes,
):
    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
    color_exitkey = (0, 0, 255)  # Red
    label = str(classes[class_id]).capitalize()
    percent = str(f"{confidence * 100:.2f}%")
    label_percent = label + ": " + percent
    color = COLORS[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    exit_text_h = round((5 / 100) * frame_height)
    exit_text_w = round((5 / 100) * frame_width)
    cv2.putText(
        img,
        "Press q to exit",
        (exit_text_h, exit_text_w),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color_exitkey,
        2,
    )
    cv2.putText(
        img,
        f"FPS: {fps}",
        (exit_text_h, exit_text_w + 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color_exitkey,
        2,
    )
