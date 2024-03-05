# Image-Forgery-Detection-Using-Signal-and-Image-Pocessing-Techniques

## Overview

This project targets detecting image forgeries caused by internal copying within images while maintaining resilience against compression like JPEG. Employing 8x8 or 16x16 block segmentation aids in localized forgery detection. Utilizing Discrete Cosine Transform (DCT) and zigzag scanning, low-frequency information is extracted for compression-resistant meaningful data retention. Vector representation of DCT outputs, focusing on the initial 16 elements, undergoes quantization for compression resilience. Euclidean distance assessment with a 3.5 threshold against 8 neighboring vectors is employed, followed by a distance filter of at least 100 pixels between block coordinates, ensuring accurate detection, especially in images with analogous regions.

## Methodology

1. **RGB to Grayscale Conversion:**
   - Utilize the rgb2gray function to convert the color image to grayscale.
   - Facilitates simplified processing by reducing the image to a single intensity channel.
   - Preserves essential image information while simplifying subsequent analysis.

2. **Discrete Cosine Transform (DCT):**
   - The Discrete Cosine Transform (DCT) is a mathematical transform commonly used in image compression.
   - DCT converts the spatial representation of the block (pixel intensities) into its frequency representation (DCT coefficients).
   - In the copy-move forgery detection, DCT is applied to the image blocks after conversion of image blocks.

3. **Zigzag Algorithm:**
   - After quantization, the coefficients are arranged in a two-dimensional array.
   - The Zigzag algorithm is applied to this array to convert it into a one-dimensional array.
   - The zigzag pattern helps to gather the most significant coefficients first, making it more efficient storage.

4. **Significant Part Extraction:**
   - Extracts the significant part of a vector by deleting high significant values.
   - A block size of the vector value will be given, and higher frequency values will be deleted.
   - For example, a 1x64 vector is changed to a 1x16 vector by deleting high-frequency components.

5. **Lexicographically Sorting:**
   - Convert the column-vector to a row-vector in a counterclockwise direction (anti-clockwise).
   - Use the lexisort function to convert the column to a row vector in such a way that the last element in the column becomes the 1st element in the row.

6. **Correlation of Vectors:**
   - Check if the Euclidean distance between the vectors is less than the Euclidean threshold.
   - Append the similar vectors to a separate empty array.
   - Actual processing of similar vectors is further handled in the elimination_of_weak_vectors method.

7. **Elimination of Weak Vectors:**
   - Check if the Euclidean distance is greater than the vector threshold value.
   - If it satisfies the condition, call the elimination_of_weak_area function.

8. **Elimination of Weak Area:**
   - Find the displacement and direction of the vectors.
   - Create a new vector to avoid losing information about which block vectors increase in which direction.
   - Calculate the directions of the determined vectors and increase the position of this direction in Hough space.
   - Keep its own coordinates in the vector, and assign block-by-block shift in these vectors to the vector, i.e., shift_vectors.

9. **Detection of Forgery:**
   - Find the Max Hough space value to determine the threshold value.
   - Set the img array by setting all pixel values to 0.
   - Calculate the threshold value using a formula.
   - Fill rectangles in the coordinates in the Hough space corresponding to a shift vector.
   - Output image with white blocks, which represent the forged part of the original image.

## Dependencies

- Python 3.x
- OpenCV
- numpy
- scikit-image

## Usage

1. Clone the repository:
    https://github.com/Blackmonarch4574/Image-Forgery-Detection-Using-Signal-and-Image-Pocessing-Techniques-.git
