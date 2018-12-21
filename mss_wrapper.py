import time

import cv2
import mss
import numpy

sct = mss.mss()


def screenshot(window):
    return numpy.array(sct.grab(window))
