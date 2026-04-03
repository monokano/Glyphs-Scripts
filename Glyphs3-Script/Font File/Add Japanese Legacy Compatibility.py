#MenuTitle: Add Japanese Legacy Compatibility

# -*- coding: utf-8 -*-
__doc__="""
日本語フォント用。レガシー環境で日本語フォントとして認識されるよう下記を追加します。
・Mac Japanese cmap（platformID=1, platEncID=1）
・OS/2.ulCodePageRange1 にJIS/Japan（932）ビット（bit17）を設定
・Mac Roman nameレコード（platformID=1, platEncID=0, langID=0x0）
PythonモジュールのFontToolsのインストールが必要です。
"""

import sys
import os

# fontTools のパッケージルートを sys.path に追加
fonttools_lib = os.path.expanduser(
    "~/Library/Application Support/Glyphs 3/Repositories/fonttools/Lib"
)
if fonttools_lib not in sys.path:
    sys.path.insert(0, fonttools_lib)

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import _c_m_a_p
from AppKit import NSOpenPanel

# JIS/Japan (932) = bit17
BIT_JIS = 1 << 17   # 0x00020000


def select_font_file():
    panel = NSOpenPanel.openPanel()
    panel.setTitle_("フォントファイルを選択")
    panel.setMessage_("日本語レガシー互換設定を追加するフォントファイルを選んでください")
    panel.setAllowedFileTypes_(["otf", "ttf"])
    panel.setAllowsMultipleSelection_(False)
    panel.setCanChooseDirectories_(False)
    if panel.runModal() == 1:
        return panel.URL().path()
    return None


def build_mac_japanese_map(font):
    """Unicode cmap から Mac Japanese（Shift_JIS）コード → グリフ名 の辞書を生成"""
    unicode_cmap = font.getBestCmap()
    if not unicode_cmap:
        return {}

    sjis_map = {}
    for uni, glyph_name in unicode_cmap.items():
        try:
            char = chr(uni)
            sjis_bytes = char.encode('shift_jis_2004')
            if len(sjis_bytes) == 1:
                sjis_code = sjis_bytes[0]
            elif len(sjis_bytes) == 2:
                sjis_code = (sjis_bytes[0] << 8) | sjis_bytes[1]
            else:
                continue
            sjis_map[sjis_code] = glyph_name
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    return sjis_map


def add_mac_japanese_cmap(font):
    """Mac Japanese cmap（1,1）を追加。既存の場合はスキップ"""
    cmap_table = font["cmap"]
    existing = {(t.platformID, t.platEncID) for t in cmap_table.tables}

    if (1, 1) in existing:
        return "ℹ️ cmap (1,1) Mac Japanese: すでに存在します"

    sjis_map = build_mac_japanese_map(font)
    if not sjis_map:
        return "❌ cmap (1,1) Mac Japanese: Unicode cmapが見つかりません"

    t = _c_m_a_p.cmap_format_2(2)
    t.platformID = 1
    t.platEncID  = 1    # Macintosh Japanese
    t.language   = 11   # Japanese
    t.cmap       = sjis_map
    cmap_table.tables.append(t)
    return f"✅ cmap (1,1) Mac Japanese: {len(sjis_map)} エントリ追加"


def set_code_page_range(font):
    """ulCodePageRange1 に JIS/Japan（bit17）を設定。既存の場合はスキップ"""
    old_value = font["OS/2"].ulCodePageRange1

    if old_value & BIT_JIS:
        return "ℹ️ CodePageRange: JIS/Japan（932）ビットはすでに設定済みです"

    font["OS/2"].ulCodePageRange1 |= BIT_JIS
    new_value = font["OS/2"].ulCodePageRange1
    return f"✅ CodePageRange: {hex(old_value)} → {hex(new_value)}"


def add_mac_name_records(font):
    """Mac platform nameレコードを追加"""
    name_table = font["name"]
    added = 0

    # --- Mac Roman（platformID=1, platEncID=0, langID=0x0）---
    # 英語テキスト用 / Windows langID=0x409 から取得
    roman_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 14, 16, 17]
    for name_id in roman_ids:
        if name_table.getName(name_id, 1, 0, 0) is not None:
            continue
        record = name_table.getName(name_id, 3, 1, 0x409)
        if record is None:
            continue
        try:
            text = record.toUnicode()
            text.encode('mac_roman')   # エンコード可能かチェック
            name_table.setName(text, name_id, 1, 0, 0)
            added += 1
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass

    return added


# ============================================================
# メイン
# ============================================================

font_path = select_font_file()
if not font_path:
    Message("", "ファイルが選択されませんでした", OKButton="終了")
else:
    font = TTFont(font_path)

    if "vmtx" not in font:
        Message("", "❌\n\nこのフォントはvmtxがないので\n日本語フォントではありません。\n\n" + os.path.basename(font_path), OKButton="終了")
    else:
        cmap_result  = add_mac_japanese_cmap(font)
        range_result = set_code_page_range(font)
        name_added   = add_mac_name_records(font)

        font.save(font_path)

        result_text = (
            f"{os.path.basename(font_path)}\n\n"
            f"{cmap_result}\n\n"
            f"{range_result}\n\n"
            f"✅ Mac nameレコード: {name_added} 件追加"
        )
        Message("", result_text, OKButton="OK")