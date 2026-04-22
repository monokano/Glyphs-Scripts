#MenuTitle: Deactivate Test Fonts
# -*- coding: utf-8 -*-
__doc__ = """Glyphsのテストインストール機能でアクティベートされたフォントをディアクティベートします。"""

import os
import re
import subprocess
from Foundation import NSURL
from CoreText import (
    CTFontCreateWithName,
    CTFontCopyAttribute,
    CTFontManagerUnregisterFontsForURL,
    kCTFontURLAttribute,
)

kCTFontManagerScopeSession = 3


def find_font_files(folder):
    result = []
    for root, _, files in os.walk(folder):
        for name in files:
            if name.lower().endswith(('.otf', '.ttf')):
                result.append(os.path.join(root, name))
    return result


def get_ps_name(font_path):
    try:
        raw = subprocess.check_output(
            ['mdls', font_path], stderr=subprocess.DEVNULL, encoding='utf-8'
        )
    except subprocess.CalledProcessError:
        return None
    compact = re.sub(r'\s+', '', raw)
    m = re.search(r'com_apple_ats_name_postscript=\("(.+?)"', compact)
    return m.group(1) if m else None


def is_activated(font_path):
    ps_name = get_ps_name(font_path)
    if not ps_name:
        return False
    font_ref = CTFontCreateWithName(ps_name, 10.0, None)
    if font_ref is None:
        return False
    url = CTFontCopyAttribute(font_ref, kCTFontURLAttribute)
    if url is None:
        return False
    return os.path.normcase(url.path()) == os.path.normcase(font_path)


def deactivate_font(font_path):
    url = NSURL.fileURLWithPath_(font_path)
    result = CTFontManagerUnregisterFontsForURL(url, kCTFontManagerScopeSession, None)
    if isinstance(result, (list, tuple)):
        return result[0]
    return bool(result)


# ---- メイン処理 ----

def main():
    temp_folder = os.path.expanduser("~/Library/Application Support/Glyphs 3/Temp")

    TITLE = "Deactivate Test Fonts"

    if not os.path.isdir(temp_folder):
        Message(
            "Glyphs 3のTempフォルダが見つかりませんでした。\n"
            "テストインストールされたフォントがまだ有効な場合はログアウトしてください。",
            TITLE
        )
        return

    font_files = find_font_files(temp_folder)
    activated = [f for f in font_files if is_activated(f)]

    if not activated:
        Message("Tempフォルダ内にアクティベートされているフォントはありませんでした。", TITLE)
        return

    deactivated_names = []
    failed_names = []

    for font_path in activated:
        name = os.path.basename(font_path)
        if deactivate_font(font_path):
            deactivated_names.append(name)
        else:
            failed_names.append(name)

    if failed_names:
        Message(
            "ディアクティベートできなかったフォント:\n\n"
            + "\n".join(failed_names),
            TITLE
        )
    else:
        Message(
            "以下のフォントを\nディアクティベートしました:\n\n"
            + "\n".join(deactivated_names)
            + "\n\nテストインストールされたフォントがまだ有効な場合はログアウトしてください。",
            TITLE
        )

main()
