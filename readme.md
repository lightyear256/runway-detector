#  Runway Alignment Decision System (OpenCV)

A Computer Vision based system that detects runway boundaries and determines whether the aircraft is aligned properly during landing approach.

This project simulates a basic visual landing guidance system using classical OpenCV techniques.

---

## 🚀 Features

- Detects left and right runway boundaries
- Calculates runway center
- Computes lateral deviation
- Estimates runway angle
- Smooths detection over multiple frames
- Displays alignment status:
  - ALIGNED
  - SLIGHT LEFT
  - SLIGHT RIGHT
  - MISALIGNED

---

## 🎥 Test Video
- Donwload this video and set its path inthe project


 **Google Drive Link:**  
https://drive.google.com/file/d/18Cql7Fb8ZDjXl7CXMOoZOpwGUeKZ-q3f/view?usp=sharing

---

## 🛠 Technologies Used

- Python
- OpenCV
- NumPy

---

## 📂 Project Structure
- runway_alignment_system.py
- runway.mp4
- README.md


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/lightyear256/runway-detector.git

cd runway-detector

pip install opencv-python numpy
# set the path here in runway_detect.py
VIDEO_SOURCE = "ENTER_YOUR_VIDEO_PATH"

python runway_alignment_system.py


```


