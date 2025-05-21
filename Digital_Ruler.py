import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np

# Globals
measure_points = []
pixels_per_unit = 10.0  # Default value; 10 pixels = 1 unit

def apply_edge_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)  # Convert back to 3-channel image

def set_pixels_per_unit(value):
    global pixels_per_unit
    try:
        pixels_per_unit = float(value)
        print(f"[✓] Pixels per unit set to: {pixels_per_unit}")
    except ValueError:
        print("[!] Invalid input for pixels per unit.")

def select_image():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if path:
        measure_image(path)

def measure_image(image_path):
    global measure_points, pixels_per_unit
    measure_points = []

    image = cv2.imread(image_path)
    if edge_detection_enabled.get() == 1:
        image = apply_edge_detection(image)

    image_display = image.copy()

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(measure_points) == 2:
                measure_points.clear()
                image_display[:] = image.copy()  # Reset image

            measure_points.append((x, y))
            cv2.circle(image_display, (x, y), 5, (0, 255, 0), -1)
            cv2.putText(image_display, f"P{len(measure_points)}", (x + 10, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            if len(measure_points) == 2:
                cv2.line(image_display, measure_points[0], measure_points[1], (0, 255, 0), 2)
                px_dist = np.linalg.norm(np.array(measure_points[0]) - np.array(measure_points[1]))
                real_dist = px_dist / pixels_per_unit
                midpoint = tuple(np.mean([measure_points[0], measure_points[1]], axis=0).astype(int))
                label = f"{real_dist:.2f} units"
                cv2.putText(image_display, label, midpoint,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                print(f"[📏] Measured: {real_dist:.2f} units")

            cv2.imshow("Digital Ruler", image_display)

    cv2.imshow("Digital Ruler", image_display)
    cv2.setMouseCallback("Digital Ruler", click_event)
    print("🖱️ Click two points to measure. Uses the set scale.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# ==== GUI ====
root = tk.Tk()
root.title("Digital Ruler")
root.geometry("320x270")

# Now it's safe to define IntVar
edge_detection_enabled = tk.IntVar(value=0)

# Scale input
tk.Label(root, text="Pixels per unit (e.g., 48 = px per cm):", font=("Arial", 11)).pack()
scale_entry = tk.Entry(root, font=("Arial", 12))
scale_entry.insert(0, "48.0")
scale_entry.pack(pady=5)

# Set scale button
set_btn = tk.Button(root, text="Set Scale", font=("Arial", 11),
                    command=lambda: set_pixels_per_unit(scale_entry.get()))
set_btn.pack(pady=5)

# Edge detection toggle
tk.Label(root, text="Apply Edge Detection:", font=("Arial", 11)).pack()
tk.Radiobutton(root, text="Off", variable=edge_detection_enabled, value=0, font=("Arial", 10)).pack()
tk.Radiobutton(root, text="On", variable=edge_detection_enabled, value=1, font=("Arial", 10)).pack()

# Image selection button
load_btn = tk.Button(root, text="📂 Select Image", font=("Arial", 14), command=select_image)
load_btn.pack(pady=10)

root.mainloop()
