import sys
import cv2 as cv
import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt


# Helper function to help display an oversized image
def display_image(image, name):
    small_image = cv.resize(image, (0, 0), fx=0.85, fy=0.85)
    cv.imshow(name, small_image)
    cv.waitKey(0)
    cv.destroyAllWindows()


# Helper function to sharpen the image
def sharpen(img):
    kernel = np.array([[0, -1, 0],
                       [-1, 5.5, -1],
                       [0, -1, 0]], np.float32)
    img = cv.filter2D(img, -1, kernel)
    return img


# Helper function to increase contrast of an image
def increase_contrast(img):
    lab_img = cv.cvtColor(img, cv.COLOR_RGB2LAB)
    l, a, b = cv.split(lab_img)
    clahe = cv.createCLAHE(clipLimit=4, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    img = cv.merge((cl, a, b))
    img = cv.cvtColor(img, cv.COLOR_LAB2RGB)
    return img

image_name = 'images/test.jpg'  # select image
image = cv.imread(image_name)  # read the image

# sanity check
if image is None:
    print('Cannot open image: ' + image_name)
    sys.exit(0)
display_image(image, 'Original Image')

# grayscale check
if len(image.shape) != 2:
    gray_image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

# blur the image to get rid of noise
blurred_image = cv.GaussianBlur(gray_image, (3, 3), 0)
blurred_image = cv.medianBlur(blurred_image, 3)

# apply adaptive threshold to transform to a binary image
binary_image = cv.adaptiveThreshold(blurred_image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 101, 50)

# further noise removal
# kernel = np.ones((2, 2), np.uint8)
# denoised_image = cv.morphologyEx(binary_image, cv.MORPH_OPEN, kernel, iterations=2)
display_image(binary_image, 'Processed Image')

cv.imwrite('result_image.png', binary_image)