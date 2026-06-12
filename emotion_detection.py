import cv2
from fer import FER
import matplotlib.pyplot as plt
from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode, b64encode
import numpy as np
from PIL import Image as PILImage
import io

detector = FER()

def js_to_image(js_reply):
    image_bytes = b64decode(js_reply.split(',')[1])
    np_arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(np_arr, flags=1)
    return img

def bbox_to_bytes(bbox_array):
    _, buffer = cv2.imencode('.jpg', bbox_array)
    return buffer.tobytes()

def capture_image():
    js = Javascript('''
        async function capture() {
            const div = document.createElement('div');
            const video = document.createElement('video');
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');

            const stream = await navigator.mediaDevices.getUserMedia({video: true});

            document.body.appendChild(div);
            div.appendChild(video);

            video.srcObject = stream;

            await new Promise((resolve) => video.onloadedmetadata = resolve);

            video.play();

            await new Promise((resolve) => setTimeout(resolve, 1000));

            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            stream.getTracks()[0].stop();

            const image = canvas.toDataURL('image/jpeg', 0.8);

            div.remove();

            return image;
        }

        capture();
    ''')

    display(js)
    data = eval_js('capture()')
    return data

while True:
    frame = js_to_image(capture_image())

    if frame is None:
        print("Error: Could not read frame.")
        break

    !pip install opencv-python-headless fer
    !pip install pillow

    result = detector.detect_emotions(frame)

    if result:
        for face in result:
            (x, y, w, h) = face['box']

            emotion, score = max(
                face['emotions'].items(),
                key=lambda item: item[1]
            )

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

            cv2.putText(
                frame,
                f'{emotion}: {score:.2f}',
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 0, 0),
                2
            )

    img_pil = PILImage.open(
        io.BytesIO(bbox_to_bytes(frame))
    )

    display(img_pil)

    if input() == 'q':
        break