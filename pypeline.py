class Pypeline:
    def __init(self, raws=None, flats=None, biases=None, darks=None):
        '''Create a new pypeline object.'''
        pass

    def calibrate(self, raw=None, flat=None, bias=None, dark=None):
        '''Calibrate an image'''

    def register(self, images=None):
        '''Register (align) images'''
        pass

    def stack(self, images=None):
        '''Stack images'''
        pass



if __name__ == '__main__':
    p = Pypeline()

