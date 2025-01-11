import cv2
from mtcnn.mtcnn import MTCNN
from pynput import keyboard
import threading
import tkinter as tk
from tkinter import messagebox
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
from PIL import ImageGrab  # To capture the entire screen
import time

# Initialize the MTCNN face detector
detector = MTCNN()

# Font settings for the warning text in the video
font = cv2.FONT_HERSHEY_SIMPLEX

# Email details using Gmail SMTP server
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'vp7714532@gmail.com'  # Sender email
SENDER_PASSWORD = 'tekb kyvd ynrf buzs'  # Use the App Password generated from Gmail
SUPERVISOR_EMAIL = 'vp7714532@gmail.com'  # Supervisor email (same as sender)

# Function to send an email with attachments
def send_email_with_attachments(face_screenshot, screen_screenshot, keylog_file):
    print(f"Preparing to send email with attachments: {face_screenshot}, {screen_screenshot}, {keylog_file}")
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = SUPERVISOR_EMAIL
    msg['Subject'] = "Multiple Faces Detected - Exam Terminated"

    # Attach all screenshots and the key log file
    for file in [face_screenshot, screen_screenshot, keylog_file]:
        if not os.path.exists(file):
            print(f"Error: File {file} does not exist.")
            continue  # Skip the attachment if the file does not exist

        with open(file, 'rb') as f:
            mime_type, encoding = mimetypes.guess_type(file)
            mime_type, mime_subtype = mime_type.split('/')
            part = MIMEBase(mime_type, mime_subtype)
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file)}"')
            msg.attach(part)

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        print("Email sent successfully!")

# Function to show a popup message and exit
def show_warning_and_exit(frame):
    # Save the frame with multiple faces as a screenshot
    face_screenshot = "multiple_faces_detected.png"
    cv2.imwrite(face_screenshot, frame)
    print(f"Saved face screenshot: {face_screenshot}")

    # Capture the entire screen
    screen_screenshot = "entire_screen.png"
    time.sleep(1)  # Wait for a moment before capturing the screen
    screen = ImageGrab.grab()
    screen.save(screen_screenshot)
    print(f"Saved screen screenshot: {screen_screenshot}")

    # Key log file name
    keylog_file = "keyfile.txt"

    # Check if the screenshots exist
    if os.path.exists(face_screenshot):
        print(f"{face_screenshot} exists.")
    else:
        print(f"Error: {face_screenshot} does not exist.")
    
    if os.path.exists(screen_screenshot):
        print(f"{screen_screenshot} exists.")
    else:
        print(f"Error: {screen_screenshot} does not exist.")

    # Send all attachments via email
    send_email_with_attachments(face_screenshot, screen_screenshot, keylog_file)

    # Create a simple tkinter window for the popup
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("COPY DETECTED", "Multiple faces detected. Exiting exam.")
    
    # Terminate the program
    os._exit(0)

# Function for real-time face detection
def face_detection():
    # Open webcam for video capture
    cap = cv2.VideoCapture(0)  # 0 is the default webcam

    while True:
        # Capture frame-by-frame from the webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB (since OpenCV uses BGR by default)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the frame
        faces = detector.detect_faces(frame_rgb)

        # Draw bounding boxes around detected faces
        for face in faces:
            x, y, width, height = face['box']
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

        # If multiple faces are detected, show a warning message and terminate
        if len(faces) > 1:
            # Display warning message on the frame
            warning_message = "Warning: Multiple Faces Detected!"
            cv2.putText(frame, warning_message, (50, 50), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            
            # Show the popup warning, take a screenshot of both the webcam feed and screen, and exit
            show_warning_and_exit(frame)

        # Display the resulting frame
        cv2.imshow('Live Multi-Face Detection', frame)

        # Press 'q' to exit the loop manually
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Function for logging key presses
def key_logging():
    def keyPressed(key):
        print(str(key))  # Print the key pressed
        with open("keyfile.txt", 'a') as logkey:
            try:
                # Attempt to write regular character keys
                char = key.char
                logkey.write(char)
            except AttributeError:
                # If it's a special key (like Shift, Ctrl, etc.), log it differently
                logkey.write(f"[{key}]")

    # Start listening to the keyboard inputs
    with keyboard.Listener(on_press=keyPressed) as listener:
        listener.join()

# Run the face detection and key logging simultaneously using threading
if __name__ == '__main__':
    # Create threads for face detection and key logging
    face_thread = threading.Thread(target=face_detection)
    key_thread = threading.Thread(target=key_logging)

    # Start both threads 
    face_thread.start()
    key_thread.start()

    # Join threads to the main thread
    face_thread.join()
    key_thread.join()
