import math
import os
import subprocess
import sys

import cv2
import numpy

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
        orb = cv2.ORB()
        features = []
        for image in images:
            features.append(orb.detectAndCompute(image, None))
        
        return images # for now no real registration

    def stack(self, images=None):
        """Stack images.  Return one stacked image."""
        rows, cols, channels = images[0].shape
        out = numpy.zeros(images[0].shape)
        
        for row in range(rows):
            for col in range(cols):
                for channel in range(channels):
                    pixels = [image[row][col][channel] for image in images]
                    pixels.sort()
                    out[row][col][channel] = pixels[int(math.floor(len(pixels) / 2))]
        
        return out


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "usage: python pypeline.py <input directory>"
        sys.exit(1)
    
    pype = Pypeline()
    converted = ['marker/DSC_0027.JPG', 'marker/DSC_0028.JPG', 'marker/DSC_0029.JPG', 'marker/DSC_0030.JPG', 'marker/DSC_0031.JPG']#pype.convert(sys.argv[1])
    registered = pype.register(converted)
    stacked = pype.stack(registered)
    cv2.imwrite('output.jpg', stacked)
    
