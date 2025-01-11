# KeenLogger
It integrates real-time face detection, keylogging, and automatic email reporting in order to avoid cheating in an online examination. It uses various tools and technologies that would ensure a secure environment and catch suspicious activities like more than one face appearing in the camera feed.


# Features

1. Real-Time Face Detection:
   *Uses MTCNN (Multi-Task Cascaded Convolutional Neural Networks) for accurate detection of faces in a live webcam feed.
   *Triggers a warning and terminates the exam if multiple faces are detected.

2. Keylogging:
   *Records all key presses using the pynput library and saves them in a log file (keyfile.txt).

3. Automated Reporting:
   *Captures and emails:
    *A screenshot of the webcam feed showing multiple faces.
    *A screenshot of the entire screen.
    *The keylog file.
   *It uses the Gmail SMTP server for secure sending of emails.

3. Popup Alerts:
   *Warns the user and ends the exam when it detects more than one face.

5. Multi-Threading:
   *Faces are detected in parallel with keylogging for optimal performance.

# Installation

1. Clone the Repository:
   git clone https://github.com/PatilVedant25/KeenLogger.git
   cd project-name

2. Install Dependencies:
   Use the following command to install the required Python libraries:
    pip install -r requirements.txt

3. Set Up Email Credentials:
   Open the script and configure these variables
    SENDER_EMAIL = 'your_email@gmail.com'  # Replace with your Gmail address
    SENDER_PASSWORD = 'your_app_password'  # Generate and use an App Password
    SUPERVISOR_EMAIL = 'supervisor_email@gmail.com'  # Replace with the supervisor's email

4. Run the Application:
   python main.py

# How It Works
  
1. Face Detection:
   *Webcam feed is processed in real-time to detect faces.
   *In case more than one face is detected:
   *Warning message is shown on the video feed.
   *Images of the webcam and screen are captured.
   *System halts and notifies for infringement.

2. Keylogging:
   *Keystrokes are logged into a file called keyfile.txt.

3. Automated Email Reporting:
   *Images of the webcam and the screen along with the keyfile.txt are sent to the supervisor's email account.

4. Popup Alerts:
   *Notifies the user by showing the message "Multiple faces detected. Exiting exam."

# Dependencies
Ensure you have the following Python libraries installed:

opencv-python
mtcnn
pynput
pillow
tkinter (built-in with Python)
smtplib (built-in with Python)
email (built-in with Python)

# Usage Scenarios

1. Online Examination Proctoring:
   *Prevents unauthorized presence by detecting multiple faces.
   *Monitors and logs keyboard activity during the exam.

2. Remote Monitoring:
   *Tracks activities in sensitive environments.

3. Workplace Security:
   *Ensures secure access to systems by monitoring for multiple users.

# Future Enhancements
1. Background Audio Recording:
   *Capture ambient sound during the session for additional context.

2. AI-Based Content Detection:
   *Analyze screen content for cheating materials or other suspicious activities.

3. Cloud Storage:
   *Store logs and screenshots in the cloud for long-term analysis.

4. Customization:
   *Enable configurable options such as thresholds for detected faces.

# Contributing
Contributions are welcome! Feel free to fork this repository and submit pull requests for improvements or new features.

# Acknowledgments

OpenCV: For real-time video processing.
MTCNN: For accurate face detection.
Pynput: For seamless keylogging.
Pillow: For capturing screenshots.
