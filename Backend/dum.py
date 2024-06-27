from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from keras.models import model_from_json
import threading

app = Flask(__name__)
CORS(app)

# Load face recognition model
haar_cascade = cv2.CascadeClassifier(r'C:\Users\suraj\Desktop\UI\Backend\haar_face.xml')
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(r'C:\Users\suraj\Desktop\UI\Backend\face_trained.yml')
people = ['Ben Afflek', 'Elton John', 'Jerry Seinfield', 'Madonna', 'Mindy Kaling']

# Load emotion detection model
json_file = open(r'C:\Users\suraj\Desktop\UI\Backend\emotion_model.json')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)
emotion_model.load_weights(r'C:\Users\suraj\Desktop\UI\Backend\emotion_model.h5')
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

def process_image(file):
    print("processing called")
    img_stream = file.stream
    img_bytes = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces_rect = haar_cascade.detectMultiScale(gray, 1.1, 4)
    result = []
    for (x, y, w, h) in faces_rect:
        print("loop")
        faces_roi = gray[y:y+h, x:x+w]
        label, _ = face_recognizer.predict(faces_roi)
        print( "I AM ",people[label])
        recognition_result = people[label]
        cv2.putText(img, people[label], (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), thickness=1)
        print("RECOGNITION DONE")
        print("Emotion detection start")
        roi_gray = gray[y:y+h, x:x+w]
        cropped_img = cv2.resize(roi_gray, (48, 48))
        cropped_img = np.expand_dims(cropped_img, axis=0) # these two extra dimension helps to match the input img
        cropped_img = np.expand_dims(cropped_img, axis=-1) # adding axis into end of aarray to represent signle channel(gray)
        print("MIDDLE EMOTION DETECTION")
        emotion_prediction = emotion_model.predict(cropped_img)
        print(emotion_prediction)
        maxindex = int(np.argmax(emotion_prediction))
        print(maxindex)
        emotion_result = emotion_dict[maxindex]
        print(emotion_result)
        cv2.putText(img, emotion_dict[maxindex], (x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        result.append({'person': recognition_result, 'emotion': emotion_result})

    _, jpeg = cv2.imencode('.jpg', img)
    jpeg_bytes = jpeg.tobytes()

    return result

def flask_thread():
    app.run(host='0.0.0.0', port=5000)

@app.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    file = request.files['image']
    print("what we recieved",file)
    response_data = process_image(file)
    return response_data, 200, {'Content-Type': 'image/jpeg'}

if __name__ == '__main__':
    flask_thread = threading.Thread(target=flask_thread)
    flask_thread.start()
