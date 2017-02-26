#! /usr/bin/python3

import random
from threading import Thread

from PIL import Image

W = 256
H = 382
SZ = H * W
data = bytes
SPECIMENT_CNT = 4
specimens = [0] * SPECIMENT_CNT


class Specimen():
    def __init__(self, name='mona'):
        self.data = [0] * SZ
        self.score = -1
        self.name = name


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
        im = Image.frombytes('P', (W, H), bytes(self.specimen.data))
        im.save('/tmp/mona_sp_' + self.name + '.png')


class ScoreHandler(Thread):
    def __init__(self, specimen):
        super().__init__()
        self.specimen = specimen

    def run(self):
        print('score ' + self.name + ' start')
        _score = 0
        for i in range(SZ):
            a = data[i]
            b = self.specimen.data[i]
            _score += (a - b) ** 2
        self.specimen.score = _score
        print(self.name, self.specimen.name, str(self.specimen.score))
        print('score ' + self.name + ' stop')


def mutate():
    threads = list()
    for specimen in specimens:
        m = MutateHandler(specimen)
        m.start()
        threads.append(m)
    for m in threads:
        m.join()


def score():
    threads = list()
    for i in range(SPECIMENT_CNT):
        s = ScoreHandler(specimens[i])
        s.start()
        threads.append(s)
    for s in threads:
        s.join()


if __name__ == '__main__':
    # with open('mona_small_gray.raw', 'rb') as f:
    #     picture = f.read()

    im = Image.open('mona_small_gray.png')  # type: Image.Image
    data = im.tobytes()
    im.close()
    for i in range(SPECIMENT_CNT):
        specimens[i] = Specimen(str(i))
    random.seed(100)

    for i in range(2):
        mutate()

        score()
