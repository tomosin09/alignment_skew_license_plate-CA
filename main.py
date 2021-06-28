import argparse
import os

import matplotlib.pyplot as plt
from alignment_skew import alignment
from loguru import logger
import time
import sys


def visualize(images, titles):
    column = len(images)
    row = 1
    if len(images) > 3:
        column = 3
        row = column % 3
    for i in range(len(images)):
        plt.subplot(row, column, i + 1);
        plt.imshow(images[i])
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='alignment of license plate skew using contour analysis')
    parser.add_argument('--frame_path',
                        help='enter frame path')
    args = parser.parse_args()
    start = time.time()
    run, image, thresh, warped = alignment(args.frame_path)
    if not run:
        logger.error('failed to convert image, try more')
        sys.exit(-1)
    logger.info(f'the number was corrected in {round(time.time() - start, 4)}')
    images = [image, thresh, warped]
    titles = ['original', 'thresh', 'warped']
    visualize(images, titles)



