# Motion Detection Script

## Author: Oli Jaggard (oli@jaggard.uk)

## Description:

This is a motion detection script that captures video from an RTSP stream and performs motion detection within a defined region of interest (ROI). When motion is detected, it sends a notification and provides real-time feedback on the motion percentage.

## Features:

- Real-time motion detection
- Configurable threshold sensitivity
- Manual motion trigger (for ntfy troubleshooting)
- Customizable cooldown durations
- GUI window for visual feedback (optional)

## Prerequisites:

Before running the script, ensure you have the following dependencies installed:

- Python 3.x
- OpenCV
- NumPy

## Getting Started:

1. Clone this repository to your local machine.
2. modify the text files in the folder named 'args'.
3. Edit the input files in the 'args' folder as needed (see details below).
4. Install the `requirements.txt` file:

     `pip3 install -r requirements.txt`

5. Run the script using the following command:

     `python motion_detection_script.py [--disable-gui]`

## Usage:

Input Files (Inside 'args' Folder):

- `'arguments.txt': Specify the RTSP stream URL and threshold sensitivity (one per line).
  Example:
  rtsp://your_rtsp_stream_url
  [\newline] 30.0`

- `'cooldownmotion.txt': Set the cooldown duration (in seconds) between motion detection notifications (one number).
  Example:
  60`

- `'cooldownnotif.txt': Set the cooldown duration (in seconds) between general notifications (one number).
  Example:
  60`

- `'roi.txt': Define the Region of Interest (ROI) coordinates (X, Y, Width, Height) within the frame (one line).
  Example:
  X=100, Y=100, Width=400, Height=300`

## Manual Motion Trigger:

You can manually trigger motion detection for testing purposes by pressing the 'N' key. Note that this manual trigger is primarily intended for ntfy troubleshooting.

## Custom Notification Server:

To receive notifications, you need to specify your own ntfy server URL in the script:

`example("https://ntfy.sh/default")`


If you are not sure on how to setup your own ntfy server, follow the youtube link below:

https://youtu.be/poDIT2ruQ9M?si=XP2fcnDXnR0CaS_M
` Title: how did I NOT know about this?
Author: NetworkChuck
Details: Setting up an Ntfy service for local server or cloud(Linode)`

## Customization:

Real-time Motion Percentage Display:

The script has been customized to display the motion percentage in real-time on the RTSP stream with ROI window. The motion percentage will be displayed in green text and formatted as follows: Motion Sensitivity + %.

## Disabling the GUI:

If you wish to run the script without the GUI windows (useful for headless environments), you can add the --disable_gui argument when running the script:

- `python3 motion_detection_script.py --disable_gui`

## Additional Command-Line Arguments:

The script supports the following additional command-line arguments:

- `--argument_file FILE`: Specify a different text file containing arguments (default: `args/arguments.txt`).

- `--disable-gui`: Disable the GUI windows for a headless operation.

- `--no-binary`: Display only the RTSP stream with ROI window and not the binary mask GUI window (default: both windows are displayed).

For example, to use a custom argument file, you can run the script as follows:


- `python3 motion_detection_script.py --argument_file custom_args.txt`


## License:

This project is licensed under the MIT License.

## Acknowledgments:

- Thanks to the OpenCV and NumPy communities for their valuable contributions.

If you have any questions or encounter issues, please feel free to contact the author: oli@jaggard.uk.

Enjoy using the Motion Detection Script!
