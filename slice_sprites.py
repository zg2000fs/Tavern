#!/usr/bin/env python3
"""Slice characters.png into agent_0..4.png with background removed.

The source image has 5 sprites on a white (or near-white/light-gray)
background. Strips bg where: saturation low (max-min <= 18) AND
brightness >= 125. Applies feathering in the 125-220 brightness zone
so edges anti-alias cleanly against the dark tavern.
"""
from PIL import Image
import os, sys

def strip_bg(img):
    img = img.convert('RGBA')
    data = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = data[x, y]
            mn, mx = min(r,g,b), max(r,g,b)
            br = (r + g + b) / 3
            if (mx - mn) <= 18 and br >= 125:
                if br >= 220:
                    data[x, y] = (r, g, b, 0)
                else:
                    # Feather edge zone 125-220 → alpha 0-180
                    alpha = max(0, round((220 - br) / 95 * 180))
                    data[x, y] = (r, g, b, alpha)
    return img

def autocrop_pad(img, pad=6):
    bbox = img.getbbox()
    if not bbox:
        return img
    cropped = img.crop(bbox)
    out = Image.new('RGBA', (cropped.width + pad*2, cropped.height + pad*2), (0,0,0,0))
    out.paste(cropped, (pad, pad))
    return out

def main():
    src = 'characters.png'
    if not os.path.exists(src):
        print(f'ERROR: {src} not found in current directory.')
        sys.exit(1)

    img = Image.open(src).convert('RGBA')
    W, H = img.size
    sw = W // 5
    print(f'Source: {W}x{H}, slicing into 5 @ {sw}px each')

    for i in range(5):
        region = img.crop((i*sw, 0, (i+1)*sw, H))
        region = strip_bg(region)
        region = autocrop_pad(region, pad=6)
        out = f'agent_{i}.png'
        region.save(out)
        print(f'  Saved {out}  {region.size}')

    print('Done. Place agent_0..4.png alongside tavern.html.')

if __name__ == '__main__':
    main()
