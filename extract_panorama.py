#!venv/bin/python3
import cv2
import numpy as np
import os
import sys

cv2.ocl.setUseOpenCL(False)


def extract_frames(video_path, output_folder, start_time, end_time, fps=1):
    """Extracts frames from a video file between start_time and end_time."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return 0

    video_fps = cap.get(cv2.CAP_PROP_FPS)  # Get video FPS
    start_frame = int(start_time * video_fps)
    end_frame = int(end_time * video_fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    frame_count = start_frame
    extracted_count = 0

    while frame_count <= end_frame:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % int(video_fps / fps) == 0:
            frame_filename = os.path.join(output_folder, f"frame_{extracted_count:03d}.jpg")
            cv2.imwrite(frame_filename, frame)
            extracted_count += 1

        frame_count += 1

    cap.release()
    return extracted_count

def load_images_from_folder(folder):
    """Loads all images from the specified folder and sorts them."""
    images = []
    for filename in sorted(os.listdir(folder)):  # Sorting ensures correct order
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path)
        if img is not None:
            images.append(img)
    return images

def stitch_images(images, output_filename):
    """Stitches images together using OpenCV's Stitcher and saves them."""
    if len(images) < 2:
        print("Skipping: Need at least two images to create a panorama.")
        return None, 0

    stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)

    try:
        status, panorama = stitcher.stitch(images)
        if status == cv2.Stitcher_OK:
            cv2.imwrite(output_filename, panorama)
            return panorama, os.path.getsize(output_filename)
        else:
            print(f"Skipping: Stitching failed with error code {status}")
            return None, 0
    except cv2.error as e:
        print(f"Skipping: OpenCV error - {e}")
        return None, 0

def find_longest_valid_panorama(video_path, fps=1):
    """Iterates through the video to extract all possible panoramas."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    video_duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
    cap.release()

    start_time = 0
    output_folder = "frames"

    while start_time < video_duration:
        print(f"\n[+] Starting at {start_time}s")
        best_end_time = start_time + 1
        prev_size = 0

        while best_end_time <= video_duration:
            print(f"  - Testing interval {start_time}s to {best_end_time}s")
            os.makedirs(output_folder, exist_ok=True)
            for file in os.listdir(output_folder):  # Clear old frames
                os.remove(os.path.join(output_folder, file))

            frame_count = extract_frames(video_path, output_folder, start_time, best_end_time, fps)
            if frame_count < 2:  # Not enough frames to stitch
                break

            images = load_images_from_folder(output_folder)
            output_filename = f"panorama_{start_time:04d}_{best_end_time:04d}.jpg"

            _, size = stitch_images(images, output_filename)

            if size > prev_size:
                prev_size = size
                best_end_time += 1  # Try extending
            else:
                if size > 0:
                    print(f"  -> Panorama saved: {output_filename} (Size: {size} bytes)")
                break  # Stop when file size stops increasing

        start_time += 1  # Move to the next second

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_panorama.py <video_path> [fps]")
        sys.exit(1)

    video_path = sys.argv[1]
    fps = float(sys.argv[2]) if len(sys.argv) > 2 else 1  # Default: 1 FPS

    find_longest_valid_panorama(video_path, fps)

