import os
from PIL import Image, ImageDraw, ImageFont


class ImageManipulator:
    laser = os.path.abspath(__file__ + "/../data/base/funny/laser.jpeg") # path, size

    @classmethod
    def generate_funny_crypto(cls, text):
        im = Image.open(cls.laser)
        dr = ImageDraw.Draw(im)
        w, h = dr.textsize(text)
        font = ImageFont.truetype(r'C:\Windows\Fonts\Arial.ttf', 20)

        dr.text(((336 - w) / 2, (336 - h) / 2), text, fill="black", align='center', font=font)

        created = os.path.abspath(__file__) + "/../data/base/funny/generated.jpeg"
        im.save(created)

        return created

