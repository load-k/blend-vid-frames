import cv2
import os

def get_valid_input(prompt, cast_func=str, validate=lambda x: True, error_msg="Invalid input."):
    """
    Prompt user for input, cast and validate.

    Args:
        prompt (str): The prompt message to display.
        cast_func (callable): Function to cast input (e.g., int, float, str).
        validate (callable): Function to validate the input.
        error_msg (str): Error message to display on invalid input.

    Returns:
        The validated and casted input value.
    """
    while True:
        try:
            value = cast_func(input(prompt))
            if validate(value):
                return value
            print(error_msg)
        except Exception:
            print(error_msg)

def timestamp_to_frame_idx(timestamp, fps):
    """
    Convert HH:MM:SS or HH:MM:SS.mmm timestamp to frame index.

    Args:
        timestamp (str): Timestamp string in HH:MM:SS or HH:MM:SS.mmm format.
        fps (float): Frames per second of the video.

    Returns:
        int or None: Frame index corresponding to the timestamp, or None if invalid.
    """
    try:
        parts = timestamp.split(':')
        if len(parts) != 3:
            return None
        s_part = parts[2]
        if '.' in s_part:
            s, ms = s_part.split('.')
            s = float(s)
            ms = float('0.' + ms)
        else:
            s = float(s_part)
            ms = 0.0
        h = float(parts[0])
        m = float(parts[1])
        total_seconds = h * 3600 + m * 60 + s + ms
        return int(total_seconds * fps)
    except Exception:
        return None

def main():
    """
    Main function to extract frames from a video file based on user input.
    """
    # Get video file path from user
    video_path = input("Enter the path to the video file (.mov, .mp4): ").strip()
    if not os.path.isfile(video_path):
        print("Video file not found.")
        return

    # Open video to get frame info
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Failed to open video.")
        return
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Total frames in video: {total_frames}")

    # Get export directory from user and create it if it doesn't exist
    export_dir = input("Enter the export directory for frames: ").strip()
    os.makedirs(export_dir, exist_ok=True)

    # Get starting timestamp and validate it
    while True:
        start_time = get_valid_input(
            "Enter the starting timestamp (HH:MM:SS or HH:MM:SS.mmm): ",
            str,
            lambda t: len(t.split(':')) == 3,
            "Please enter timestamp in HH:MM:SS or HH:MM:SS.mmm format."
        )
        start_frame = timestamp_to_frame_idx(start_time, fps)
        if start_frame is None or start_frame >= total_frames:
            print("Invalid timestamp or timestamp beyond video length.")
            continue
        frames_left = total_frames - start_frame
        print(f"Frames remaining after {start_time}: {frames_left}")
        break

    # Get number of frames to extract, ensuring it does not exceed available frames
    num_frames = get_valid_input(
        "Enter the number of frames to extract (below 1000): ",
        int,
        lambda n: 1 <= n < 1000 and n <= frames_left,
        f"Please enter a number between 1 and {min(999, frames_left)}."
    )

    # Set video to start frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Extract and save frames
    for i in range(1, num_frames + 1):
        ret, frame = cap.read()
        if not ret:
            print("Reached end of video or failed to read frame.")
            break
        filename = os.path.join(export_dir, f"frame_{i:04d}.jpg")
        cv2.imwrite(filename, frame)

    cap.release()
    print(f"Extracted {i if ret else i-1} frames to {export_dir}")

if __name__ == "__main__":
    main()