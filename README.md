# Adaptive Thresholding for Fiber Volume Fraction Estimation

This Python script processes images of composite materials to estimate the **local fiber volume fraction** of a specific layer and calculate the **global volume fraction** in a multi-layered structure.

## Overview

Given an image, the script:
1. Applies contrast and brightness adjustments.
2. Performs adaptive thresholding to isolate the fibrous regions.
3. Calculates the volume fraction of fibers based on pixel density.
4. Computes a global volume fraction for multilayered composites using user-defined layer thicknesses.

## Example Output

The script also generates a side-by-side plot displaying:
- The original image.
- The contrast-adjusted image.
- The thresholded binary image.

## Configuration

All user-defined parameters are declared at the beginning of the script in the **Settings** section. These include:

### Paths
- `INPUT`: Path to the input image.
- `OUTPUT`: Path to save the filtered thresholded image.

### Image Processing
- `ALPHA`: Contrast adjustment (values >1 increase contrast).
- `BETA`: Brightness adjustment.
- `BLOCK_SIZE`: Size of the neighborhood for adaptive thresholding (odd number).
- `C`: Constant subtracted from the mean in adaptive thresholding.

### Layer Thicknesses
To compute the **global fiber volume fraction**, the user must set the thicknesses of the layers:
```python
E1 = 0.96  # Top rubber layer
E2 = 0.143 # Fiber layer
E3 = 0.96  # Bottom rubber layer
```
These values (in mm or consistent units) are case-specific and must be updated by the user.

### Fiber Threshold
- `THRESHOLD`: Pixel intensity threshold to classify white pixels as fibers (range: 0–255). This value may need to be tuned depending on image characteristics.

### Global Volume Fraction Formula
The formula used is:
```python
Vf = (E2 * 100) / (E1 + E2 + E3)
```
You can **modify this expression** in the code to match your multilayer system if needed.

## Installation

Before running the script, install the dependencies:
```bash
pip install -r requirements.txt
```

## Running

Once configured, simply run:
```bash
python main.py
```
The script will:
- Save the thresholded image.
- Display the processed images.
- Print the fiber volume fraction and global volume fraction in the console.

## License

This project is open-source and free to use under the MIT License.
