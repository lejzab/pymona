import random
from PIL import Image

W = 256
H = 382
SZ = H * W
data = bytes
SPECIMENT_CNT = 4
specimen = [0] * SZ
specimens = list()

if __name__ == '__main__':
    with open('mona_small_gray.raw', 'rb') as f:
        picture = f.read()

    im = Image.open('mona_small_gray.png')  # type: Image.Image
    # print(im.mode, im.size)
    data = im.tobytes()
    for i in range(SPECIMENT_CNT):
        specimens.append(specimen)
    random.seed(100)

    for i in range(0, SPECIMENT_CNT):
        x = random.randint(0, W)
        y = random.randint(0, H)
        w = random.randint(x, W) + 1
        h = random.randint(y, H) + 1
        c = random.randint(0, 255)
        for n in range(y, h):
            for m in range(x, w):
                specimens[i][n * W + m] = (specimens[i][n * W + m] + c) >> 1

    for i in range(0, SPECIMENT_CNT):
        im2 = Image.frombytes('P', (W, H), bytes(specimens[i]))
        im2.show()

        # im2.save('mona2.png')
