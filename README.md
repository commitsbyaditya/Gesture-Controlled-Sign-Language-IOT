# Gesture-Controlled-Sign-Language-IOT

Your project allows users to control IoT devices detect sign language — without touching any device and display on the lcd A laptop camera to capture hand gestures. OpenCV and MediaPipe (computer vision tools) to detect and track hand movements. Machine Learning models to recognize gestures and sign language alphabets. how to build this in nodemcu give me the code each and everything step by step

<br/>
python -m src.train
<br/>
python -m src.evaluate
<br/>
python -m src.live_demo


## Installation

1. **Create and activate a virtual environment**
   - **Windows**
     ```powershell
     python -m venv venv
     venv\Scripts\activate
     ```
   - **macOS / Linux**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

2. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Install optional packages (recommended)**
   ```bash
   # For smoother PPT support (Windows + PowerPoint)
   pip install pywin32

   # Ensure Poppler binaries are installed and on PATH for pdf2image (Windows)
   ```

---

## Usage

1. Save your decks (PPT/PPTX/PDF/images) inside the `Presentation` folder.
2. Run the application:
   ```bash
   python main.py
   ```
3. Enter the file number or name when prompted. Press Enter to use raw images from the folder instead.
4. Keep your hand visible to the webcam. Use the gesture chart above to move through slides or draw.
5. Press `F` to toggle fullscreen, `Q` to exit.

> The app shows a small cyan circle for the tracked pointer. Drawings use thinner strokes for better readability.

---
