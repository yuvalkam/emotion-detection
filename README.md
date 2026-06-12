# Emotion Detection with Webcam in Google Colab

A webcam-based emotion detection project built with Python, OpenCV, FER, JavaScript, and Google Colab.

The program captures an image from the webcam, detects faces, identifies the strongest emotion, draws a bounding box around each face, and displays the processed image inside the notebook.

---

## 📋 Overview

This project uses the webcam through Google Colab and the browser.
Because Google Colab runs Python remotely, the webcam is accessed using JavaScript and then converted into an OpenCV image.

For every detected face, the system:

* Detects the face location
* Analyzes facial expressions
* Finds the emotion with the highest confidence score
* Draws a rectangle around the face
* Displays the emotion and score above the face

---

## 🗂️ File Structure

```text
├── emotion_detection.py     # Main Python code
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
```

---

## ✨ Features

* 📷 Capture images from the webcam in Google Colab
* 😀 Detect emotions using FER
* 👤 Detect multiple faces in one image
* 🟦 Draw bounding boxes around faces
* 📊 Display emotion confidence score
* 🔄 Repeat image capture in a loop
* 🛑 Stop the program by typing `q`

---

## 🧠 How It Works

### 1. Import Libraries

The project uses:

```python
import cv2
from fer import FER
import matplotlib.pyplot as plt
from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode, b64encode
import numpy as np
from PIL import Image as PILImage
import io
```

---

### 2. Initialize the Detector

```python
detector = FER()
```

This creates the FER emotion detector.

---

### 3. Capture Image from Webcam

The function `capture_image()` uses JavaScript to request access to the webcam:

```javascript
navigator.mediaDevices.getUserMedia({video: true})
```

The captured image is returned as a Base64 string.

---

### 4. Convert Image to OpenCV Format

```python
frame = js_to_image(capture_image())
```

The `js_to_image()` function converts the Base64 image into an OpenCV image.

---

### 5. Detect Emotions

```python
result = detector.detect_emotions(frame)
```

FER returns a list of detected faces and emotion scores.

Example result:

```python
{
    "box": [x, y, w, h],
    "emotions": {
        "angry": 0.01,
        "disgust": 0.00,
        "fear": 0.02,
        "happy": 0.89,
        "sad": 0.01,
        "surprise": 0.03,
        "neutral": 0.04
    }
}
```

---

### 6. Select the Strongest Emotion

```python
emotion, score = max(
    face["emotions"].items(),
    key=lambda item: item[1]
)
```

This selects the emotion with the highest confidence score.

---

### 7. Draw Results on the Image

```python
cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

cv2.putText(
    frame,
    f"{emotion}: {score:.2f}",
    (x, y - 10),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.9,
    (255, 0, 0),
    2
)
```

The program draws:

* A blue rectangle around the face
* The detected emotion above the face
* The confidence score next to the emotion

---

### 8. Display the Image

```python
img_pil = PILImage.open(io.BytesIO(bbox_to_bytes(frame)))
display(img_pil)
```

The processed image is converted and displayed in the Colab notebook.

---

## ⚙️ Main Functions

| Function                          | Purpose                                                    |
| --------------------------------- | ---------------------------------------------------------- |
| `js_to_image(js_reply)`           | Converts a Base64 image from JavaScript into OpenCV format |
| `bbox_to_bytes(bbox_array)`       | Converts the OpenCV image into JPEG bytes                  |
| `capture_image()`                 | Captures one image from the webcam using JavaScript        |
| `detector.detect_emotions(frame)` | Detects faces and emotions in the image                    |

---

## 🎯 Supported Emotions

FER can detect:

| Emotion  | Meaning                      |
| -------- | ---------------------------- |
| Angry    | Anger or frustration         |
| Disgust  | Disgust reaction             |
| Fear     | Fearful expression           |
| Happy    | Smile or positive expression |
| Sad      | Sadness                      |
| Surprise | Surprise or shock            |
| Neutral  | No strong emotion detected   |

---

## 🛠️ Technologies Used

| Technology      | Purpose                                |
| --------------- | -------------------------------------- |
| Python          | Main programming language              |
| OpenCV          | Image processing, rectangles, and text |
| FER             | Face emotion recognition               |
| NumPy           | Converts image bytes into arrays       |
| Pillow          | Displays processed images              |
| JavaScript      | Accesses the webcam in the browser     |
| Google Colab    | Runs the notebook environment          |
| IPython Display | Displays JavaScript and images         |

---

## 📦 Dependencies

Install the required packages:

```bash
pip install opencv-python-headless fer pillow
```

Optional, based on the imports in the code:

```bash
pip install matplotlib numpy ipython
```

Example `requirements.txt`:

```text
opencv-python-headless
fer
pillow
matplotlib
numpy
ipython
```

---

## 🚀 How to Run

1. Open Google Colab.
2. Create a new notebook.
3. Run the installation command:

```python
!pip install opencv-python-headless fer
!pip install pillow
```

4. Copy the Python code into a notebook cell.
5. Run the cell.
6. Allow webcam access when the browser asks for permission.
7. The program captures an image and displays the detected emotion.
8. Press **Enter** to capture another image.
9. Type `q` and press Enter to stop.

---

## ⚠️ Important Notes

This code is designed for **Google Colab**, not regular Python in VS Code.

It depends on:

```python
from google.colab.output import eval_js
from IPython.display import display, Javascript
```

These are used to run JavaScript inside the notebook and access the browser webcam.

In VS Code, this part will not work:

```python
eval_js("capture()")
```

For VS Code, webcam access should be done with OpenCV:

```python
cap = cv2.VideoCapture(0)
```

---

## ⚠️ Code Notes

In the current version of the code:

* `matplotlib.pyplot` is imported but not used.
* `b64encode` is imported but not used.
* The `pip install` commands are inside the `while True` loop.
* It is better to move installation commands to a separate Colab cell before running the main code.

Recommended separate Colab install cell:

```python
!pip install opencv-python-headless fer
!pip install pillow
```

Then run the main Python code in another cell.

---

## 📸 Example Output

```text
happy: 0.92
```

The detected face will be marked with a blue rectangle, and the emotion score will appear above it.

---

## 🔮 Future Improvements

* Move installation commands outside the loop
* Remove unused imports
* Add real-time video processing
* Save captured images automatically
* Add emotion history tracking
* Add a dashboard with statistics
* Convert the project to run locally with VS Code
* Build a web version with Flask or FastAPI

---

## 👨‍💻 Author

Developed as a Python computer vision project using OpenCV, FER, and Google Colab.
