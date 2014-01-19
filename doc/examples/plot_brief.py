"""
=======================
BRIEF binary descriptor
=======================

This example demonstrates the BRIEF binary description algorithm.

The descriptor consists of relatively few bits and can be computed using
a set of intensity difference tests. The short binary descriptor results
in low memory footprint and very efficient matching based on the Hamming
distance metric.

However, BRIEF does not provide rotation-invariance and scale-invariance can be
achieved by detecting and extracting features at different scales.

The ORB feature detection and binary description algorithm is an extension to
the BRIEF method and provides rotation and scale-invariance, see
`skimage.feature.ORB`.

"""
from skimage import data
from skimage import transform as tf
from skimage.feature import (match_descriptors, corner_peaks, corner_harris,
                             plot_matches, BRIEF)
from skimage.color import rgb2gray
import matplotlib.pyplot as plt


img1 = rgb2gray(data.lena())
tform = tf.AffineTransform(scale=(1.2, 1.2), translation=(0, -100))
img2 = tf.warp(img1, tform)
img3 = tf.rotate(img1, 25)

keypoints1 = corner_peaks(corner_harris(img1), min_distance=5)
keypoints2 = corner_peaks(corner_harris(img2), min_distance=5)
keypoints3 = corner_peaks(corner_harris(img3), min_distance=5)

extractor = BRIEF()

extractor.extract(img1, keypoints1)
keypoints1 = keypoints1[extractor.mask_]
descriptors1 = extractor.descriptors_

extractor.extract(img2, keypoints2)
keypoints2 = keypoints2[extractor.mask_]
descriptors2 = extractor.descriptors_

extractor.extract(img3, keypoints3)
keypoints3 = keypoints3[extractor.mask_]
descriptors3 = extractor.descriptors_

matches12 = match_descriptors(descriptors1, descriptors2, cross_check=True)
matches13 = match_descriptors(descriptors1, descriptors3, cross_check=True)

fig, ax = plt.subplots(nrows=2, ncols=1)

plt.gray()

plot_matches(ax[0], img1, img2, keypoints1, keypoints2, matches12)
ax[0].axis('off')

plot_matches(ax[1], img1, img3, keypoints1, keypoints3, matches13)
ax[1].axis('off')

plt.show()
