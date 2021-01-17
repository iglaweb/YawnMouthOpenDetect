import cv2
import dlib
from imutils import face_utils

from yawn_train import detect_utils, download_utils, inference_utils

(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

TEMP_FOLDER = "./temp"
dlib_landmarks_file = download_utils.download_and_unpack_dlib_68_landmarks(TEMP_FOLDER)
# dlib predictor for 68pts
predictor = dlib.shape_predictor(dlib_landmarks_file)
detector = dlib.get_frontal_face_detector()

img = cv2.imread(
    '/Users/igla/Desktop/Screenshot 2021-01-17 at 18.49.42.png', cv2.IMREAD_GRAYSCALE)
rects = inference_utils.detect_face_dlib(detector, img)

if len(rects) > 0:
    # determine the facial landmarks for the face region, then
    height_frame, width_frame = img.shape[:2]
    face_rect = rects[0]
    (start_x, start_y, end_x, end_y) = face_rect
    start_x = max(start_x, 0)
    start_y = max(start_y, 0)
    dlib_rect = dlib.rectangle(start_x, start_y, end_x, end_y)

    # https://pyimagesearch.com/wp-content/uploads/2017/04/facial_landmarks_68markup.jpg
    shape = predictor(img, dlib_rect)  # dlib.rectangle(0, 0, width_frame, height_frame))
    shape = face_utils.shape_to_np(shape)

    print(shape)
    print('Predictions size: ' + str(len(shape)))

    mouth = shape[mStart:mEnd]
    mouth_mar = detect_utils.mouth_aspect_ratio(mouth)
    print(mouth_mar)

    for (x, y) in shape:
        cv2.circle(img, (x, y), 2, (0, 0, 255), -1)
else:
    print('No face')
cv2.imshow("Dlib landmarks", img)
cv2.waitKey(0)
