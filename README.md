# moviepano
Create panoramas from movies
# Extract Panorama from Video

This script extracts frames from a video, stitches them into panoramas, and finds the longest valid panorama where the file size keeps increasing. It iterates through each second of the video to determine the optimal segment for stitching.

## Features
- Extracts frames from a video within a given time range.
- Uses OpenCV to stitch frames into a panorama.
- Automatically finds the longest valid panorama by iterating through the video.
- Saves the generated panorama with an appropriate filename.

## Requirements
Make sure you have Python installed along with the required dependencies:

```bash
pip install opencv-python numpy
```

## Usage
Run the script with the following command:

```bash
python extract_panorama.py <video_path> [fps]
```

- `<video_path>`: Path to the input video file.
- `[fps]` (optional): Frames per second to extract. Default is `1` FPS.

### Example:
```bash
python extract_panorama.py example.mp4 2
```
This extracts frames at `2` FPS and attempts to generate panoramas.

## How It Works
1. **Frame Extraction**: The script extracts frames from the video between a given start and end time.
2. **Image Stitching**: OpenCV's Stitcher is used to create a panorama.
3. **Iterative Search**: It iterates through the video, testing different time intervals to find the longest sequence that produces a valid panorama.
4. **Saving Results**: If a valid panorama is found, it is saved with a filename indicating the time range.

## Output
- Extracted frames are stored in a `frames` directory.
- Generated panoramas are saved as `panorama_<start_time>_<end_time>.jpg`.
- The script prints progress updates and errors during execution.

## Notes
- OpenCV’s stitching function requires at least two frames to create a panorama.
- If stitching fails, the script skips that segment and moves to the next.
- Ensure the video has good horizontal motion for better results.

## License
This project is released under the MIT License.

