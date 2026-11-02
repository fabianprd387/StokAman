#!/usr/bin/env python3
"""Hasilkan view_tabbar_{owner|staff}_{beranda|barang|laporan|riwayat|profil}.xml.

Pemakaian (dari root project):
    python3 tools/gen_tabbars.py app/src/main/res/layout
"""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])

TABS = {
    "owner": [("beranda", "Beranda", "ic_home"), ("barang", "Barang", "ic_box"),
              ("laporan", "Laporan", "ic_chart"), ("profil", "Profil", "ic_user")],
    "staff": [("beranda", "Beranda", "ic_home"), ("barang", "Barang", "ic_box"),
              ("riwayat", "Riwayat", "ic_history"), ("profil", "Profil", "ic_user")],
}


def tab(key, label, icon, active):
    bg = '\n            android:background="@drawable/bg_tab_active"' if active else ""
    tint = "@color/sf_brand" if active else "@color/sf_tab_off"
    style = "@style/SF.Tab.Label.Active" if active else "@style/SF.Tab.Label"
    return f'''    <LinearLayout
        android:id="@+id/tab_{key}"
        style="@style/SF.Tab">

        <FrameLayout
            android:layout_width="36dp"
            android:layout_height="27dp"{bg}>

            <ImageView
                android:layout_width="19dp"
                android:layout_height="19dp"
                android:layout_gravity="center"
                android:src="@drawable/{icon}"
                app:tint="{tint}" />
        </FrameLayout>

        <TextView
            style="{style}"
            android:text="{label}" />
    </LinearLayout>
'''


for role, tabs in TABS.items():
    for key, _, _ in tabs:
        body = "\n".join(tab(k, l, i, k == key) for k, l, i in tabs)
        xml = f'''<?xml version="1.0" encoding="utf-8"?>
<!-- Tab bar {role}, tab aktif: {key} (draft.html .tabbar) -->
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="68dp"
    android:background="@drawable/bg_tabbar"
    android:orientation="horizontal"
    android:paddingHorizontal="12dp"
    android:paddingTop="6dp"
    android:paddingBottom="8dp"
    tools:ignore="HardcodedText,ContentDescription">

{body}</LinearLayout>
'''
        (OUT / f"view_tabbar_{role}_{key}.xml").write_text(xml, encoding="utf-8")
print("selesai")
