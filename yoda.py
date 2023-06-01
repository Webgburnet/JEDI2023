#!/usr/bin/env python3
from gui import start
from PIL import Image
import argparse
import prios

parser = argparse.ArgumentParser(
    prog="yoda",
    description="Intelligent Scissors",
    epilog="Don't worry, be heap.py!",
)

parser.add_argument("image", nargs="?", default="data/bruD.png", help="source image")
parser.add_argument(
    "-p",
    "--priodict",
    choices=prios.choices,
    default=prios.default,
    help="priority dict implementation",
)
args = parser.parse_args()

prios.default = args.priodict
img = Image.open(args.image).convert("RGBA")
start(img)
