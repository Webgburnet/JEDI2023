import numpy as np
from math import sqrt
from functools import lru_cache

sq2 = sqrt(2)


def filtre(m, K):
    mc = np.zeros(m.shape)
    for dr in range(-1, 2):
        mr = np.roll(m, dr, 0)
        for dc in range(-1, 2):
            mrc = np.roll(mr, dc, 1)
            mc = mc + K[dr + 1, dc + 1] * mrc
    raw = np.abs(mc)
    return 1 + (np.max(raw) - raw)


HN = np.matrix("1 0 -1; 1 0 -1; 0 0 0") / 4
HW = np.matrix("1 1 0; 0 0 0; -1 -1 0") / 4
HE = np.matrix("0 1 1; 0 0 0; 0 -1 -1") / 4
HS = np.matrix("0 0 0; 1 0 -1; 1 0 -1") / 4
HNE = np.matrix("0 1 0; 0 0 -1; 0 0 0") / sq2
HNW = np.matrix("0 1 0; -1 0 0; 0 0 0") / sq2
HSE = np.matrix("0 0 0; 0 0 -1; 0 1 0") / sq2
HSW = np.matrix("0 0 0; -1 0 0; 0 1 0") / sq2
Hvois = [
    ((-1, -1), HNW),
    ((0, -1), HN),
    ((1, -1), HNE),
    ((-1, 0), HW),
    ((1, 0), HE),
    ((-1, 1), HSW),
    ((0, 1), HS),
    ((1, 1), HSE),
]


class GDelta:
    def __init__(self, img):
        data = np.asarray(img.convert("L"))
        self.vois = [(dz, filtre(data, H)) for (dz, H) in Hvois]
        self.w = np.size(data, 1)
        self.h = np.size(data, 0)

    @lru_cache(128)
    def __getitem__(self, z):
        (x, y) = z
        if x < 1 or self.w <= x + 1 or y < 1 or self.h <= y + 1:
            return KeyError(z)
        v = {
            (x + dx, y + dy): w[y + dy][x + dx]
            for ((dx, dy), w) in self.vois
            if 1 < x + dx + 1 < self.w and 1 < y + dy + 1 < self.h
        }
        return v

    def __len__(self):
        return (self.w - 2) * (self.h - 2)

    def __iter__(self):
        for y in range(1, self.h - 1):
            for x in range(1, self.w - 1):
                yield (x, y)
