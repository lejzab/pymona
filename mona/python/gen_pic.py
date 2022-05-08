#! /usr/bin/python3

import random
from threading import Thread
import copy

import datetime
from PIL import Image

W = 256
H = 382
SZ = H * W
data = bytes
SPECIMENT_CNT = 300
BEST_CNT = 3
specimens = [0] * SPECIMENT_CNT


class Specimen:
    def __init__(self, name='mona'):
        self.data = [0] * SZ
        self.score = -1
        self.name = name

    def __str__(self):
        return self.name + ' ' + str(self.score)

    def __repr__(self):
        return repr((self.name, self.score))


class MutateHandler(Thread):
    def __init__(self, specimen):
        super().__init__()
        self.specimen = specimen

    def run(self):
        x = random.randint(0, W)
        y = random.randint(0, H)
        w = random.randint(0, W - x)
        h = random.randint(0, H - y)
        c = random.randint(0, 255)
        for n in range(y, h + y):
            for m in range(x, w + x):
                self.specimen.data[n * W + m] = (self.specimen.data[n * W + m] + c) >> 1
                # im = Image.frombytes('P', (W, H), bytes(self.specimen.data))
                # im.save('/tmp/mona_sp_' + self.name + '.png')


class ScoreHandler(Thread):
    def __init__(self, specimen):
        super().__init__()
        self.specimen = specimen

    def run(self):
        # print('score ' + self.name + ' start')
        _score = 0
        for i in range(SZ):
            a = data[i]
            b = self.specimen.data[i]
            _score += (a - b) ** 2
        self.specimen.score = _score
        # print(self.name, self.specimen)
        # print('score ' + self.name + ' stop')


def mutate():
    threads = list()
    for specimen in specimens:
        thread = MutateHandler(specimen)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()


def score():
    threads = list()
    for specimen in specimens:
        thread = ScoreHandler(specimen)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    return sorted(specimens, key=lambda spec: spec.score)


def cross():
    new_specimens = [0] * SPECIMENT_CNT
    for i in range(len(specimens)):
        new_specimens[i] = copy.deepcopy(specimens[i % BEST_CNT])
    return new_specimens


def dump_best(step):
    best = specimens[0]
    im = Image.frombytes('P', (W, H), bytes(best.data))
    im.save('/tmp/mona_best_{:0>5}.png'.format(step))


if __name__ == '__main__':
    # with open('mona_small_gray.raw', 'rb') as f:
    #     picture = f.read()

    im = Image.open('mona_small_gray.png')  # type: Image.Image
    data = im.tobytes()
    im.close()
    for i in range(SPECIMENT_CNT):
        specimens[i] = Specimen('mona_' + str(i))
    random.seed(100)

    for i in range(25):
        print('{0:%Y-%m-%d %H:%M:%S} step {1:d} started'.format(datetime.datetime.now(), i))
        mutate()
        print('{0:%Y-%m-%d %H:%M:%S} step {1:d} mutate done'.format(datetime.datetime.now(), i))
        specimens = score()
        print('{0:%Y-%m-%d %H:%M:%S} step {1:d} score done'.format(datetime.datetime.now(), i))
        # print('plain', specimens)
        specimens = cross()
        print('{0:%Y-%m-%d %H:%M:%S} step {1:d} cross done'.format(datetime.datetime.now(), i))
        print('crossed', specimens[:BEST_CNT])
        dump_best(i)
