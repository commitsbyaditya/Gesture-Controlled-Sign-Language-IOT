# 🎮 Gesture-Controlled Presentation Controller

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Enabled-green)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.21-orange)](https://developers.google.com/mediapipe)
[![cvzone](https://img.shields.io/badge/cvzone-1.6.1-lightblue)](https://github.com/cvzone/cvzone)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🧠 Project Overview

Control PowerPoint, PDF, or image-based presentations using hand gestures captured from a webcam. 
The application combines **OpenCV**, **MediaPipe**, and **cvzone** to track a single hand and translate finger poses into slide navigation and drawing actions.

---

## Features

- Pick a file from the `Presentation` folder (PPT/PPTX, PDF, JPG, PNG, BMP, GIF) or use pre-exported slide images.
- Smooth on-screen pointer with smaller brush size for precise annotations.
- Annotate slides by drawing with your index finger and remove the latest stroke with a multi-finger gesture.
- Toggle between windowed mode (with close/minimize/maximize controls) and fullscreen using the keyboard.
- Split view: fullscreen slides plus a resizable preview window of the webcam feed.

---

## Gestures & Keyboard Shortcuts

| Gesture | Description |
|----------|-------------|
| 👍 (Thumb Up) | Move to **previous slide** |
| 👋 (Pinky Up) | Move to **next slide** |
| 👆 (Index Finger) | Start **drawing** on the slide |
| ✌️ (Index + Middle) | Stop drawing |
| 🤟 (Index + Middle + Ring) | Undo last drawing |
| ❌ (Press `Q`) | Quit the program |

---

## Requirements

- Python 3.8 or newer
- Webcam
- Packages listed in `requirements.txt`

Optional dependencies:

- `pywin32` – enables high-quality PPT→image conversion using PowerPoint on Windows.
- `pdf2image` (already in requirements) + [Poppler](https://github.com/oschwartz10612/poppler-windows/releases) – allows rendering PDFs to images.

---

## Project Structure

```
Gesture-Controlled-IoT-Project/
├── Presentation/          # Place PPT/PPTX/PDF or images here
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── README.md
└── venv/                  # (Optional) Python virtual environment
```

When `main.py` starts, it ensures the `Presentation` folder exists and prompts you to choose a file from it.

---

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

## Troubleshooting

- **Slides do not load:** Ensure the selected file exists in `Presentation/` and has a supported extension.
- **PDF fallback message:** Install Poppler and keep it on your PATH so `pdf2image` can render pages.
- **PPT fallback placeholders:** Install `pywin32` (and have Microsoft PowerPoint installed) for native conversion, or export your deck to PDF.
- **Hand not detected:** Improve lighting and keep the webcam within range. Only one hand is tracked at a time.

---

## Contributing

Pull requests and feature suggestions are welcome! Feel free to open an issue describing your idea or bug report.