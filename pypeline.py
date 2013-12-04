import math
import sys

from PIL import Image

class Pypeline:
    def __init__(self, raws=None, flats=None, biases=None, darks=None):
        """Create a new pypeline object."""
        pass

    def calibrate(self, raw=None, flat=None, bias=None, dark=None):
        """Calibrate an image"""

    def register(self, images=None):
        """Register (align) images"""
        pass

    def stack(self, images=None):
        """Stack images"""
        inputs = [Image.open(img) for img in images]
        width, height = inputs[0].size
        
        out = Image.new("RGB", (width, height))
        
        for x in range(width):
            for y in range(height):
                pixels = [img.getpixel((x, y)) for img in inputs]
                reds = [pixel[0] for pixel in pixels]
                greens = [pixel[1] for pixel in pixels]
                blues = [pixel[2] for pixel in pixels]
                
                reds.sort()
                greens.sort()
                blues.sort()

                medianred = reds[math.floor(len(reds) / 2)]
                mediangreen = greens[math.floor(len(greens) / 2)]
                medianblue = blues[math.floor(len(blues) / 2)]
                
                out.putpixel((x,y), (medianred, mediangreen, medianblue))
                
        return out


if __name__ == '__main__':
    pype = Pypeline()
    newimg = pype.stack(sys.argv[1:-1])
    newimg.save(sys.argv[-1], "JPEG")
    
