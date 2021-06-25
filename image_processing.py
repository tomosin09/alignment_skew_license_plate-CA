import cv2
import numpy as np


class ImageConversion():

    @staticmethod
    def changeBC(frame, alpha=1, beta=0):
        new_image = np.zeros(frame.shape, frame.dtype)
        # Initialize values
        return cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    @staticmethod
    def gammaCorrection(frame, gamma=1):
        lookUpTable = np.empty((1, 256), np.uint8)
        for i in range(256):
            lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
        return cv2.LUT(frame, lookUpTable)

    @staticmethod
    def convToThresh(frame):
        blur = cv2.GaussianBlur(frame, (3, 3), cv2.BORDER_DEFAULT)
        emission_value = np.nanmean(blur) + np.nanstd(blur)
        return cv2.threshold(blur, emission_value, 255, cv2.THRESH_BINARY)[1]

    @staticmethod
    def confToSobel(frame):
        x = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=3, scale=1)
        y = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=3, scale=1)
        absx = cv2.convertScaleAbs(x)
        absy = cv2.convertScaleAbs(y)
        return cv2.addWeighted(absx, 0.5, absy, 0.5, 0)

    @staticmethod
    def getOutlines(frame):
        contours = cv2.findContours(frame.copy(), cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else 1
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        return contours
