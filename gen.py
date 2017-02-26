from PIL import Image



if __name__ == '__main__':

    with open('mona_small_gray.raw', 'rb') as f:
        picture = f.read()

    im = Image.open('mona_small_gray.png') #type: Image.Image
    data = im.getdata()
    print(len(data))
