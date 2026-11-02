#!/usr/bin/env python3
"""Hasilkan drawable shape (bg_*, progress_*, dot_*) dari token style draft.html.

Pemakaian (dari root project):
    python3 tools/gen_drawables.py app/src/main/res/drawable
"""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

HEAD = '<?xml version="1.0" encoding="utf-8"?>\n'
NS = 'xmlns:android="http://schemas.android.com/apk/res/android"'


def write(name, body):
    (OUT / (name + ".xml")).write_text(HEAD + body + "\n", encoding="utf-8")


def shape_inner(solid=None, stroke=None, radius=None, grad=None, dashed=False,
                oval=False, radii=None, indent="    "):
    kind = "oval" if oval else "rectangle"
    lines = [indent + '<shape android:shape="%s">' % kind]
    i2 = indent + "    "
    if grad:
        angle, colors = grad
        attrs = 'android:angle="%d"' % angle
        if len(colors) == 2:
            attrs += ' android:startColor="%s" android:endColor="%s"' % tuple(colors)
        else:
            attrs += ' android:startColor="%s" android:centerColor="%s" android:endColor="%s"' % tuple(colors)
        lines.append(i2 + "<gradient %s />" % attrs)
    elif solid:
        lines.append(i2 + '<solid android:color="%s" />' % solid)
    if stroke:
        color, width = stroke
        extra = ' android:dashWidth="5dp" android:dashGap="4dp"' if dashed else ""
        lines.append(i2 + '<stroke android:width="%s" android:color="%s"%s />' % (width, color, extra))
    if radii:
        tl, tr, br, bl = radii
        lines.append(i2 + '<corners android:topLeftRadius="%s" android:topRightRadius="%s" '
                     'android:bottomRightRadius="%s" android:bottomLeftRadius="%s" />' % (tl, tr, br, bl))
    elif radius is not None:
        lines.append(i2 + '<corners android:radius="%s" />' % radius)
    lines.append(indent + "</shape>")
    return "\n".join(lines)


def shape(name, **kw):
    inner = shape_inner(indent="", **kw)
    inner = inner.replace("<shape ", "<shape %s " % NS, 1)
    write(name, inner)


def ripple(name, ripple_color, **kw):
    body = '<ripple %s\n    android:color="%s">\n    <item>\n%s\n    </item>\n</ripple>' % (
        NS, ripple_color, shape_inner(indent="        ", **kw))
    write(name, body)


# ---------- Kartu ----------
LINE = "@color/sf_line"
for name, r in (("bg_card", "18dp"), ("bg_card_16", "16dp"), ("bg_card_14", "14dp"), ("bg_card_12", "12dp")):
    shape(name, solid="@color/sf_card", stroke=(LINE, "1dp"), radius=r)
shape("bg_card_tint", grad=(315, ["#FAFCF9", "#F1F7F2"]), stroke=(LINE, "1dp"), radius="18dp")
shape("bg_card_unread", grad=(0, ["#F8FDF9", "#FFFFFF"]), stroke=("#CFE6D9", "1dp"), radius="14dp")
shape("bg_card_danger_tint", grad=(315, ["#FDF2F1", "#FFFFFF"]), stroke=("@color/sf_danger_line", "1dp"), radius="18dp")
shape("bg_empty", solid="@color/sf_card", stroke=("@color/sf_line_strong", "1dp"), radius="18dp", dashed=True)

# ---------- Notice / alert ----------
shape("bg_notice_danger", grad=(0, ["#FDF0EF", "#FFFFFF"]), stroke=("@color/sf_danger_line", "1dp"), radius="14dp")
shape("bg_notice_warn", grad=(0, ["#FDF6E8", "#FFFFFF"]), stroke=("@color/sf_warn_line", "1dp"), radius="14dp")
for kind in ("danger", "warn", "info", "safe"):
    shape("bg_alert_" + kind, solid="@color/sf_%s_bg" % kind, stroke=("@color/sf_%s_line" % kind, "1dp"), radius="12dp")

# ---------- Pill status ----------
shape("bg_pill_safe", solid="@color/sf_safe_bg", stroke=("@color/sf_safe_line", "1dp"), radius="99dp")
shape("bg_pill_warn", solid="@color/sf_warn_bg", stroke=("@color/sf_warn_line", "1dp"), radius="99dp")
shape("bg_pill_danger", solid="@color/sf_danger_bg", stroke=("@color/sf_danger_line", "1dp"), radius="99dp")
shape("bg_pill_muted", solid="#F1F4F2", stroke=("#E4EAE6", "1dp"), radius="99dp")
shape("bg_pill_info", solid="@color/sf_info_bg", stroke=("@color/sf_info_line", "1dp"), radius="99dp")
shape("bg_pill_violet", solid="@color/sf_violet_bg", stroke=("#E2DCF0", "1dp"), radius="99dp")
shape("bg_pill_brand", solid="@color/sf_mint", radius="99dp")
shape("bg_pill_outline", solid="@color/sf_card", stroke=("@color/sf_line_strong", "1dp"), radius="99dp")

