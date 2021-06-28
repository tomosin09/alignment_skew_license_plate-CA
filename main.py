import argparse
import matplotlib.pyplot as plt
from alignment_skew import alignment
from loguru import logger
import time


def visualize(images, titles):
    l = len(images)
    for i in range(l):
        plt.subplot(1, l, i + 1);
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
    run, image, warped = alignment(args.frame_path)
    if not run:
        logger.error('failed to convert image, try more')
        sys.exit(-1)
    logger.info(f'the number was corrected in {round(time.time()-start,4)}')
    images = [image, warped]
    titles = ['original', 'warped']
    visualize(images, titles)

