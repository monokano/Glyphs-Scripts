#MenuTitle: Set AJ1 Unicode JP04

# -*- coding: utf-8 -*-
__doc__ = """
AJ1のCMapに基づいてUnicodeを設定します。
CMap: UniJIS2004-UTF32-H（GitHubから取得）
NiceNameは実行中のGlyphsアプリのMapFileAdobe-Japan1.txtから取得します。
"""

import os
import re
import ssl
import urllib.request
from Foundation import NSBundle

CMAP_URL = (
    "https://raw.githubusercontent.com/adobe-type-tools/cmap-resources"
    "/master/Adobe-Japan1-7/CMap/UniJIS2004-UTF32-H"
)


def fetch_url(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "GlyphsScript"})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
        return response.read().decode("utf-8")


def build_cid_unicode_map(cmap_text):
    """CMapテキストからCID→Unicodeリストのマッピングを構築する。
    notdefrange（CID 1 に 0000〜001F を含む）も処理する。"""
    cid_to_unicodes = {}

    def add(cid, u):
        cid_to_unicodes.setdefault(cid, []).append(format(u, '04X'))

    mode = None
    for line in cmap_text.splitlines():
        line = line.strip()
        if line.endswith('beginnotdefrange'):
            mode = 'notdefrange'
        elif line.endswith('begincidchar'):
            mode = 'char'
        elif line.endswith('begincidrange'):
            mode = 'range'
        elif line in ('endnotdefrange', 'endcidchar', 'endcidrange'):
            mode = None
        elif mode == 'notdefrange':
            m = re.match(r'<([0-9a-fA-F]+)>\s+<([0-9a-fA-F]+)>\s+(\d+)', line)
            if m:
                u_start, u_end, cid = int(m.group(1), 16), int(m.group(2), 16), int(m.group(3))
                for u in range(u_start, u_end + 1):
                    add(cid, u)
        elif mode == 'char':
            m = re.match(r'<([0-9a-fA-F]+)>\s+(\d+)', line)
            if m:
                add(int(m.group(2)), int(m.group(1), 16))
        elif mode == 'range':
            m = re.match(r'<([0-9a-fA-F]+)>\s+<([0-9a-fA-F]+)>\s+(\d+)', line)
            if m:
                u_start, u_end, cid_start = int(m.group(1), 16), int(m.group(2), 16), int(m.group(3))
                for i, u in enumerate(range(u_start, u_end + 1)):
                    add(cid_start + i, u)

    return {cid: sorted(unicodes, key=lambda x: int(x, 16))
            for cid, unicodes in cid_to_unicodes.items()}


def load_mapping():
    """CMapとMapFileを組み合わせて {nicename: unicode_list} を構築する"""
    try:
        cmap_text = fetch_url(CMAP_URL)
    except Exception as e:
        Message(f"CMapの取得に失敗しました:\n{e}", title="エラー")
        return None

    cid_to_unicodes = build_cid_unicode_map(cmap_text)

    map_file = os.path.join(
        NSBundle.mainBundle().bundlePath(),
        "Contents/Frameworks/GlyphsCore.framework/Versions/A/Resources/MapFileAdobe-Japan1.txt"
    )
    if not os.path.exists(map_file):
        Message(f"MapFileAdobe-Japan1.txt が見つかりません:\n{map_file}", title="エラー")
        return None

    result = {}
    with open(map_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue
            cid = int(parts[0])
            nicename = parts[1]
            result[nicename] = cid_to_unicodes.get(cid, [])

    return result


def main():
    font = Glyphs.font
    if font is None:
        Message("フォントが開かれていません。", title="エラー")
        return

    mapping = load_mapping()
    if mapping is None:
        return

    unknown_names = [g.name for g in font.glyphs if g.export and g.name not in mapping]
    if unknown_names:
        lines = ["以下の Nice Name はマッピングに含まれていません。", "Unicodeの設定は行っていません。", ""]
        for name in unknown_names:
            lines.append(f"・{name}")
        Message("\n".join(lines), title="未知の Nice Name が見つかりました")
        return

    set_count = 0
    skipped_count = 0

    font.disableUpdateInterface()
    try:
        for glyph in font.glyphs:
            if not glyph.export:
                continue
            new_unicodes = mapping[glyph.name]
            current = list(glyph.unicodes) if glyph.unicodes else []
            if current != new_unicodes:
                glyph.unicodes = new_unicodes
                set_count += 1
            else:
                skipped_count += 1
    finally:
        font.enableUpdateInterface()

    total = set_count + skipped_count
    msg = (
        f"Unicode を設定　　{set_count} グリフ\n"
        f"変更なし　　　　　{skipped_count} グリフ\n"
        f"────────────────\n"
        f"合計　　　　　　　{total} グリフ"
    )
    Message(msg, title="処理完了")


main()
