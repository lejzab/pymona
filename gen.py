import random
from threading import Thread

from PIL import Image

W = 256
H = 382
SZ = H * W
data = bytes
SPECIMENT_CNT = 40
specimen = [0] * SPECIMENT_CNT


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
                self.specimen[n * W + m] = (self.specimen[n * W + m] + c) >> 1
        print(self.name)

def mutate():
    threads = list()

    for i in range(0, SPECIMENT_CNT):
        m = MutateHandler(specimen[i])
        m.start()
        threads.append(m)

    for m in threads:
        m.join()

if __name__ == '__main__':
    # with open('mona_small_gray.raw', 'rb') as f:
    #     picture = f.read()

    im = Image.open('mona_small_gray.png')  # type: Image.Image
    data = im.tobytes()
    im.close()
    for i in range(SPECIMENT_CNT):
        specimen[i] = [0] * SZ
    random.seed(100)

    mutate()



