import cv2
import subprocess
import argparse
import numpy as np
import time
import os

# Function to clear the console
def clear():
    os.system("cls")

clear()

# Function to read ROI coordinates from a file
def read_roi_coordinates(file_path):
    try:
        with open(file_path, 'r') as file:
            coordinates = file.readline().strip()
            # Split the coordinates by comma and space, then extract X, Y, Width, and Height values
            parts = coordinates.split(', ')
            roi_x = int(parts[0].split('=')[1])
            roi_y = int(parts[1].split('=')[1])
            roi_width = int(parts[2].split('=')[1])
            roi_height = int(parts[3].split('=')[1])
            return roi_x, roi_y, roi_width, roi_height
    except FileNotFoundError:
        print(f"Error: The specified file '{file_path}' was not found.")
        return None

# Function to read cooldown durations from files
def read_cooldown_duration(file_path, default_duration):
    try:
        with open(file_path, 'r') as file:
            duration = float(file.readline().strip())
            return duration
    except FileNotFoundError:
        print(f"Error: The specified file '{file_path}' was not found. Using default duration.")
        return default_duration

# Function to trigger motion detection manually
def trigger_motion_detection():
    global last_notification_time  # Declare last_notification_time as global
    current_time = time.time()
    if current_time - last_notification_time >= cooldown_duration_motion:
        # Notify that motion is detected
        print("Manual Motion Triggered! Sending notification...")

        # Execute the system command when motion is detected and suppress output
        subprocess.run(["curl",
            "-H", "Priority: urgent",
            "-H", "Tags: rotating_light,warning",
            "-H", "Title: Front Driveway",
            "-d", "Manual Motion Triggered",
            "https://your_ntfy_server/subscribed_topics"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        # Notify that the notification has been sent
        print("Notification sent!")

        last_notification_time = current_time

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Motion Detection Script")
parser.add_argument(
    "--argument_file", type=str, default="args/arguments.txt",
    help="Specify the text file containing arguments (default: args/arguments.txt)"
)
parser.add_argument(
    "--disable_gui", action="store_true",
    help="Disable GUI windows"
)
args = parser.parse_args()

# Read arguments from the specified text file
try:
    with open(args.argument_file, 'r') as file:
        rtsp_stream_url = file.readline().strip()
        threshold_sensitivity = float(file.readline().strip())
        insert_motion_sens = file.readline().strip()
except FileNotFoundError:
    print(f"Error: The specified text file '{args.argument_file}' was not found.")
    exit(1)

# Display the provided or default threshold sensitivity
print(f"Threshold Sensitivity: {threshold_sensitivity}%")

# Read ROI coordinates from the file
roi_coordinates = read_roi_coordinates('args/roi.txt')

# Check if ROI coordinates were successfully loaded
if roi_coordinates is not None:
    roi_x, roi_y, roi_width, roi_height = roi_coordinates
else:
    exit(1)

# Initialize the background subtractor
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

# Create a kernel for morphological operations (adjust the size as needed)
kernel = np.ones((5, 5), np.uint8)

# Initialize cooldown parameters
cooldown_duration_notif = read_cooldown_duration('args/cooldownnotif.txt', default_duration=60)
cooldown_duration_motion = read_cooldown_duration('args/cooldownmotion.txt', default_duration=60)
last_notification_time = 0  # Initialize last_notification_time

# Open the RTSP stream using the URL from the file
cap = cv2.VideoCapture(rtsp_stream_url)
print("\nRTSP stream connected...")

if args.disable_gui:
    print("\nNo GUI...")
if not args.disable_gui:  # Check if the GUI should be enabled
    # Set the initial window size and make them resizable
    cv2.namedWindow('Motion Detection', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Motion Detection', 800, 600)  # Set the initial size
    cv2.namedWindow('Raw RTSP Stream', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Raw RTSP Stream', 800, 600)  # Set the initial size

while True:
    ret, frame = cap.read()
    if not ret:
        break  # End of stream

    # Crop the frame to the defined ROI
    roi_frame = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

    # Apply background subtraction to the ROI
    fg_mask = bg_subtractor.apply(roi_frame)

    # Apply threshold to get binary motion mask
    _, binary_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)

    # Perform morphological operations to reduce noise
    binary_mask = cv2.erode(binary_mask, kernel, iterations=1)
    binary_mask = cv2.dilate(binary_mask, kernel, iterations=1)

    if binary_mask is not None:
        white_pixel_count = cv2.countNonZero(binary_mask)
        total_pixel_count = binary_mask.size
        motion_percentage = (white_pixel_count / total_pixel_count) * 100

        if motion_percentage > threshold_sensitivity:
            current_time = time.time()
            if current_time - last_notification_time >= cooldown_duration_motion:
                # Notify that motion is detected
                print("Motion Detected! Sending notification...")

                # Execute the system command when motion is detected and suppress output
                subprocess.run(["curl",
                    "-H", "Priority: urgent",
                    "-H", "Tags: rotating_light,warning",
                    "-H", "Title: Front Driveway",
                    "-d", "Motion Detected",
                    "https://your_ntfy_server/subscribed_topics"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)

                # Notify that the notification has been sent
                print("Notification sent!")

                last_notification_time = current_time

        # Display motion_percentage on the RTSP stream with ROI window
        text = f"Motion Percentage: {motion_percentage:.2f}%"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if not args.disable_gui:  # Check if the GUI should be enabled
        cv2.imshow('Motion Detection', binary_mask if binary_mask is not None else frame)

        frame_with_roi = frame.copy()
        cv2.rectangle(frame_with_roi, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)
        cv2.imshow('Raw RTSP Stream', frame_with_roi)

    key = cv2.waitKey(1) & 0xFF

    # Check for key presses
    if key == ord('q'):
        break
    elif key == ord('n') or key == ord('N'):
        # Simulate motion detection by pressing 'N' key
        trigger_motion_detection()

cap.release()

if not args.disable_gui:  # Check if the GUI should be enabled
    cv2.destroyAllWindows()