# ---------- Lingkaran ikon ----------
for kind, fill in (("mint", "@color/sf_mint_2"), ("warn", "@color/sf_warn_bg"), ("danger", "@color/sf_danger_bg"),
                   ("info", "@color/sf_info_bg"), ("violet", "@color/sf_violet_bg"), ("muted", "@color/sf_muted_bg"),
                   ("safe", "@color/sf_safe_bg")):
    shape("bg_ic_" + kind, solid=fill, radius="12dp")

# ---------- Ikon produk ----------
for kind, fill, stroke in (("food", "#FDF4E4", "#F4E5C8"), ("drink", "#EAF4FB", "#D9EAF5"),
                           ("med", "#F9EDF0", "#F3DCE1"), ("home", "#EEF6F0", "#DCECDF"),
                           ("other", "#F1F2F1", "#E4E7E4"), ("default", "@color/sf_mint_2", "#E3EEE8")):
    shape("bg_product_" + kind, solid=fill, stroke=(stroke, "1dp"), radius="13dp")

# ---------- Tombol ----------
ripple("bg_btn_primary", "#33FFFFFF", grad=(315, ["#12875D", "#07563D"]), radius="12dp")
ripple("bg_btn_dark", "#33FFFFFF", solid="@color/sf_brand_ink", radius="12dp")
ripple("bg_btn_ghost", "#1F0B6B4F", solid="@color/sf_card", stroke=("@color/sf_line_strong", "1dp"), radius="12dp")
ripple("bg_btn_soft", "#1F0B6B4F", solid="@color/sf_mint_2", stroke=("@color/sf_safe_line", "1dp"), radius="12dp")
ripple("bg_btn_danger", "#33FFFFFF", solid="@color/sf_danger", radius="12dp")
ripple("bg_btn_danger_soft", "#1FB4473F", solid="@color/sf_danger_bg", stroke=("@color/sf_danger_line", "1dp"), radius="12dp")
ripple("bg_iconbtn_boxed", "#1F0B6B4F", solid="@color/sf_card", stroke=(LINE, "1dp"), radius="11dp")
ripple("bg_ripple_row", "#140B6B4F", solid="#00FFFFFF", radius="0dp")

# ---------- Chip, search, input ----------
shape("bg_chip", solid="@color/sf_card", stroke=(LINE, "1dp"), radius="99dp")
shape("bg_chip_active", solid="@color/sf_brand", stroke=("@color/sf_brand", "1dp"), radius="99dp")
shape("bg_search", solid="@color/sf_card", stroke=(LINE, "1dp"), radius="13dp")
shape("bg_input", solid="@color/sf_input_bg", stroke=("@color/sf_line_strong", "1dp"), radius="10dp")
shape("bg_input_error", solid="#FFFAFA", stroke=("#CF6B63", "1dp"), radius="10dp")
shape("bg_segmented", solid="@color/sf_seg_bg", radius="13dp")
shape("bg_segment_active", solid="@color/sf_card", radius="10dp")
shape("bg_radio_card", solid="@color/sf_input_bg", stroke=("@color/sf_line_strong", "1dp"), radius="12dp")
shape("bg_radio_card_on", solid="#F4FBF7", stroke=("#84C3A8", "1dp"), radius="12dp")
shape("bg_status_preview", solid="#F4F8F5", stroke=("@color/sf_line_strong", "1dp"), radius="10dp", dashed=True)
shape("bg_attach", solid="@color/sf_card", stroke=(LINE, "1dp"), radius="10dp")
shape("bg_attach_add", solid="@color/sf_card", stroke=("@color/sf_line_strong", "1dp"), radius="10dp", dashed=True)

# ---------- Progress ----------
for kind, (a, b) in (("safe", ("#26A474", "#0B6B4F")), ("warn", ("#E5B45D", "#C7851D")),
                     ("danger", ("#DD8B83", "#B4473F")), ("muted", ("#B6C3BC", "#8C9C93"))):
    body = ('<layer-list %s>\n    <item android:id="@android:id/background">\n%s\n    </item>\n'
            '    <item android:id="@android:id/progress">\n        <clip>\n%s\n        </clip>\n    </item>\n</layer-list>') % (
        NS, shape_inner(solid="@color/sf_track", radius="99dp", indent="        "),
        shape_inner(grad=(0, [a, b]), radius="99dp", indent="            "))
    write("progress_" + kind, body)

