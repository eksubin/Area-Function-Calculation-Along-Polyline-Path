import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import map_coordinates
from PIL import Image
from scipy.interpolate import splprep, splev
from scipy.signal import savgol_filter
import os

def load_image_as_mask(image_path, threshold=50):
    image = Image.open(image_path).convert("L")
    mask = np.array(image)
    binary_mask = (mask > threshold).astype(np.uint8)
    return binary_mask

def get_polyline_from_user(mask):
    """
    Prompt user to draw a polyline by clicking multiple points.
    Right-click or press enter to finish.
    """
    fig, ax = plt.subplots()
    ax.imshow(mask, cmap='gray')
    ax.set_title("Draw polyline path by clicking (right-click or enter to finish)")

    points = plt.ginput(n=-1, timeout=0)
    plt.close()

    if len(points) < 5:
        raise ValueError("Please click at least 5 points to define the path.")

    points = np.array(points).T  # shape (2, N)
    # Interpolate smooth curve
    tck, u = splprep(points, s=0)
    unew = np.linspace(0, 1, 200)
    x_smooth, y_smooth = splev(unew, tck)

    path = np.vstack((x_smooth, y_smooth)).T
    return path

def compute_area_function_along_path(mask, path, cut_length=100):
    """
    Compute area function along path with perpendicular cuts.
    """
    areas = []
    distances = [0]

    for i in range(1, len(path) - 1):
        p_prev = path[i - 1]
        p_next = path[i + 1]
        direction = p_next - p_prev
        norm = np.linalg.norm(direction)
        if norm == 0:
            areas.append(0)
            continue
        direction /= norm
        ortho = np.array([-direction[1], direction[0]])
        center = path[i]

        s_vals = np.linspace(-cut_length / 2, cut_length / 2, 1000)
        coords = center[:, None] + s_vals * ortho[:, None]
        coords_yx = np.vstack((coords[1], coords[0]))  # rows, cols

        values = map_coordinates(mask.astype(float), coords_yx, order=1, mode='constant', cval=0)
        area = np.trapz(values, dx=(cut_length / 1000)) * (0.93** 2)
        areas.append(area)

        distances.append(distances[-1] + np.linalg.norm(path[i] - path[i - 1]))

    return np.array(distances[1:]), np.array(areas)


def plot_results(mask, path, distances, areas, cut_length=100):
    areas_smooth = savgol_filter(areas, window_length=21, polyorder=3)

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # === Left: Mask with polyline and perpendicular cuts ===
    axs[0].imshow(mask, cmap='gray')
    axs[0].plot(path[:, 0], path[:, 1], 'r-', linewidth=2, label="Polyline Path")

    # Draw perpendicular cuts every N steps
    step = max(1, len(path) // 50)
    for i in range(1, len(path) - 1, step):
        p_prev = path[i - 1]
        p_next = path[i + 1]
        direction = p_next - p_prev
        norm = np.linalg.norm(direction)
        if norm == 0:
            continue
        direction /= norm
        ortho = np.array([-direction[1], direction[0]])
        center = path[i]

        p1 = center + (cut_length / 2) * ortho
        p2 = center - (cut_length / 2) * ortho
        axs[0].plot([p1[0], p2[0]], [p1[1], p2[1]], 'g-', alpha=0.6)

    axs[0].set_title("Mask with Polyline Path and Perpendicular Cuts")
    axs[0].axis('off')
    axs[0].legend()

    # === Right: Area function plot ===
    axs[1].plot(distances, areas, alpha=0.4, label='Raw Area', linestyle='--')
    axs[1].plot(distances, areas_smooth, label='Smoothed Area', linewidth=2)
    axs[1].set_title("Area Function Along Path")
    axs[1].set_xlabel("Distance Along Path (pixels)")
    axs[1].set_ylabel("Cross-sectional Area")
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    image_path = "slice_036.png"  # Replace with your PNG
    maskT = load_image_as_mask(image_path)
    path = get_polyline_from_user(maskT)

    # Configuration
    folder_path = "./ImageSlices"  # <-- Set to your folder with PNG images
    window_length = 21
    polyorder = 3

    all_areas = []
    all_distances = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            print(f"Processing {filename}...")

            mask = load_image_as_mask(image_path)
            #path = get_polyline_from_user(mask)  # If path is the same across images, you can define it outside the loop

            distances, areas = compute_area_function_along_path(mask, path)
            areas_smooth = savgol_filter(areas, window_length=window_length, polyorder=polyorder)

            all_distances.append(distances)
            all_areas.append(areas_smooth)

    # Align arrays (in case they vary slightly in length)
    min_length = min(len(d) for d in all_distances)
    all_distances = np.array([d[:min_length] for d in all_distances])
    all_areas = np.array([a[:min_length] for a in all_areas])

    # Compute averages
    avg_distances = np.mean(all_distances, axis=0)
    avg_areas = np.mean(all_areas, axis=0)

    # Plot average result
    plt.figure(figsize=(10, 5))
    plt.plot(avg_distances, avg_areas, label='Average Area Function', color='blue')
    plt.xlabel("Distance along path")
    plt.ylabel("Smoothed Cross-sectional Area")
    plt.title("Average Area Function Across All Images")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # distances, areas = compute_area_function_along_path(mask, path)

    # # Smooth the area function
    # areas_smooth = savgol_filter(areas, window_length=21, polyorder=3)

    # # Plot
    # plot_results(mask, path, distances, areas_smooth)

