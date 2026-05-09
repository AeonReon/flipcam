#!/usr/bin/env python3
"""Generate FlipCam icon set.

Design: rounded coral square (like the iOS app icon shape), with a big white
camera lens (rear cam) and a smaller teal lens at bottom-left (front cam in PiP),
echoing the dual-camera concept.

Outputs:
- images/icon-192.png         (192x192, transparent corners)
- images/icon-512.png         (512x512)
- images/icon-maskable.png    (512x512 with 20% safe-area padding for Android adaptive)
- images/apple-touch-icon.png (180x180)
- images/favicon.png          (32x32)
"""
from PIL import Image, ImageDraw
from pathlib import Path

# Palette (matches index.html :root)
CORAL      = (255, 106, 87, 255)
CORAL_DEEP = (225,  69, 53, 255)
CREAM      = (255, 244, 238, 255)
INK        = ( 42,  31,  44, 255)
TEAL       = ( 46, 184, 164, 255)


def rounded_rect_mask(size, radius):
    img = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    return img


def render_icon(size, *, maskable=False):
    s = size
    img = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if maskable:
        # Maskable: fill the entire square with coral so Android can crop to any shape.
        draw.rectangle((0, 0, s, s), fill=CORAL)
        # Safe-area inset = 20% of the icon side. All meaningful art lives inside this.
        inset = int(s * 0.20)
        ax, ay = inset, inset
        aw, ah = s - inset * 2, s - inset * 2
    else:
        # Standard: rounded coral tile (~22% radius, matches iOS feel)
        radius = int(s * 0.22)
        draw.rounded_rectangle((0, 0, s - 1, s - 1), radius=radius, fill=CORAL)
        ax, ay = 0, 0
        aw, ah = s, s

    cx = ax + aw / 2
    cy = ay + ah / 2

    # Big rear-camera lens — cream ring with dark inner circle, offset slightly up-right
    big_r = aw * 0.30
    big_cx = cx + aw * 0.08
    big_cy = cy - ah * 0.05
    draw.ellipse((big_cx - big_r, big_cy - big_r, big_cx + big_r, big_cy + big_r),
                 fill=CREAM)
    inner_r = big_r * 0.62
    draw.ellipse((big_cx - inner_r, big_cy - inner_r,
                  big_cx + inner_r, big_cy + inner_r), fill=INK)
    # Tiny highlight on the lens
    hi_r = inner_r * 0.28
    hi_cx = big_cx - inner_r * 0.35
    hi_cy = big_cy - inner_r * 0.35
    draw.ellipse((hi_cx - hi_r, hi_cy - hi_r, hi_cx + hi_r, hi_cy + hi_r),
                 fill=(255, 255, 255, 200))

    # Small front-camera lens (PiP), bottom-left, teal with cream border
    sm_r = aw * 0.18
    sm_cx = cx - aw * 0.20
    sm_cy = cy + ah * 0.20
    border = max(2, int(aw * 0.025))
    draw.ellipse((sm_cx - sm_r - border, sm_cy - sm_r - border,
                  sm_cx + sm_r + border, sm_cy + sm_r + border), fill=CREAM)
    draw.ellipse((sm_cx - sm_r, sm_cy - sm_r, sm_cx + sm_r, sm_cy + sm_r),
                 fill=TEAL)
    # Flip arrow inside small lens
    arrow_w = sm_r * 0.55
    arrow_h = sm_r * 0.55
    cx_a, cy_a = sm_cx, sm_cy
    line_w = max(2, int(sm_r * 0.18))
    # Two-arrow loop suggesting "swap"
    # Top arrow pointing right
    draw.line([(cx_a - arrow_w * 0.7, cy_a - arrow_h * 0.32),
               (cx_a + arrow_w * 0.6, cy_a - arrow_h * 0.32)],
              fill=CREAM, width=line_w)
    draw.polygon([
        (cx_a + arrow_w * 0.6,  cy_a - arrow_h * 0.32),
        (cx_a + arrow_w * 0.25, cy_a - arrow_h * 0.62),
        (cx_a + arrow_w * 0.25, cy_a - arrow_h * 0.02),
    ], fill=CREAM)
    # Bottom arrow pointing left
    draw.line([(cx_a + arrow_w * 0.7, cy_a + arrow_h * 0.32),
               (cx_a - arrow_w * 0.6, cy_a + arrow_h * 0.32)],
              fill=CREAM, width=line_w)
    draw.polygon([
        (cx_a - arrow_w * 0.6,  cy_a + arrow_h * 0.32),
        (cx_a - arrow_w * 0.25, cy_a + arrow_h * 0.62),
        (cx_a - arrow_w * 0.25, cy_a + arrow_h * 0.02),
    ], fill=CREAM)

    return img


OUT = Path(__file__).resolve().parent.parent / "images"
OUT.mkdir(parents=True, exist_ok=True)

specs = [
    ('icon-192.png',         192, False),
    ('icon-512.png',         512, False),
    ('icon-maskable.png',    512, True),
    ('apple-touch-icon.png', 180, False),
    ('favicon.png',           32, False),
]

for name, size, maskable in specs:
    img = render_icon(size, maskable=maskable)
    img.save(OUT / name, 'PNG', optimize=True)
    print(f"  ✓ {name} ({size}x{size}{', maskable' if maskable else ''})")

print(f"\nIcons written to: {OUT}")
