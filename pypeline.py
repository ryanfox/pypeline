import math
import os
import subprocess
import sys

import cv
import cv2
import numpy as np

class Pypeline:
    def __init__(self, raws=None, flats=None, biases=None, darks=None):
        """Create a new pypeline object."""
        pass
    
    def convert(self, directory=None):
        """Convert a list of raw files to tiff, using dcraw.  Return a list
        of converted filenames."""
        converted = set()
        for filename in os.listdir(directory):
            inputpath = os.path.join(directory, filename)
            outputpath = os.path.splitext(inputpath)[0] + '.tiff'
            if not os.path.isfile(outputpath):
                command = ['./dcraw', '-W', '-T', '-6', inputpath]
                subprocess.call(command)
            converted.add(outputpath)
        return converted

    def calibrate(self, raw=None, flat=None, bias=None, dark=None):
        """Calibrate an image"""

    def register(self, filenames=None):
        """Register (align) images.  Return a list of aligned images."""
        images = [cv2.imread(image) for image in filenames]
        height, width = images[0].shape[:2]
        orb = cv2.ORB()
        features = []
        for image in images:
            features.append(orb.detectAndCompute(image, None))
        
        # magic numbers taken from
        # https://github.com/Itseez/opencv/blob/master/samples/python2/find_obj.py
        flannparams = {'algorithm': 6,
                       'table_number': 6,
                       'key_size': 12,
                       'multi_probe_level': 1}
        flann = cv2.FlannBasedMatcher(flannparams, {})
        
        warped = [images[0]]
        for i in range(len(images) - 1):
            keypoints1 = features[0][0]
            descriptors1 = features[0][1]
            keypoints2 = features[i+1][0]
            descriptors2 = features[i+1][1]
            matches = flann.knnMatch(descriptors1, descriptors2, k=2)
            
            goodmatches = []
            for pair in matches:
                if len(pair) == 2:
                    if pair[0].distance < 0.7 * pair[1].distance:
                        goodmatches.append(pair[0])
            
            sourcepoints = np.float32([keypoints1[m.queryIdx].pt for m in goodmatches])
            destpoints = np.float32([keypoints2[m.trainIdx].pt for m in goodmatches])
            
            h, mask = cv2.findHomography(destpoints, sourcepoints, cv2.RANSAC, 5)
            warpedimage = cv2.warpPerspective(images[i+1], h, (width, height))
            
            warped.append(warpedimage)
        return warped

    def stack(self, images=None):
        """Stack images.  Return one stacked image."""
        rows, cols, channels = images[0].shape
        stacked = np.zeros(images[0].shape)
        
        for row in range(rows):
            for col in range(cols):
                for channel in range(channels):
                    pixels = [image[row][col][channel] for image in images]
                    pixels.sort()
                    stacked[row][col][channel] = pixels[int(math.floor(len(pixels) / 2))]
        
        return stacked


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "usage: python pypeline.py <input directory>"
        sys.exit(1)
    
    pype = Pypeline()
    converted = pype.convert(sys.argv[1])
    registered = pype.register(converted)
    stacked = pype.stack(registered)
    
    cv2.imwrite('output.jpg', stacked)
    
