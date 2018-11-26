# import os
# from selenium import webdriver

# PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# DRIVER_BIN = os.path.join(PROJECT_ROOT, "bin/chromedriver_for_mac")
# browser = webdriver.Chrome(executable_path=DRIVER_BIN)
# browser.get('http://www.baidu.com/')

import webbrowser

import pytesseract
from PIL import Image
# import pyscreenshot as ImageGrab
import screenshot
import time
import re
import sys

import applescript
from AppKit import NSWorkspace
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID
)

import itertools
import rumps


def getActiveInfo():
    app = NSWorkspace.sharedWorkspace().frontmostApplication()
    active_app_name = app.localizedName()

    options = kCGWindowListOptionOnScreenOnly
    windowList = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
    windowTitle = 'Unknown'
    for window in windowList:
        windowNumber = window['kCGWindowNumber']
        ownerName = window['kCGWindowOwnerName']
        geometry = window['kCGWindowBounds']
        windowTitle = window.get('kCGWindowName', u'Unknown')
        if windowTitle and ownerName == active_app_name:
            return windowNumber, ownerName, geometry, windowTitle
    return None


def findErrors(text):
    res = []
    for match in re.finditer('Traceback', text):
        surrounding_text = text[match.start():match.end() + 1000]
        print('"""' + surrounding_text + '"""')
        important_line = surrounding_text.split('\n')[3]
        res.append(important_line)
    return res


def values_to_ints(d): return dict((k, int(v)) for k, v in d.items())


def getError():
    windowNumber, ownerName, geometry, windowTitle = getActiveInfo()
    geometry = values_to_ints(geometry)
    print(windowTitle)
    print('Screenshoting...')
    rect = geometry['X'], geometry['Y'], geometry['Width'], geometry['Height']
    print(rect)
    im = screenshot.screenshot(rect)
    # im.show()
    print('OCRing...')
    text = pytesseract.image_to_string(im)
    print('Finding errors...')
    errors = findErrors(text)
    print(errors)
    for error in errors:
        print(error)
    return errors


progress_char = itertools.cycle(['/', '-', '\\', '|'])

app = rumps.App('Yassist')

search_string = ''


@rumps.clicked('Investigate')
def investigate(_):
    url = f"https://www.google.com.tr/search?q={search_string}"
    # print(f'>>>{url}<<<')
    webbrowser.open_new_tab(url)


@rumps.timer(1)
def updateName(sender):
    print('update!')
    errs = getError()
    if errs:
        global search_string
        search_string = errs[0]
        app.title = f'Traceback "{search_string}" {next(progress_char)}'
    else:
        app.title = f'Yassist Scanning {next(progress_char)}'


timer = rumps.Timer(updateName, 1)
app.run()


# print(text)


# import cv2
# import sys
# import pytesseract
#
# if __name__ == '__main__':
#
#     if len(sys.argv) < 2:
#         print('Usage: python ocr_simple.py image.jpg')
#         sys.exit(1)
#
#     # Read image path from command line
#     imPath = sys.argv[1]
#
#     # Define config parameters.
#     # '-l eng'  for using the English language
#     # '--oem 1' for using LSTM OCR Engine
#     config = ('-l eng --oem 1 --psm 3')
#
#     # Read image from disk
#     im = cv2.imread(imPath, cv2.IMREAD_COLOR)
#
#     # Run tesseract OCR on image
#     text = pytesseract.image_to_string(im, config=config)
#
#     # Print recognized text
#     print(text)
