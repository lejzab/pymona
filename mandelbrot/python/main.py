import datetime
import time
import logging
import concurrent.futures
from dataclasses import dataclass

import numpy as np
from PIL import Image

IMG_WIDTH = 1000
# IMG_HEIGHT = 5
MIN_X_VAL = -2.0
MAX_X_VAL = 0.6
MIN_Y_VAL = -1.3
MAX_Y_VAL = 1.3
MAX_ITER = 150
STEP = IMG_WIDTH // 4


@dataclass
class Point:
    x: int
    y: int

    def dx(self, target) -> int:
        return abs(self.x - target.x)

    def dy(self, target) -> int:
        return abs(self.y - target.y)


@dataclass
class Crop:
    start_point: Point
    stop_point: Point


def mandelbrot_point(vx, vy):
    z = 0
    c = complex(vx, vy)
    for i in range(MAX_ITER):
        if abs(z) > 2:
            return i
        z = z ** 2 + c
    return 0


def mandel(start_point: Point, stop_point: Point, x_step, y_step):
    start = time.time()
    logging.info(f'start calculating {start_point=} {stop_point=}')
    dx = start_point.dx(stop_point)
    dy = start_point.dy(stop_point)
    points = np.zeros((dx, dy), dtype=int)

    yp = MIN_Y_VAL + start_point.y * y_step
    for y in range(dy):
        xp = MIN_X_VAL + start_point.x * x_step
        for x in range(dx):
            p = mandelbrot_point(xp, yp)
            points[x][y] = p
            logging.debug(f'mandelbrot point[{x}][{y}]={p}. {xp=} {yp=}')
            xp += x_step
        yp += y_step
    logging.info(f'stop calculating {start_point=} {stop_point=}. elapsed {time.time() - start}')
    return start_point, stop_point, points


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info('main mandel start')
    ratio = abs(MIN_Y_VAL - MAX_Y_VAL) / abs(MIN_X_VAL - MAX_X_VAL)
    img_height = int(IMG_WIDTH * ratio)
    x_step = (MAX_X_VAL - MIN_X_VAL) / IMG_WIDTH

    y_step = (MAX_Y_VAL - MIN_Y_VAL) / img_height
    img = Image.new('RGB', (IMG_WIDTH, img_height))
    logging.info('start calculations')
    with concurrent.futures.ProcessPoolExecutor() as executor:
        data = []
        completed_futures = []
        for i in range(0, IMG_WIDTH, STEP):
            for j in range(0, img_height, STEP):
                start_point = Point(i, j)
                stop_point = Point(i + STEP, j + STEP)
                if i + STEP > IMG_WIDTH:
                    stop_point.x = IMG_WIDTH
                if j + STEP > img_height:
                    stop_point.y = img_height

                completed_futures.append(executor.submit(mandel,
                                                         start_point,
                                                         stop_point,
                                                         x_step,
                                                         y_step)
                                         )
        for future in concurrent.futures.as_completed(completed_futures):
            data.append(future.result())
    logging.info('stop calculations')

    for start_point, stop_point, points in data:
        for x in range(start_point.x, stop_point.x):
            for y in range(start_point.y, stop_point.y):
                # logging.debug(f'{x=} {y=}')
                p = points[x - start_point.x][y - start_point.y]
                color = (p, 8 * p, 12 * p)
                img.putpixel((x, y), color)

    img.save(f'../pictures/mandelbrot_{datetime.datetime.now()}.png')
    logging.info('main mandel stop')


if __name__ == '__main__':
    main()
