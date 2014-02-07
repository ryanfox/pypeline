pypeline
========

pypeline - an astronomical data pipeline in python

The goal of this package is to provide a cross-platform (python), open (github)
pipeline for astronomical image processing.  The bulk of the action is in
pypeline.py. More to come later.

Currently my source of images is a Nikon D5200.  The NEFs (RAW files) created
are converted to tiffs using dcraw and then analyzed using opencv.  This
package should be compatible with every image format supported by dcraw, which
is over 500 different cameras as of the time of this writing.

Many thanks to Dave Coffin's dcraw for raw image conversion.  That project
can be found at http://www.cybercom.net/~dcoffin/dcraw/

Change log
==========

    -v0.0.1
        image stacking added
