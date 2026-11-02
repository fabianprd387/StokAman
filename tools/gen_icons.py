#!/usr/bin/env python3
"""Hasilkan vector drawable (ic_*.xml) dari objek ICONS di draft.html.

Pemakaian (dari root project):
    python3 tools/gen_icons.py draft.html app/src/main/res/drawable
"""
import re
import sys
from pathlib import Path


def num(v):
    return float(v)


def fmt(x):
    s = ("%.3f" % x).rstrip("0").rstrip(".")
    return s if s else "0"


def circle(cx, cy, r):
    return "M%s,%sa%s,%s 0 1,0 %s,0a%s,%s 0 1,0 %s,0z" % (
        fmt(cx - r), fmt(cy), fmt(r), fmt(r), fmt(2 * r), fmt(r), fmt(r), fmt(-2 * r))


def ellipse(cx, cy, rx, ry):
    return "M%s,%sa%s,%s 0 1,0 %s,0a%s,%s 0 1,0 %s,0z" % (
        fmt(cx - rx), fmt(cy), fmt(rx), fmt(ry), fmt(2 * rx), fmt(rx), fmt(ry), fmt(-2 * rx))


def rect(x, y, w, h, rx, ry):
    rx = min(rx, w / 2)
    ry = min(ry, h / 2)
    if rx <= 0 and ry <= 0:
        return "M%s,%sh%sv%sh%sz" % (fmt(x), fmt(y), fmt(w), fmt(h), fmt(-w))
    return ("M%s,%sh%sa%s,%s 0 0 1 %s,%sv%sa%s,%s 0 0 1 %s,%sh%sa%s,%s 0 0 1 %s,%sv%sa%s,%s 0 0 1 %s,%sz" % (
        fmt(x + rx), fmt(y), fmt(w - 2 * rx), fmt(rx), fmt(ry), fmt(rx), fmt(ry),
        fmt(h - 2 * ry), fmt(rx), fmt(ry), fmt(-rx), fmt(ry),
        fmt(-(w - 2 * rx)), fmt(rx), fmt(ry), fmt(-rx), fmt(-ry),
        fmt(-(h - 2 * ry)), fmt(rx), fmt(ry), fmt(rx), fmt(-ry)))


def parse_elements(svg):
    out = []
    for m in re.finditer(r"<(path|circle|ellipse|rect)\s+([^>]*?)/?>", svg):
        tag = m.group(1)
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(2)))
        filled = attrs.get("fill") == "currentColor"
        if tag == "path":
            d = attrs["d"]
        elif tag == "circle":
            d = circle(num(attrs["cx"]), num(attrs["cy"]), num(attrs["r"]))
        elif tag == "ellipse":
            d = ellipse(num(attrs["cx"]), num(attrs["cy"]), num(attrs["rx"]), num(attrs["ry"]))
        else:
            rx = num(attrs.get("rx", attrs.get("ry", "0")))
            ry = num(attrs.get("ry", attrs.get("rx", "0")))
            d = rect(num(attrs.get("x", "0")), num(attrs.get("y", "0")),
                     num(attrs["width"]), num(attrs["height"]), rx, ry)
        out.append((d, filled))
    return out


SMALL = ["check-circle", "clock", "alert-triangle", "alert-circle", "archive", "arrow-down-left",
         "arrow-up-right", "swap-horiz", "package-x", "plus", "chevron-right", "check", "info",
         "calendar", "database", "shield-check", "lock", "clipboard-check", "calendar-clock",
         "download", "x", "save"]


def vector_xml(elements, size=24):
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<vector xmlns:android="http://schemas.android.com/apk/res/android"',
        '    android:width="%ddp"' % size,
        '    android:height="%ddp"' % size,
        '    android:viewportWidth="24"',
        '    android:viewportHeight="24">',
    ]
    for d, filled in elements:
        lines.append("    <path")
        lines.append('        android:pathData="%s"' % d)
        if filled:
            lines.append('        android:fillColor="#FFFFFF" />')
        else:
            lines.append('        android:strokeColor="#FFFFFF"')
            lines.append('        android:strokeWidth="1.8"')
            lines.append('        android:strokeLineCap="round"')
            lines.append('        android:strokeLineJoin="round" />')
    lines.append("</vector>")
    return "\n".join(lines) + "\n"


def main():
    html = Path(sys.argv[1]).read_text(encoding="utf-8")
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    start = html.index("const ICONS = {")
    end = html.index("};", start)
    block = html[start:end]
    count = 0
    for name, svg in re.findall(r"'([a-z0-9-]+)':\s*'((?:[^'\\]|\\.)*)'", block):
        elements = parse_elements(svg)
        if not elements:
            print("lewati (kosong):", name)
            continue
        fname = "ic_" + name.replace("-", "_") + ".xml"
        (out_dir / fname).write_text(vector_xml(elements), encoding="utf-8")
        if name in SMALL:
            (out_dir / ("ic12_" + name.replace("-", "_") + ".xml")).write_text(
                vector_xml(elements, 12), encoding="utf-8")
        count += 1
    print("selesai: %d ikon ditulis ke %s" % (count, out_dir))


if __name__ == "__main__":
    main()
