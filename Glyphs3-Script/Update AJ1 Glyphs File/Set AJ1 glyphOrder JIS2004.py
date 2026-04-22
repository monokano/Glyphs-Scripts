#MenuTitle: Set AJ1 glyphOrder JIS2004
# -*- coding: utf-8 -*-
__doc__ = """
Adobe-Japan1用のglyphOrderを設定します。
JIS2004対応は常に有効です。
MapFileAdobe-Japan1.txt は Glyphs バンドル内から取得します。
"""

import os
import re
from AppKit import (
    NSAlert, NSPopUpButton, NSTextField, NSView, NSMakeRect,
    NSAlertFirstButtonReturn,
)
from Foundation import NSBundle


# Supplement ごとの CID 範囲（Adobe-Japan1 仕様に基づく固定値）
SUPPLEMENT_RANGES = [
    ("AJ1-0",  0,     8283),
    ("AJ1-1",  8284,  8358),
    ("AJ1-2",  8359,  8719),
    ("AJ1-3",  8720,  9353),
    ("AJ1-4",  9354,  15443),
    ("AJ1-5",  15444, 20316),
    ("AJ1-6",  20317, 23057),
    ("AJ1-7",  23058, 23059),
]

POPUP_ITEMS = ["AJ1-3", "AJ1-4", "AJ1-5", "AJ1-6 (1-7)"]

# 各選択肢に含まれる base supplement の順序
BASE_SUPS = {
    "AJ1-3":       ["AJ1-0", "AJ1-1", "AJ1-2", "AJ1-3"],
    "AJ1-4":       ["AJ1-0", "AJ1-1", "AJ1-2", "AJ1-3", "AJ1-4"],
    "AJ1-5":       ["AJ1-0", "AJ1-1", "AJ1-2", "AJ1-3", "AJ1-4", "AJ1-5"],
    "AJ1-6 (1-7)": ["AJ1-0", "AJ1-1", "AJ1-2", "AJ1-3", "AJ1-4", "AJ1-5", "AJ1-6", "AJ1-7"],
}

# JIS2004 追加 CID データ（スクリプト内に埋め込み）
JIS2004_DATA = {
    "AJ1-3": """\
**AJ1-4**
9354
9779
12101
12870
13320-13327
13330
13332-13333
13335-13341
13343
13345-13355
13358-13369
13371
13373-13382
13385-13388
13391-13400
13402
13460
13495
13538
13624
13650
13673
13731
13803
13860
13893
13915
13949
13964
14013
14066
14074
14111
14116
14196
14272
14290
**AJ1-5**
16977
17041
18760
19312
19346
20175
20222
20263-20296
20301-20305
20307
20314
**AJ1-6**
21072-21074
**AJ1-7**
23058
""",
    "AJ1-4": """\
**AJ1-5**
16413
16444-16449
16467-16468
16889
16905
16977
17014
17041
17168
17205
18759-18760
19061
19312
19346
20175
20222
20263-20296
20299-20310
20312-20315
**AJ1-6**
21071-21074
21558
21933
22010
22920
**AJ1-7**
23058
23059
""",
    "AJ1-5": """\
**AJ1-6**
21071-21074
21371
21558
21722
21933
22010
22920
**AJ1-7**
23058
23059
""",
}


def load_cid_nicename_map():
    """Glyphs バンドル内の MapFileAdobe-Japan1.txt から CID → nicename マッピングを構築"""
    map_file = os.path.join(
        NSBundle.mainBundle().bundlePath(),
        "Contents/Frameworks/GlyphsCore.framework/Versions/A/Resources/MapFileAdobe-Japan1.txt"
    )
    if not os.path.exists(map_file):
        Message(f"MapFileAdobe-Japan1.txt が見つかりません:\n{map_file}", title="エラー")
        return None

    cid_map = {}
    with open(map_file, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                try:
                    cid_map[int(parts[0])] = parts[1]
                except ValueError:
                    pass
    return cid_map


def parse_cid_list_text(text):
    """追加 CID テキストを解析して (section_order, {section: [cids]}) を返す"""
    sections = {}
    section_order = []
    current = None

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        m = re.match(r"\*\*AJ1?-(\d+)\*\*", line)
        if m:
            current = f"AJ1-{m.group(1)}"
            if current not in sections:
                sections[current] = []
                section_order.append(current)
            continue

        if current is None:
            continue

        m = re.match(r"^(\d+)-(\d+)$", line)
        if m:
            sections[current].extend(range(int(m.group(1)), int(m.group(2)) + 1))
        elif re.match(r"^\d+$", line):
            sections[current].append(int(line))

    return section_order, sections


def build_glyph_order(selection, cid_map):
    """glyphOrder リストを構築する（常に JIS2004 対応）"""
    sup_map = {name: (start, end) for name, start, end in SUPPLEMENT_RANGES}
    order = []

    for sup in BASE_SUPS[selection]:
        order.append(f"**{sup}**")
        start, end = sup_map[sup]
        for cid in range(start, end + 1):
            if cid in cid_map:
                order.append(cid_map[cid])

    if selection in JIS2004_DATA:
        section_order, additional = parse_cid_list_text(JIS2004_DATA[selection])
        for sec in section_order:
            cids = additional[sec]
            if not cids:
                continue
            order.append(f"**{sec}**")
            for cid in cids:
                if cid in cid_map:
                    order.append(cid_map[cid])

    return order


def show_dialog():
    """NSAlert でレベル選択ダイアログを表示し、選択結果を返す。キャンセル時は None。"""
    # アクセサリビュー: ラベル + ポップアップ
    accessory = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, 260, 28))

    label = NSTextField.alloc().initWithFrame_(NSMakeRect(0, 5, 56, 18))
    label.setStringValue_("レベル:")
    label.setBezeled_(False)
    label.setDrawsBackground_(False)
    label.setEditable_(False)
    label.setSelectable_(False)

    popup = NSPopUpButton.alloc().initWithFrame_(NSMakeRect(62, 0, 198, 28))
    for item in POPUP_ITEMS:
        popup.addItemWithTitle_(item)

    accessory.addSubview_(label)
    accessory.addSubview_(popup)

    alert = NSAlert.alloc().init()
    alert.setMessageText_("AJ1 glyphOrder を設定")
    alert.setInformativeText_("レベルを選択して「実行」をクリックしてください。\n（JIS2004対応は常に有効）")
    alert.addButtonWithTitle_("実行")
    alert.addButtonWithTitle_("キャンセル")
    alert.setAccessoryView_(accessory)
    alert.window().setInitialFirstResponder_(popup)

    response = alert.runModal()
    if response != NSAlertFirstButtonReturn:
        return None

    return POPUP_ITEMS[popup.indexOfSelectedItem()]


def main():
    font = Glyphs.font
    if not font:
        Message("フォントが開かれていません。", title="エラー")
        return

    selection = show_dialog()
    if selection is None:
        return

    cid_map = load_cid_nicename_map()
    if cid_map is None:
        return

    order = build_glyph_order(selection, cid_map)
    font.customParameters["glyphOrder"] = order

    Message(
        f"glyphOrder を設定しました。\n"
        f"レベル: {selection} + JIS2004\n"
        f"エントリ数: {len(order)}",
        title="処理完了"
    )


main()
