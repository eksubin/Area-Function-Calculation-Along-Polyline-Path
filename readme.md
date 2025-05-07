# Area Function Calculation Along Polyline Path for 3D segmentation

This Python script allows users to **draw a polyline path** on a 2D mid-sagittal segmentation image (in `.png` format) and computes the **area function** along the path using **perpendicular cuts** at each point along the polyline. Then this process is repeated for all the slices in the 3D volume. The function then visualizes the results by plotting:

- The **input image** with the drawn polyline and perpendicular cuts.
- The **area function** along the polyline path, both in raw and smoothed forms as an average for all the slices.

## How It Works:

1. **Slice Volume**: Slice the 3D segmentatioin using the `NrrdSlicer.py` code and save it into the `ImageSlices` folder
2. **Move file**: Copy and paste the mid-sagittal slice outside this folder
3. **Load Image**: The script loads a mid-sagittal segmentation image in `.png` format and converts it into a binary mask.
4. **Draw Polyline Path**: The user clicks on the image to define a polyline path. A **minimum of 5 points** is required to define the path.
5. **Compute Area Function**: For each point on the polyline, the script calculates the area along perpendicular cuts at each segment in all the 3D slices.
6. **Smooth Area Function**: A **Savitzky–Golay filter** is applied to smooth the raw area function.
7. **Visualization**: The script shows:
   - The **input image** with the polyline and the perpendicular cuts.
   - The **raw and smoothed area functions** plotted against the distance along the polyline path.

Here's a quick demo of how the script works:

![Area Function Demo](./animation.gif)

## Usage:

1. **Run the Script**: Execute the Python script in your preferred environment (such as Jupyter Notebook or a Python IDE).

2. **Provide Input**: When prompted, select your segmentation image (e.g., `slice_036.png` which is the mid-sagittal slice).

3. **Draw the Polyline**: Click on the image to define the path. You must click **at least 5 points** to create the polyline. Right-click or press **Enter** to finish.

4. **Results**: The script will:
   - Display the image with the polyline and perpendicular cuts.
   - Plot the **raw and smoothed area function** along the path.

## Requirements:

- Python 3.x
- Required libraries:
  - `numpy`
  - `matplotlib`
  - `scipy`
  - `PIL` (Pillow)

You can install the necessary dependencies with `pip`:

```bash
pip install numpy matplotlib scipy pillow
```
