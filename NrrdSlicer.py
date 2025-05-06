import os
import argparse
import nrrd
import numpy as np
from PIL import Image

def slice_nrrd_to_png(nrrd_file_path, output_folder):
    # Read the NRRD file
    data, header = nrrd.read(nrrd_file_path)

    # Check dimensions
    if data.ndim != 3:
        raise ValueError(f"Expected a 3D NRRD file, got shape {data.shape}")

    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through slices along the 3rd axis
    for i in range(data.shape[2]):
        slice_img = data[:, :, i].astype(np.float32)

        # Normalize to 0-255
        slice_img -= slice_img.min()
        if slice_img.max() > 0:
            slice_img = slice_img / slice_img.max()
        slice_img = (slice_img * 255).astype(np.uint8)

        # Save as PNG
        img = Image.fromarray(slice_img)
        img.save(os.path.join(output_folder, f"slice_{i:03d}.png"))

    print(f"✅ Saved {data.shape[2]} slices to: {output_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Slice a 3D NRRD file into individual PNG images.")
    parser.add_argument("input_nrrd", help="Path to the input .nrrd file")
    parser.add_argument("output_folder", help="Directory where output PNGs will be saved")
    args = parser.parse_args()

    slice_nrrd_to_png(args.input_nrrd, args.output_folder)
