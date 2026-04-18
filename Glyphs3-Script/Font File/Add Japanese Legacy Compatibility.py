#MenuTitle: Add Japanese Legacy Compatibility

# -*- coding: utf-8 -*-
__doc__="""
日本語フォント用。日本語フォントとして認識されるよう下記を追加します。

【cmap】
・MacJapanese cmap（platformID=1, platEncID=1）を追加
・Windows Shift-JIS cmap（platformID=3, platEncID=2）が存在すれば削除

【OS/2】
・ulCodePageRange1にJIS/Japan（932）を設定
・usWinAscent/usWinDescentをFontBBoxの値に合わせる

【name】
・Mac Roman nameレコード（platformID=1, platEncID=0, langID=0x0）を調整
・Mac Japanese nameレコード（platformID=1, platEncID=1, langID=0xb）を調整
・Windows Japanese nameレコード（platformID=3, platEncID=1, langID=0x411）を調整

【meta】
・dlng タグに ja を設定（なければmetaテーブルを新規作成）

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


def select_font_files():
    panel = NSOpenPanel.openPanel()
    panel.setTitle_("フォントファイルを選択")
    panel.setMessage_("日本語レガシー互換設定を追加するフォントファイルを選んでください")
    panel.setAllowedFileTypes_(["otf", "ttf"])
    panel.setAllowsMultipleSelection_(True)
    panel.setCanChooseDirectories_(False)
    if panel.runModal() == 1:
        return [url.path() for url in panel.URLs()]
    return []


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
    """Mac Japanese cmap（1,1）を追加。正しいものが既存の場合はスキップ"""
    cmap_table = font["cmap"]

    # language=0 のものが既存かチェック
    existing_correct = any(
        t.platformID == 1 and t.platEncID == 1 and t.language == 0
        for t in cmap_table.tables
    )
    if existing_correct:
        return "ℹ️ cmap (1,1) Mac Japanese: すでに存在します"

    # language != 0 の誤ったレコードがあれば削除
    cmap_table.tables = [
        t for t in cmap_table.tables
        if not (t.platformID == 1 and t.platEncID == 1)
    ]

    sjis_map = build_mac_japanese_map(font)
    if not sjis_map:
        return "❌ cmap (1,1) Mac Japanese: Unicode cmapが見つかりません"

    t = _c_m_a_p.cmap_format_2(2)
    t.platformID = 1
    t.platEncID  = 1    # Macintosh Japanese
    t.language   = 0    # Unspecific
    t.cmap       = sjis_map
    cmap_table.tables.append(t)
    return f"✅ cmap (1,1) Mac Japanese: {len(sjis_map)} エントリ追加"


def remove_windows_sjis_cmap(font):
    """Windows Shift-JIS cmap（platformID=3, platEncID=2）が存在すれば削除"""
    cmap_table = font["cmap"]
    before = len(cmap_table.tables)
    cmap_table.tables = [
        t for t in cmap_table.tables
        if not (t.platformID == 3 and t.platEncID == 2)
    ]
    after = len(cmap_table.tables)
    if before != after:
        return "✅ cmap (3,2) Windows Shift-JIS: 削除しました"


def set_code_page_range(font):
    """ulCodePageRange1 に JIS/Japan（bit17）を設定。既存の場合はスキップ"""
    old_value = font["OS/2"].ulCodePageRange1

    if old_value & BIT_JIS:
        return "ℹ️ CodePageRange: JIS/Japan（932）ビットはすでに設定済みです"

    font["OS/2"].ulCodePageRange1 |= BIT_JIS
    new_value = font["OS/2"].ulCodePageRange1
    return f"✅ CodePageRange: {hex(old_value)} → {hex(new_value)}"


def add_mac_name_records(font):
    """Mac Roman nameレコード（platformID=1, platEncID=0, langID=0x0）を追加"""
    name_table = font["name"]

    target_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 14, 16, 17]
    added = 0

    for name_id in target_ids:
        if name_table.getName(name_id, 1, 0, 0) is not None:
            continue
        record = name_table.getName(name_id, 3, 1, 0x409)
        if record is None:
            continue
        try:
            text = record.toUnicode()
            text.encode('mac_roman')
            name_table.setName(text, name_id, 1, 0, 0)
            added += 1
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass

    return added


def fix_win_japanese_name(font):
    """
    (3,1,0x411) の修正:
    ・nameID=1 を nameID=16+17 から再構築（Glyphsが英語スタイル名を使う問題を修正）
    ・nameID=4 の英語名混入を削除
    """
    name_table = font["name"]

    # (3,1,0x411) が存在しない場合はスキップ
    if name_table.getName(1, 3, 1, 0x411) is None:
        return None

    msgs = []

    # nameID=1 を nameID=16 + nameID=17 から再構築
    rec16 = name_table.getName(16, 3, 1, 0x411)
    rec17 = name_table.getName(17, 3, 1, 0x411)
    if rec16 and rec17:
        expected = rec16.toUnicode() + " " + rec17.toUnicode()
        rec1     = name_table.getName(1, 3, 1, 0x411)
        current  = rec1.toUnicode() if rec1 else None
        if current != expected:
            name_table.setName(expected, 1, 3, 1, 0x411)
            msgs.append(f"nameID=1: {current!r} → {expected!r}")

    # nameID=4 削除
    if name_table.getName(4, 3, 1, 0x411) is not None:
        name_table.removeNames(nameID=4, platformID=3, platEncID=1, langID=0x411)
        msgs.append("nameID=4 削除")

    if msgs:
        return "✅ name (3,1,0x411): " + "、".join(msgs)
    return None


def fix_mac_japanese_name(font):
    """
    (1,1,0xb) Mac Japanese の nameID=1,2,4 を (3,1,0x411) から同期。
    存在しない場合は追加、値が異なる場合は更新する。
    """
    name_table = font["name"]

    # (3,1,0x411) nameID=1 が存在しない場合はスキップ
    src1 = name_table.getName(1, 3, 1, 0x411)
    if src1 is None:
        return None

    msgs = []

    def sync(name_id, value):
        dst = name_table.getName(name_id, 1, 1, 0xb)
        if dst is None:
            name_table.setName(value, name_id, 1, 1, 0xb)
            msgs.append(f"nameID={name_id} 追加")
        elif dst.toUnicode() != value:
            name_table.setName(value, name_id, 1, 1, 0xb)
            msgs.append(f"nameID={name_id} 更新")

    full_name = src1.toUnicode()

    # nameID=1: (3,1,0x411) nameID=1（再構築済み）から同期
    sync(1, full_name)

    # nameID=2: (3,1,0x411) nameID=2 から同期
    src2 = name_table.getName(2, 3, 1, 0x411)
    if src2:
        sync(2, src2.toUnicode())

    # nameID=4: nameID=1 と同値（日本語フルネーム）
    sync(4, full_name)

    if msgs:
        return "✅ name (1,1,0xb) Mac Japanese: " + "、".join(msgs)
    return "ℹ️ name (1,1,0xb) Mac Japanese: 修正不要"


def set_meta_dlng(font):
    """meta テーブルの dlng タグに ja を設定。なければ meta テーブルを新規作成"""
    if "meta" not in font:
        from fontTools.ttLib.tables import _m_e_t_a
        meta = _m_e_t_a.table__m_e_t_a()
        meta.data = {}
        font["meta"] = meta

    meta = font["meta"]
    current = meta.data.get("dlng", "")
    if isinstance(current, bytes):
        current = current.decode("utf-8")

    langs = [l.strip() for l in current.split(",") if l.strip()] if current else []
    if "ja" in langs:
        return "ℹ️ meta dlng: ja はすでに設定済みです"

    langs.append("ja")
    new_value = ",".join(langs)
    meta.data["dlng"] = new_value
    return f"✅ meta dlng: {current!r} → {new_value!r}"


def set_win_metrics(font):
    """OS/2.usWinAscent/WinDescent を head.yMax/yMin から設定"""
    if "fvar" in font:
        return "ℹ️ WinMetrics: バリアブルフォントのためスキップ"

    y_max = font["head"].yMax
    y_min = font["head"].yMin
    old_ascent  = font["OS/2"].usWinAscent
    old_descent = font["OS/2"].usWinDescent

    font["OS/2"].usWinAscent  = y_max
    font["OS/2"].usWinDescent = -y_min

    return (
        f"✅ WinAscent : {old_ascent} → {y_max}\n"
        f"   WinDescent: {old_descent} → {-y_min}"
    )


# ============================================================
# メイン
# ============================================================

font_paths = select_font_files()
if not font_paths:
    Message("", "ファイルが選択されませんでした", OKButton="終了")
else:
    results = []
    for font_path in font_paths:
        font = TTFont(font_path)

        if "vmtx" not in font:
            results.append(f"❌ {os.path.basename(font_path)}\nvmtxがないので日本語フォントではありません")
            continue

        cmap_result      = add_mac_japanese_cmap(font)
        sjis_result      = remove_windows_sjis_cmap(font)
        range_result     = set_code_page_range(font)
        name_added       = add_mac_name_records(font)
        win_name_result  = fix_win_japanese_name(font)
        mac_name_result  = fix_mac_japanese_name(font)
        meta_result      = set_meta_dlng(font)
        metrics_result   = set_win_metrics(font)

        font.save(font_path)

        name_result = (
            f"✅ Mac nameレコード: {name_added} 件追加"
            if name_added > 0
            else "ℹ️ Mac nameレコード: すでに存在します"
        )

        entry_lines = [os.path.basename(font_path)]
        entry_lines.append(cmap_result)
        if sjis_result:
            entry_lines.append(sjis_result)
        entry_lines.append(range_result)
        entry_lines.append(name_result)
        if win_name_result:
            entry_lines.append(win_name_result)
        if mac_name_result:
            entry_lines.append(mac_name_result)
        entry_lines.append(meta_result)
        entry_lines.append(metrics_result)

        results.append("\n".join(entry_lines))

    Message("", "\n\n---\n\n".join(results), OKButton="OK")
