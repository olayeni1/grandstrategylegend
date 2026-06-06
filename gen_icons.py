#!/usr/bin/env python3
"""Generate PWA icons (no external deps) for Grand Strategy.
Draws a gradient rounded square with a white shield + gold star emblem."""
import zlib, struct, math, os

def lerp(a, b, t): return a + (b - a) * t

def hex2rgb(h): return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

BG_TOP = hex2rgb("667eea")
BG_BOT = hex2rgb("764ba2")
NAVY   = hex2rgb("0b1020")
WHITE  = (255, 255, 255)
GOLD   = hex2rgb("fbbf24")

def point_in_poly(px, py, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]; xj, yj = poly[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi + 1e-9) + xi):
            inside = not inside
        j = i
    return inside

def shield_poly(cx, cy, w, h):
    # rounded shield: top flat, sides taper to a point at bottom
    return [
        (cx - w/2, cy - h/2),
        (cx + w/2, cy - h/2),
        (cx + w/2, cy - h/2 + h*0.45),
        (cx,       cy + h/2),
        (cx - w/2, cy - h/2 + h*0.45),
    ]

def star_poly(cx, cy, r_out, r_in, points=5, rot=-math.pi/2):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = rot + i * math.pi / points
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def make_icon(size, maskable=False):
    # supersample 3x for smooth edges
    ss = 3
    S = size * ss
    px = bytearray(S * S * 4)
    pad = int(S * 0.12) if not maskable else 0   # corner radius region
    radius = int(S * 0.20)
    inset = 0 if maskable else int(S * 0.0)
    cx = cy = S / 2
    shield = shield_poly(cx, cy - S*0.02, S*0.46, S*0.56)
    star = star_poly(cx, cy - S*0.04, S*0.17, S*0.075)

    for y in range(S):
        t = y / (S - 1)
        br = int(lerp(BG_TOP[0], BG_BOT[0], t))
        bg = int(lerp(BG_TOP[1], BG_BOT[1], t))
        bb = int(lerp(BG_TOP[2], BG_BOT[2], t))
        for x in range(S):
            # rounded corner mask (transparent outside) for non-maskable
            a = 255
            if not maskable:
                rx = min(x, S - 1 - x); ry = min(y, S - 1 - y)
                if rx < radius and ry < radius:
                    dx = radius - rx; dy = radius - ry
                    if dx*dx + dy*dy > radius*radius:
                        a = 0
            r, g, b = br, bg, bb
            if a:
                if point_in_poly(x, y, shield):
                    r, g, b = WHITE
                    # navy inner field
                    inner = shield_poly(cx, cy - S*0.02, S*0.40, S*0.50)
                    if point_in_poly(x, y, inner):
                        r, g, b = NAVY
                        if point_in_poly(x, y, star):
                            r, g, b = GOLD
            o = (y * S + x) * 4
            px[o] = r; px[o+1] = g; px[o+2] = b; px[o+3] = a

    # downsample by ss (box filter) into final size
    out = bytearray(size * size * 4)
    for y in range(size):
        for x in range(size):
            tr = tg = tb = ta = 0
            for dy in range(ss):
                for dx in range(ss):
                    o = ((y*ss+dy) * S + (x*ss+dx)) * 4
                    al = px[o+3]
                    tr += px[o]*al; tg += px[o+1]*al; tb += px[o+2]*al; ta += al
            o2 = (y * size + x) * 4
            if ta:
                out[o2] = tr // ta; out[o2+1] = tg // ta; out[o2+2] = tb // ta
            out[o2+3] = ta // (ss*ss)
    return bytes(out)

def write_png(path, size, rgba):
    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)
    raw = bytearray()
    for y in range(size):
        raw.append(0)
        raw.extend(rgba[y*size*4:(y+1)*size*4])
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    print("wrote", path, size)

here = os.path.dirname(os.path.abspath(__file__))
ic = os.path.join(here, "icons")
write_png(os.path.join(ic, "icon-192.png"), 192, make_icon(192))
write_png(os.path.join(ic, "icon-512.png"), 512, make_icon(512))
write_png(os.path.join(ic, "icon-maskable-512.png"), 512, make_icon(512, maskable=True))
write_png(os.path.join(ic, "apple-touch-icon.png"), 180, make_icon(180, maskable=True))
print("done")
