from keras.preprocessing.image import img_to_array
import imutils
from keras.models import load_model
import numpy as np
import cv2
import keras

# parameters for loading data and images
detection_model_path = 'static/models/haarcascade_frontalface_default.xml'
emotion_model_path = 'static/models/_mini_XCEPTION.106-0.65.hdf5'

# hyper-parameters for bounding boxes shape
# loading models
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised",
            "neutral"]

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        keras.backend.clear_session()
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()


    def get_frame(self):
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        self.facialrec()
        ret, jpeg = cv2.imencode('.jpg', self.video.read()[1])
        return jpeg.tobytes()

    

    def facialrec(self):
        frame = self.video.read()[1]
        # reading the frame
        # frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                                flags=cv2.CASCADE_SCALE_IMAGE)
        # emotion classification result screen
        scoreboard = np.zeros((250, 300, 3), dtype="uint8")
        # camera frame
        camera_frame = frame.copy()
        if len(faces) > 0:
            faces = sorted(faces, reverse=True,
                        key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces
            # Extract the ROI of the face from the grayscale image, resize it to a fixed 48x48 pixels, and then prepare
            # the ROI for classification via the CNN
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (48, 48))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            preds = emotion_classifier.predict(roi)[0]
            emotion_probability = np.max(preds)
            label = EMOTIONS[preds.argmax()]

            for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
                # construct the label text
                text = "{}: {:.2f}%".format(emotion, prob * 100)
                # probability of classes of emotion
                w = int(prob * 300)
                cv2.rectangle(scoreboard, (7, (i * 35) + 5),
                            (w, (i * 35) + 35), (0, 0, 255), -1)
                cv2.putText(scoreboard, text, (10, (i * 35) + 23),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                            (255, 255, 255), 2)
                cv2.rectangle(camera_frame, (fX, fY), (fX + fW, fY + fH),
                            (0, 0, 255), 2)
                cv2.putText(camera_frame, label, (fX, fY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        # cv2.imshow('Face Cam', camera_frame)
        # cv2.imshow("Likelihoods", scoreboard)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break