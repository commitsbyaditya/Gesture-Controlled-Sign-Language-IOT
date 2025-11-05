from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np
import tempfile

try:
    from pptx import Presentation as PptxPresentation
except ImportError:
    PptxPresentation = None

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

try:
    from pdf2image import convert_from_path
except ImportError:
    convert_from_path = None

from PIL import Image
import tkinter as tk

# ==========================
# Parameters
# ==========================
# Webcam capture resolution
cam_width, cam_height = 1280, 720
# Webcam display window size (small window)
cam_display_width, cam_display_height = 320, 240

# Slide display - use fullscreen or screen resolution
try:
    # Try to get screen resolution
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    slide_width = screen_width
    slide_height = screen_height
except:
    # Fallback to full HD
    slide_width = 1920
    slide_height = 1080

default_slide_window_width = min(slide_width, 1280)
default_slide_window_height = min(slide_height, 720)

gestureThreshold = 300                     # Height threshold for gesture detection
folderPath = "Presentation"                # Folder with slides (images/PPT/PDF)
if not os.path.isdir(folderPath):
    os.makedirs(folderPath, exist_ok=True)
    print(f"Created missing folder '{folderPath}'. Add your PPT/PDF/Image files here.")

# ==========================
# File Processing Functions
# ==========================
def convert_ppt_to_images(ppt_path):
    """Convert PPT file to a list of images using Windows COM automation"""
    try:
        # Try using Windows COM automation with PowerPoint
        import win32com.client
        import pythoncom
        
        pythoncom.CoInitialize()
        ppt_app = win32com.client.Dispatch("PowerPoint.Application")
        ppt_app.Visible = 1
        
        presentation = ppt_app.Presentations.Open(os.path.abspath(ppt_path))
        images = []
        
        temp_dir = tempfile.gettempdir()
        
        for slide_num in range(1, presentation.Slides.Count + 1):
            slide = presentation.Slides(slide_num)
            temp_image_path = os.path.join(temp_dir, f"slide_{slide_num}.png")
            
            # Export slide as image
            slide.Export(temp_image_path, "PNG", 1920, 1080)
            
            # Load the exported image
            img = cv2.imread(temp_image_path)
            if img is not None:
                images.append(img)
            else:
                # Fallback to blank image
                img = Image.new('RGB', (1920, 1080), color='white')
                img_array = np.array(img)
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                images.append(img_bgr)
        
        presentation.Close()
        ppt_app.Quit()
        pythoncom.CoUninitialize()
        
        return images
    
    except ImportError:
        print("Note: pywin32 not installed. Using basic PPT conversion.")
        print("For better PPT support, install pywin32: pip install pywin32")
        print("Or convert your PPT to PDF first for full functionality.")
    except Exception as e:
        print(f"Error using COM automation: {e}")
        print("Falling back to basic conversion...")
    
    # Fallback: Create placeholder images with slide count
    try:
        if PptxPresentation is None:
            print("Warning: python-pptx is not installed. Install it with 'pip install python-pptx' for PPT fallback support.")
            print("Returning placeholder slide. Convert PPT to PDF or install dependencies for full functionality.")
            placeholder = Image.new('RGB', (1920, 1080), color='white')
            placeholder_array = np.array(placeholder)
            placeholder_bgr = cv2.cvtColor(placeholder_array, cv2.COLOR_RGB2BGR)
            cv2.putText(placeholder_bgr, "python-pptx missing", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 6)
            cv2.putText(placeholder_bgr, "Install: pip install python-pptx", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)
            return [placeholder_bgr]

        prs = PptxPresentation(ppt_path)
        images = []
        
        for slide_num, _ in enumerate(prs.slides):
            # Create a placeholder image with slide number
            img = Image.new('RGB', (1920, 1080), color='white')
            img_array = np.array(img)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Add text to indicate slide number
            cv2.putText(img_bgr, f"Slide {slide_num + 1}", 
                       (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 5)
            cv2.putText(img_bgr, "PPT conversion requires", 
                       (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (128, 128, 128), 3)
            cv2.putText(img_bgr, "PowerPoint installed or", 
                       (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (128, 128, 128), 3)
            cv2.putText(img_bgr, "convert PPT to PDF first", 
                       (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (128, 128, 128), 3)
            
            images.append(img_bgr)
        
        return images
    except Exception as e:
        print(f"Error reading PPT file: {e}")
        return []

def convert_pdf_to_images(pdf_path):
    """Convert PDF file to a list of images"""
    if convert_from_path is not None:
        try:
            # Convert PDF pages to images using pdf2image
            # Note: Requires poppler-utils to be installed on system
            # Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases
            images = convert_from_path(pdf_path, dpi=150)
            # Convert PIL Images to OpenCV format
            cv_images = []
            for img in images:
                img_array = np.array(img)
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                cv_images.append(img_bgr)
            return cv_images
        except Exception as e:
            print(f"Error converting PDF with pdf2image: {e}")
            print("Note: pdf2image requires poppler-utils to be installed.")
            print("Windows: Download poppler from https://github.com/oschwartz10612/poppler-windows/releases")
            print("Falling back to basic conversion...")
    else:
        print("Warning: pdf2image is not installed. Install it with 'pip install pdf2image' and ensure poppler is configured for full PDF support.")
        print("Falling back to basic conversion...")

    # Fallback: try with PyPDF2 (basic approach - can't render images directly)
    try:
        if PdfReader is None:
            raise ImportError("PyPDF2 is not installed. Install it with 'pip install PyPDF2' for PDF placeholder support.")

        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)
        images = []
        for page_num in range(num_pages):
            # Create placeholder image with page number
            img = Image.new('RGB', (1920, 1080), color='white')
            img_array = np.array(img)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Add text to indicate page number
            cv2.putText(img_bgr, f"Page {page_num + 1}", 
                       (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 5)
            cv2.putText(img_bgr, "PDF conversion requires poppler", 
                       (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (128, 128, 128), 3)
            cv2.putText(img_bgr, "Please install poppler-utils", 
                       (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (128, 128, 128), 3)
            
            images.append(img_bgr)
        return images
    except Exception as e2:
        print(f"Error with PyPDF2 fallback: {e2}")
        return []

def load_images_from_folder(folder_path):
    """Load all images from a folder"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    images = []
    files = sorted([f for f in os.listdir(folder_path) 
                   if os.path.splitext(f)[1].lower() in image_extensions], key=len)
    
    for file in files:
        img_path = os.path.join(folder_path, file)
        img = cv2.imread(img_path)
        if img is not None:
            images.append(img)
    
    return images, files

def select_file():
    """Prompt the user to choose a presentation file from the Presentation folder."""
    supported_extensions = ['.pptx', '.ppt', '.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.gif']

    files = [f for f in os.listdir(folderPath)
             if os.path.isfile(os.path.join(folderPath, f))
             and os.path.splitext(f)[1].lower() in supported_extensions]

    files.sort(key=str.lower)

    print("\nFiles available in the Presentation folder:")
    if files:
        for idx, name in enumerate(files, 1):
            print(f"  {idx}. {name}")
    else:
        print("  (No PPT/PDF/Image files found. Press Enter to use only images from subfolders, if any.)")

    print("\nType the file number or name (with or without extension). Press Enter to use images directly from the folder.")

    while True:
        selection = input("Selection: ").strip()

        if selection == "":
            return ""

        # Allow direct path (absolute or relative)
        if os.path.isfile(selection):
            return selection

        # Allow numeric selection
        if selection.isdigit():
            idx = int(selection)
            if 1 <= idx <= len(files):
                return os.path.join(folderPath, files[idx - 1])
            print("Invalid number. Please choose a valid file index.")
            continue

        # Try to match by exact filename (case-insensitive)
        matches = [f for f in files if f.lower() == selection.lower()]
        if not matches:
            # Try matching by filename without extension
            matches = [f for f in files if os.path.splitext(f)[0].lower() == selection.lower()]

        if len(matches) == 1:
            return os.path.join(folderPath, matches[0])
        elif len(matches) > 1:
            print("Multiple files match that name. Please be more specific or include the extension.")
        else:
            print("File not found. Please try again with a valid file name or index.")

# ==========================
# File Selection
# ==========================
print(f"\nPlace your PPT/PDF/Image files inside the '{folderPath}' folder.")
file_path = select_file()

if not file_path:
    print("No file selected. Using images from Presentation folder...")
    slides, pathImages = load_images_from_folder(folderPath)
    if not slides:
        print("No images found in Presentation folder!")
        exit()
else:
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext in ['.pptx', '.ppt']:
        print(f"Loading PPT file: {file_path}")
        slides = convert_ppt_to_images(file_path)
        if not slides or len(slides) == 0:
            print("Error: Could not load PPT file or file is empty!")
            exit()
        pathImages = [f"Slide {i+1}" for i in range(len(slides))]
    elif file_ext == '.pdf':
        print(f"Loading PDF file: {file_path}")
        slides = convert_pdf_to_images(file_path)
        if not slides or len(slides) == 0:
            print("Error: Could not load PDF file or file is empty!")
            print("Note: PDF conversion requires poppler-utils. Install it from:")
            print("https://github.com/oschwartz10612/poppler-windows/releases")
            exit()
        pathImages = [f"Page {i+1}" for i in range(len(slides))]
    elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
        print(f"Loading image file: {file_path}")
        img = cv2.imread(file_path)
        if img is not None:
            slides = [img]
            pathImages = [os.path.basename(file_path)]
        else:
            print("Error loading image file!")
            exit()
    else:
        print("Unsupported file type!")
        exit()

if not slides or len(slides) == 0:
    print("Error: No slides/pages loaded!")
    exit()

print(f"Total Slides/Pages: {len(slides)}")

# Prepare display windows with standard OS controls
cv2.namedWindow("Slides", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Slides", default_slide_window_width, default_slide_window_height)
cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Camera", cam_display_width, cam_display_height)

print("Controls: press 'f' to toggle fullscreen, 'q' to quit.")

# ==========================
# Webcam Setup
# ==========================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam!")
    exit()

cap.set(3, cam_width)
cap.set(4, cam_height)

# ==========================
# Hand Detector
# ==========================
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# ==========================
# Variables
# ==========================
imgList = []
delay = 30
buttonPressed = False
counter = 0
imgNumber = 0
delayCounter = 0
annotations = [[]]             # Stores all drawn paths
annotationNumber = -1
annotationStart = False
pointer_smoothing_factor = 0.35
smoothed_index_finger = None
window_fullscreen = False

# ==========================
# Main Loop
# ==========================
while True:
    # 1️⃣ Get webcam image
    success, img = cap.read()
    if not success:
        print("Error: Could not read from webcam!")
        break
    img = cv2.flip(img, 1)

    # 2️⃣ Get the current slide image - Display in FULL SIZE
    imgCurrent = slides[imgNumber].copy()
    
    # Resize slide to fit full screen display
    h_current, w_current = imgCurrent.shape[:2]
    # Resize to full screen while maintaining aspect ratio
    scale = min(slide_width / w_current, slide_height / h_current)
    new_w = int(w_current * scale)
    new_h = int(h_current * scale)
    imgResized = cv2.resize(imgCurrent, (new_w, new_h))
    
    # Create a black background and center the image for full screen
    background = np.zeros((slide_height, slide_width, 3), dtype=np.uint8)
    y_offset = (slide_height - new_h) // 2
    x_offset = (slide_width - new_w) // 2
    background[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = imgResized
    imgCurrent = background

    # 3️⃣ Find the hand and landmarks
    hands, img = detectorHand.findHands(img)  # Draws hand landmarks
    cv2.line(img, (0, gestureThreshold), (cam_width, gestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed is False:
        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]
        fingers = detectorHand.fingersUp(hand)

        # Interpolate index finger position for smoother drawing
        # Get current slide dimensions for coordinate mapping
        h_current, w_current = slides[imgNumber].shape[:2]
        scale = min(slide_width / w_current, slide_height / h_current)
        new_w = int(w_current * scale)
        new_h = int(h_current * scale)
        x_offset = (slide_width - new_w) // 2
        y_offset = (slide_height - new_h) // 2
        
        # Map from webcam coordinates directly to the resized image area
        xVal = int(np.interp(lmList[8][0], [0, cam_width], [0, new_w]))
        yVal = int(np.interp(lmList[8][1], [0, cam_height], [0, new_h]))
        
        # Clamp to image bounds
        xVal = max(0, min(new_w - 1, xVal))
        yVal = max(0, min(new_h - 1, yVal))
        
        # Convert to full screen coordinates (add offsets)
        raw_index_finger = (xVal + x_offset, yVal + y_offset)

        if smoothed_index_finger is None:
            smoothed_index_finger = raw_index_finger
        else:
            smoothed_index_finger = (
                int(smoothed_index_finger[0] * (1 - pointer_smoothing_factor) + raw_index_finger[0] * pointer_smoothing_factor),
                int(smoothed_index_finger[1] * (1 - pointer_smoothing_factor) + raw_index_finger[1] * pointer_smoothing_factor)
            )

        indexFinger = smoothed_index_finger

        # Draw a small pointer indicator for visual feedback
        pointer_radius = max(6, int(slide_width / 240))
        cv2.circle(imgCurrent, indexFinger, pointer_radius, (0, 255, 255), 2)

        # ==========================
        # Slide Navigation
        # ==========================
        if cy <= gestureThreshold:  # If hand is near top area
            # 👉 Go to previous slide
            if fingers == [1, 0, 0, 0, 0]:
                print("Previous Slide")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

            # 👈 Go to next slide
            if fingers == [0, 0, 0, 0, 1]:
                print("Next Slide")
                buttonPressed = True
                if imgNumber < len(slides) - 1:
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

        # ✍️ Draw mode (index finger)
        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            annotations[annotationNumber].append(indexFinger)
            # Scale circle size based on screen resolution
            circle_size = max(10, int(slide_width / 150))
            cv2.circle(imgCurrent, indexFinger, circle_size, (0, 0, 255), cv2.FILLED)

        else:
            annotationStart = False

        # 🗑️ Erase last drawn line (index + middle + ring)
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True

    else:
        annotationStart = False
        if not hands:
            smoothed_index_finger = None

    # ==========================
    # Delay logic to avoid multiple triggers
    # ==========================
    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    # ==========================
    # Draw annotations on current slide
    # ==========================
    # Scale line width based on screen resolution for better visibility
    line_width = max(12, int(slide_width / 160))
    for i, annotation in enumerate(annotations):
        for j in range(len(annotation)):
            if j != 0:
                cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), line_width)

    # ==========================
    # Display
    # ==========================
    if window_fullscreen:
        cv2.setWindowProperty("Slides", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    else:
        cv2.setWindowProperty("Slides", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
    cv2.imshow("Slides", imgCurrent)
    
    # Display webcam in SMALL window
    imgSmall = cv2.resize(img, (cam_display_width, cam_display_height))
    cv2.imshow("Camera", imgSmall)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('f'):
        window_fullscreen = not window_fullscreen
        if not window_fullscreen:
            cv2.setWindowProperty("Slides", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Slides", default_slide_window_width, default_slide_window_height)

# ==========================
# Cleanup
# ==========================
cap.release()
cv2.destroyAllWindows()
