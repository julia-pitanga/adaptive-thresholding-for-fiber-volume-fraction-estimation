from PIL import Image
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# Settings
INPUT = 'data/raw.png'
OUTPUT = 'output/filtered_image_threshold.png'
ALPHA = 1         # Contrast (>1 = more contrast)
BETA = 1          # Brightness (0 = no change)
BLOCK_SIZE = 451  # Examples: for raw -> 451, for raw2 -> 101
C = -1            # Examples: for raw -> -1, for raw2 -> 10

# Parameters: layer thicknesses
# E0 = 0.16 # Thickness of the fabric raw2.png
E1 = 0.96  # Thickness of the rubber layer (top)
E2 = 0.143 # Thickness of the fabric raw.png
E3 = 0.96  # Thickness of the rubber layer (bottom)
# E4 = 0.16 # Thickness of the fabric raw2.png

# Threshold to identify the fiber
THRESHOLD = 110 # Because the image is already in greyscale, we can use a simple threshold to identify the fiber, any number between 0 and 255 is valid.

# Reading the image
img = cv.imread(INPUT, cv.IMREAD_GRAYSCALE)
assert img is not None, "Error while loading the image"

# Contrast adjustment
img_contrast = cv.convertScaleAbs(img, alpha=ALPHA, beta=BETA)

# Optional median filter (helps with noise)
img_filtered = cv.medianBlur(img_contrast, 5)

# Adaptive threshold
th = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                          cv.THRESH_BINARY, BLOCK_SIZE, C)

# Save the filtered image
cv.imwrite(OUTPUT, th)

# Displaying results
print(f"Image saved as {OUTPUT}")

# Plot: original, contrast, threshold
titles = ['Original Image', 'After Contrast Adjustment', 'Adaptive Threshold']
images = [img, img_contrast, th]

plt.figure(figsize=(12, 4))
for i in range(3):
    plt.subplot(1, 3, i+1)
    plt.imshow(images[i], cmap='gray')
    plt.title(titles[i])
    plt.axis('off')
plt.tight_layout()
plt.show()

# Opening and converting the image
source = Image.open(OUTPUT).convert("L")
source = np.array(source)

# Defining the function to calculate density
def getDensity(source, threshold):
    """
    Calculates the density (volume fraction) of the fiber based on the threshold.
    """
    sourceBinary = np.where(source > threshold, 1, 0)  # White pixels are fiber
    fiberCount = np.sum(sourceBinary)
    totalPixels = sourceBinary.shape[0] * sourceBinary.shape[1]
    return fiberCount / totalPixels  # Returns the density

Vf_fiber = getDensity(source, THRESHOLD)

# Example: calculating the global volume fraction for 3 layers
Vf_global = (Vf_fiber * E2) / (E1 + E2 + E3)  # The lateral dimensions (width and length) are equal in all layers,
# so they cancel out in the calculation of the global volume fraction.

# Displaying results
print(f"Volume fraction of the fibrous layer: {Vf_fiber * 100:.2f}%")
print(f"Global volume fraction: {Vf_global * 100:.2f}%")
