import cv2
import numpy as np
import os

# Prompt user for directory and change working directory
print("This script will blend a series of images into 'output.jpg'.")
print("Images are named frame_0001.jpg, frame_0002.jpg, etc.")
os.chdir(input(r"Enter directory path: "))

# Get number of frames to process
num_frames = int(input("Enter number of frames: "))

# Load frames into a list
frames = []
for i in range(1, num_frames + 1):
    img = cv2.imread(f'frame_{i:04d}.jpg')
    if img is not None:
        frames.append(img)
    else:
        print(f"frame_{i:04d}.jpg error!")

# Exit if no images loaded
if len(frames) == 0:
    print("No images loaded. Exiting.")
else:
    # Blend modes and descriptions
    modes = [
        "mean", "add", "multiply", "screen",
        "max", "min", "median", "difference",
        "geometric_mean", "stddev", "range", "parity"
    ]
    mode_descriptions = [
        "Average pixel values across all frames.",
        "Sum pixel values, then normalize to 0-255.",
        "Multiply pixel values, resulting in darker images.",
        "Inverse multiply, resulting in lighter images.",
        "Take the maximum value for each pixel across frames.",
        "Take the minimum value for each pixel across frames.",
        "Take the median value for each pixel across frames.",
        "Average of absolute differences from the first frame.",
        "Geometric mean of pixel values across frames.",
        "Standard deviation of pixel values (shows change).",
        "Range (max-min) of pixel values across frames.",
        "Parity: even/odd sum of pixel values."
    ]

    arr = np.stack(frames, axis=0)  # Stack frames into a single array

    # Blend function for different modes
    def blend(arr, mode):
        if mode == "mean":
            return np.mean(arr, axis=0).astype(np.uint8)
        elif mode == "add":
            summed = np.sum(arr.astype(np.float32), axis=0)
            normalized = summed / len(arr)
            return np.clip(normalized, 0, 255).astype(np.uint8)
        elif mode == "multiply":
            blended = np.prod(arr.astype(np.float32) / 255, axis=0)
            return np.clip(blended * 255, 0, 255).astype(np.uint8)
        elif mode == "screen":
            blended = 1 - np.prod(1 - arr.astype(np.float32) / 255, axis=0)
            blended = blended / (1 if len(arr) == 1 else np.power(len(arr), 0.5))
            return np.clip(blended * 255, 0, 255).astype(np.uint8)
        elif mode == "max":
            return np.max(arr, axis=0).astype(np.uint8)
        elif mode == "min":
            return np.min(arr, axis=0).astype(np.uint8)
        elif mode == "median":
            return np.median(arr, axis=0).astype(np.uint8)
        elif mode == "difference":
            blended = np.abs(arr.astype(np.int16) - arr[0].astype(np.int16))
            return np.clip(np.mean(blended, axis=0), 0, 255).astype(np.uint8)
        elif mode == "geometric_mean":
            blended = np.exp(np.mean(np.log(arr.astype(np.float32) + 1), axis=0)) - 1
            return np.clip(blended, 0, 255).astype(np.uint8)
        elif mode == "stddev":
            blended = np.std(arr.astype(np.float32), axis=0)
            return np.clip(blended * 2, 0, 255).astype(np.uint8)  # Scaled for visibility
        elif mode == "range":
            blended = np.max(arr, axis=0) - np.min(arr, axis=0)
            return blended.astype(np.uint8)
        elif mode == "parity":
            blended = (np.sum(arr, axis=0) % 2) * 255
            return blended.astype(np.uint8)
        else:
            return None

    # User interaction loop
    while True:
        print("\nChoose blend mode by number:")
        for idx, (m, desc) in enumerate(zip(modes, mode_descriptions), 1):
            print(f" {idx}. {m:<10} - {desc}")
        print(" 0. all          - Use all modes.")
        print("Type /bye to exit.\n")
        mode_input = input("Blend mode number: ").strip().lower()

        if mode_input == "/bye":
            print("Exiting.")
            break

        if mode_input == "0":
            # Save all blend modes
            for m in modes:
                blended = blend(arr, m)
                outname = f"output_{m}.jpg"
                cv2.imwrite(outname, blended)
                print(f"Blended image saved as {outname}")
        else:
            try:
                mode_idx = int(mode_input) - 1
                if 0 <= mode_idx < len(modes):
                    mode = modes[mode_idx]
                    blended = blend(arr, mode)
                    outname = f"output_{mode}.jpg"
                    cv2.imwrite(outname, blended)
                    print(f"Blended image saved as {outname}")
                else:
                    print("Unknown mode number.")
            except ValueError:
                print("Please enter a valid number.")