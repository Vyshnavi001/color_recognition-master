import cv2
from color_recognition_api import color_histogram_feature_extraction
from color_recognition_api import knn_classifier
import os
import os.path
import serial

cap = cv2.VideoCapture(0)
(ret, frame) = cap.read()
prediction = 'n.a.'
m=serial.Serial('COM3',9600)

# checking whether the training data is ready
PATH = './training.data'

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    print ('training data is ready, classifier is loading...')
else:
    print ('training data is being created...')
    open('training.data', 'w')
    color_histogram_feature_extraction.training()
    print ('training data is ready, classifier is loading...')
while True:
    # Capture frame-by-frame
    (ret, frame) = cap.read()

    # Check if the frame was captured successfully and has valid dimensions
    if ret and frame.shape[0] > 0 and frame.shape[1] > 0:
        cv2.putText(
            frame,
            'Prediction: ' + prediction,
            (15, 45),
            cv2.FONT_HERSHEY_PLAIN,
            3,
            (0, 0, 255),  # Color in BGR format (red)
        )

        # Display the resulting frame
        cv2.imshow('color classifier', frame)

        color_histogram_feature_extraction.color_histogram_of_test_image(frame)

        prediction = knn_classifier.main('training.data', 'test.data')
        if prediction=="apple":
            m.write(b's')
        elif prediction=="yellow" or prediction=="orange":
            m.write(b'r')
        elif prediction=="green":
            m.write(b'f')
        elif prediction=="blue" or prediction=="violet":
            m.write(b'l')
        elif prediction=="black" or prediction=="white":
            m.write(b'b')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        # When everything done, release the capture 
m.close()
cap.release() 
cv2.destroyAllWindows()		