# ---------- Dot ----------
for kind, color in (("safe", "#1D8A61"), ("warn", "#CF8B23"), ("danger", "#C05B52"), ("muted", "#9AA9A1"),
                    ("brand", "#12875D")):
    shape("dot_" + kind, solid=color, oval=True)

# ---------- Shell ----------
shape("bg_brand_mark", grad=(315, ["#12875D", "#064E3B"]), radius="11dp")
shape("bg_avatar", grad=(315, ["#CFEADD", "#9FD1BA"]), radius="12dp")
shape("bg_avatar_staff", grad=(315, ["#D8E2F0", "#AEBFD9"]), radius="12dp")
shape("bg_avatar_lg", grad=(315, ["#CFEADD", "#9FD1BA"]), radius="18dp")
shape("bg_avatar_lg_staff", grad=(315, ["#D8E2F0", "#AEBFD9"]), radius="18dp")
shape("bg_badge", solid="#C05047", stroke=("@color/sf_bg", "2dp"), radius="99dp")
shape("bg_date_chip", solid="#B3FFFFFF", stroke=(LINE, "1dp"), radius="9dp")
shape("bg_tab_active", solid="@color/sf_mint", radius="9dp")
shape("bg_batch_code", solid="#F2F6F3", stroke=("#E7EEE9", "1dp"), radius="5dp")
shape("bg_schema_ic", solid="#F1F6F3", radius="8dp")
shape("bg_schema_count", solid="@color/sf_mint_2", radius="99dp")
shape("bg_toast", solid="#073B2A", radius="11dp")

write("bg_topbar_sub", ('<layer-list %s>\n    <item><shape android:shape="rectangle"><solid android:color="@color/sf_bg" /></shape></item>\n'
                        '    <item android:gravity="bottom" android:height="1dp"><shape android:shape="rectangle">'
                        '<solid android:color="#0F093A2A" /></shape></item>\n</layer-list>') % NS)
write("bg_tabbar", ('<layer-list %s>\n    <item><shape android:shape="rectangle"><solid android:color="#F5FFFFFF" /></shape></item>\n'
                    '    <item android:gravity="top" android:height="1dp"><shape android:shape="rectangle">'
                    '<solid android:color="#12093A2A" /></shape></item>\n</layer-list>') % NS)
write("bg_actionbar", ('<layer-list %s>\n    <item><shape android:shape="rectangle"><solid android:color="#F5FFFFFF" /></shape></item>\n'
                       '    <item android:gravity="top" android:height="1dp"><shape android:shape="rectangle">'
                       '<solid android:color="#14093A2A" /></shape></item>\n</layer-list>') % NS)

# ---------- Hero ----------
shape("bg_hero_owner", grad=(315, ["#0A6045", "#063C2B", "#04281D"]), radius="24dp")
shape("bg_hero_staff", grad=(315, ["#1F4F6B", "#123B51", "#0B2939"]), radius="24dp")
shape("bg_hero_orbit", solid="#00FFFFFF", stroke=("#42A7EECC", "1dp"), oval=True)
shape("bg_hero_orbit_staff", solid="#00FFFFFF", stroke=("#3DB4E0F6", "1dp"), oval=True)

# ---------- Sheet ----------
shape("bg_sheet", solid="@color/sf_card", radii=("22dp", "22dp", "0dp", "0dp"))
shape("bg_sheet_grab", solid="#D9E2DC", radius="99dp")

# ---------- Login (gelap) ----------
shape("bg_auth", grad=(270, ["@color/sf_auth_top", "@color/sf_auth_mid", "@color/sf_auth_bottom"]))
shape("bg_auth_card", solid="#0FFFFFFF", stroke=("#29BAF0D3", "1dp"), radius="18dp")
shape("bg_auth_brand_mark", solid="#1AFFFFFF", stroke=("#38B1F0D0", "1dp"), radius="14dp")
ripple("bg_auth_demo", "#1FFFFFFF", solid="#0DFFFFFF", stroke=("#2EB8E8D1", "1dp"), radius="11dp")
shape("bg_auth_avatar", solid="#29B7EBD0", radius="9dp")
shape("bg_auth_pill", solid="#14FFFFFF", stroke=("#24B8E8D1", "1dp"), radius="99dp")
shape("bg_auth_note", solid="#0AFFFFFF", stroke=("#24B8E8D1", "1dp"), radius="10dp")
shape("bg_auth_input", solid="#14FFFFFF", stroke=("#33BEECD5", "1dp"), radius="10dp")

print("selesai")
