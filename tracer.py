from itertools import chain
from PIL import ImageDraw, Image

try:
    from PIL.Image import BOX
except:
    from PIL.Image.Resampling import BOX


class Tracer:
    def __init__(self, img, compose=True, sc=11):
        self.sc = sc
        self.img = img
        self.compose = compose
        w, h = self.img.size

    def __call__(self, segments):
        w, h = self.img.size
        paint = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(paint)
        self.draw.polygon(list(chain(*segments)), fill=(255, 255, 255, 255))
        if self.compose:
            dst = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            dst.paste(self.img, paint)
            res = dst
        else:
            res = paint
        res.save("out.png")
        return res.resize((self.sc * w, self.sc * h), BOX)
