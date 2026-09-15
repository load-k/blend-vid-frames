# Frame Blending Toolkit

This minimum toolkit has Python scripts to extract frames from a video and blend them using image blending techniques. Ideal for creative video processing, visual effects, and data visualization. Do whatever you want with it. 

## Use Cases
- **Visual Effects**: Create unique blended images from video sequences.
- **Motion Analysis**: Highlight movement across frames using statistical blending.
- **Data Visualization**: Summarize video content into a single image using mean, median, or other methods.
---

[_Example video_](https://www.youtube.com/watch?v=rxaS78Twxyw) converted into blended images:

> mean
![output_mean](https://github.com/user-attachments/assets/1402dcc4-a53d-499c-b15d-c9bf5cb5cf0a)
> stddev
![output_stddev](https://github.com/user-attachments/assets/a6dd415d-93da-4be5-ac6e-cc80252397ee)
> range
![output_range](https://github.com/user-attachments/assets/f4c06210-21b5-4ad9-b95f-94673062f796)
> parity
![output_parity](https://github.com/user-attachments/assets/69ea88d2-b9aa-4b8b-8737-14412f063699)

---
# How to use:

- Have a Video (`.mp4` or `.mov`)
- Install Python Requirements:
```powershell
pip install opencv-python numpy
```
- Run and Follow the Scripts:
```
python "extract frames.py"
```
```
python "blend jpg frames.py"
```
> THATS IT!

## Workflow Example for more Detail

### 1. Extract Frames from Video
Run `extract frames.py`:

```powershell
python "extract frames.py"
```
- **Input**: Path to video file (e.g., `.mp4`, `.mov`).
- **Export Directory**: Where frames are saved.
- **Timestamp**: Start in `HH:MM:SS` or `HH:MM:SS.mmm` format.
- **Number of Frames**: Frames to extract (up to 999).

**Output:**
Frames saved as `frame_{i:04d}.jpg` (e.g., `frame_0001.jpg`).

> **Note:** The `frame_{i:04d}.jpg` format is used by both scripts. If you change this pattern, update it in both scripts.

### 2. Blend Extracted Frames
Run `blend jpg frames.py`:

```powershell
python "blend jpg frames.py"
```
- **Input**: Directory with extracted frames.
- **Number of Frames**: Frames to blend.
- **Blend Mode**: Choose a blending technique (see below).

**Output:**
Blended image(s) saved as `output_{mode}.jpg` (e.g., `output_mean.jpg`).

## Blending Techniques
Available modes:

| Mode            | Description                                 | Reference |
|-----------------|---------------------------------------------|-----------|
| all             | Generates all following modes at once.       |           |
| mean            | Average pixel values across frames.          | [Wikipedia](https://en.wikipedia.org/wiki/Image_averaging) |
| add             | Sum pixel values, then normalize to 0-255.   |           |
| multiply        | Multiply pixel values, darker images.        | [Wikipedia](https://en.wikipedia.org/wiki/Blend_modes#Multiply) |
| screen          | Inverse multiply, lighter images.            | [Wikipedia](https://en.wikipedia.org/wiki/Blend_modes#Screen) |
| max             | Maximum value for each pixel.                |           |
| min             | Minimum value for each pixel.                |           |
| median          | Median value for each pixel.                 |           |
| difference      | Average of absolute differences from first.  |           |
| geometric_mean  | Geometric mean of pixel values.              |           |
| stddev          | Standard deviation of pixel values.          |           |
| range           | Range (max-min) of pixel values.             |           |
| parity          | Parity: even/odd sum of pixel values.        |           |

See [Wikipedia: Blend modes](https://en.wikipedia.org/wiki/Blend_modes) for more.

## Notes
- Scripts are interactive and prompt for inputs.
- Frame naming (`frame_{i:04d}.jpg`) is hardcoded. For more than 9999 frames, increase digits (e.g., `frame_{i:05d}.jpg`) in both scripts.
- Blending uses NumPy for efficiency.
- No GPU support.
