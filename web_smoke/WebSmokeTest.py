import unittest
import time
import os

from selenium import webdriver
import cv2
from skimage.measure import compare_ssim
import imutils
import numpy as np


class WebSmokeTest(unittest.TestCase):
    EXPECTED_DIR = 'examples/expected'
    ACTUAL_DIR = 'examples/actual'

    def setUp(self):
        if not self.ACTUAL_DIR:
            raise ValueError('ACTUAL_DIR value has to be provided to run tests')
        if not os.path.exists(self.ACTUAL_DIR):
            os.makedirs(self.ACTUAL_DIR)
        self._driver = self._create_driver()
        self._timeout = 5

    def _create_driver(self):
        return webdriver.Chrome()

    def load(self, url):
        self._driver.get(url)

    def wait_for_text(self, text, timeout=None):
        pass

    def wait_for_element_with_id(self, element_id, timeout=None):
        pass

    def wait(self, timeout):
        time.sleep(timeout)

    def assert_image(self, image):
        expected_image = os.path.join(self.EXPECTED_DIR, image + '.png')
        actual_image = os.path.join(self.ACTUAL_DIR, image + '.png')
        self._driver.save_screenshot(actual_image)
        print(actual_image)
        self._compare_image(expected_image, actual_image)

    def _compare_image(self, expected_path, actual_path):
        expected = cv2.imread(expected_path)

        if expected is None:
            self.fail('No expected image available')
            return
        actual = cv2.imread(actual_path)

        # convert the images to grayscale
        grayE = cv2.cvtColor(expected, cv2.COLOR_BGR2GRAY)
        grayA = cv2.cvtColor(actual, cv2.COLOR_BGR2GRAY)

        (score, diff) = compare_ssim(grayE, grayA, full=True)
        diff = (diff * 255).astype("uint8")
        if score == 1.0:
            # images match. test pass
            return
        
        # threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        height, width, _ = actual.shape
        transparent_img = np.zeros((height, width, 4), dtype=np.uint8)
        # loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and then draw the
            # bounding box on a transparent image.
            # This image will be used as overlay to highlight diff on images
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(transparent_img, (x, y), (x + w, y + h), (0, 0, 255, 255), 2)
        cv2.imwrite(actual_path.replace('.png', '-diff.png'), transparent_img)

        self.fail('Expected and actual image do not match. SSIM - {}'.format(score))
