import cv2
import numpy as np
from transform_points import PointConversion
from image_processing import ImageConversion


def alignment(image_path):
    run = True
    checkRect = True
    image = cv2.imread(image_path)
    if image is None:
        print('Image is empty')
        run = False
    gamma = ImageConversion.gammaCorrection(image, 1.3)
    gray_frame = cv2.cvtColor(gamma, cv2.COLOR_BGR2GRAY)
    thresh = ImageConversion.convToThresh(gray_frame)
    sobel = ImageConversion.confToSobel(thresh)
    contours = ImageConversion.getOutlines(sobel)
    approx_list = []
    if checkRect:
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                for i in approx:
                    approx_list.append(i)

    if approx_list == []:
        checkRect = False

    if checkRect is False:
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            for i in approx:
                approx_list.append(i)

    if approx_list == []:
        run = False

    if run:
        approx_math = np.zeros((len(approx_list), 2))
        for i in range(len(approx_list)):
            approx_math[i] = approx_list[i]
        warped = PointConversion.fourPointAlignment(image, approx_math)
        # warped = ImageConversion.changeBC(warped, alpha=1.3, beta=40)
        # warped = ImageConversion.gammaCorrection(warped, 1.3)

    if not run:
        warped = np.zeros((100, 50))

    return run, image, warped
