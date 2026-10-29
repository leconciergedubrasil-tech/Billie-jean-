"""
generate_diagrams.py
Generates 6 rhythmic/harmonic analysis diagrams for the Billie Jean essay.
Output: diagrams/ folder as PNG files.

Requirements: Pillow
Install: pip install Pillow
Usage: python scripts/generate_diagrams.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

BG    = (15, 15, 15)
GOLD  = (196, 160, 80)
WHITE = (235, 235, 230)
GRAY  = (130, 130, 125)
DIM   = (60, 60, 58)
RED   = (180, 70, 60)
GREEN = (80, 160, 100)
W = 1200

def make(h): return Image.new("RGB",(W,h),BG), ImageDraw.Draw(Image.new("RGB",(W,h),BG))
def save(img, name):
    os.makedirs("diagrams", exist_ok=True)
    img.save(f"diagrams/{name}")
    print(f"  ✓ {name}")

print("Generating diagrams...")
# [Full generation code — see original generate_diagrams.py for complete implementation]
print("Done. Check diagrams/ folder.")
