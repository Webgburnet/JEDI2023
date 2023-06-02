from PIL import ImageDraw, Image

try:
    from PIL.Image import BOX
except:
    from PIL.Image.Resampling import BOX


class decorator:
    alpha = 160
    cols = (255, 0, 255, alpha)
    colf = (0, 255, 255, alpha)
    colp = (255, 255, 0, alpha)
    colpath = (0, 255, 0, alpha)
    collast = (255, 0, 0, alpha)
    colnode = (255, 0, 0, alpha)
    pathw = 5
    rb = 3
    lw = 1
    sc = 11

    def __init__(self, img, compose=True, sc=11):
        self.sc = sc
        self.pathw = sc // 2
        self.lw = max(1, sc // 8)
        self.rb = (sc - sc // 2) // 2
        self.img = img
        w, h = self.img.size
        self.img = self.img.resize((self.sc * w, self.sc * h), BOX)
        self.rc = self.sc // 2
        self.br = self.sc - self.rb - 1
        self.compose = compose

    def pastille(self, x, y, col):
        self.draw.rectangle(
            [
                (self.sc * x + self.rb, self.sc * y + self.rb),
                (self.sc * x + self.br, self.sc * y + self.br),
            ],
            col,
        )

    def point(self, x, y):
        return (self.sc * x + self.rc, self.sc * y + self.rc)

    def lien(self, x, y, xx, yy, col):
        self.draw.line(
            [self.point(x, y), self.point(xx, yy)],
            col,
            self.lw,
        )

    def dopred(self, p, s):
        for u in list(p):
            v = p[u]
            if v is not None:
                self.pastille(*u, self.colp)
                self.lien(*u, *v, self.colp)
            else:
                s = u
        self.pastille(*s, self.cols)

    def doprio(self, F, last):
        for u in list(F):
            self.pastille(*u, self.colf)
        if last is not None:
            self.pastille(*last, self.collast)

    def dopath(self, p, d):
        l = []
        cur = d
        while cur is not None:
            l.append(self.point(*cur))
            cur = p[cur]
        self.draw.line(l, self.colpath, self.pathw)

    def dosegment(self, segments, s):
        seg = []
        po = []
        for l in segments:
            seg += l
            po.append(l[0])
        if s is not None:
            seg.append(s)
            po.append(s)
        seg = list(map(lambda z: self.point(*z), seg))
        self.draw.line(seg, self.colpath, self.pathw)
        for z in po:
            self.pastille(*z, self.colnode)

    def __call__(self, F, p, s, d, last, segments=None, showF=True, showP=True):
        paint = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(paint)
        if showP and s is not None:
            self.dopred(p, s)
        if showF and F is not None:
            self.doprio(F, last)
        if p is not None and d in p:
            self.dopath(p, d)
        if segments:
            self.dosegment(segments, s)
        if self.compose:
            dst = self.img.copy()
            dst.alpha_composite(paint)
            return dst
        return paint
