#MenuTitle: フォントファイル：BASEテーブルを追加（非CJK用）

# -*- coding: utf-8 -*-
__doc__="""
非CJKフォントファイルにBASEテーブルを追加します。
ideo/romn のみ。値はOS/2.capHeightから自動算出。
PythonモジュールのFontToolsのインストールが必要です。
"""

import sys
import os

fonttools_lib = os.path.expanduser(
    "~/Library/Application Support/Glyphs 3/Repositories/fonttools/Lib"
)
if fonttools_lib not in sys.path:
    sys.path.insert(0, fonttools_lib)

from fontTools.ttLib import TTFont, newTable
import fontTools.ttLib.tables.otTables as otTables
from AppKit import NSOpenPanel

# 非CJK用スクリプト（DFLT + latn のみ、両方 romn がデフォルト）
SCRIPTS = ["DFLT", "latn"]


def select_font_file():
    panel = NSOpenPanel.openPanel()
    panel.setTitle_("非CJKフォントファイルを選択")
    panel.setMessage_("BASEテーブルを追加する非CJKフォントファイルを選んでください")
    panel.setAllowedFileTypes_(["otf", "ttf"])
    panel.setAllowsMultipleSelection_(False)
    panel.setCanChooseDirectories_(False)
    if panel.runModal() == 1:
        return panel.URL().path()
    return None


def derive_coords(font):
    upm        = font["head"].unitsPerEm
    cap_height = font["OS/2"].sCapHeight

    # 矩形ボディの天地中央にcapHeightが来るように
    ideo = -round((upm - cap_height) / 2)

    horiz_coords = {
        "ideo": ideo,
        "romn": 0,
    }
    return horiz_coords


def make_base_coords(coord_dict):
    tags   = sorted(coord_dict.keys())
    coords = []
    for tag in tags:
        coord            = otTables.BaseCoord()
        coord.Format     = 1
        coord.Coordinate = coord_dict[tag]
        coords.append(coord)
    return tags, coords


def make_base_values(tags, coords, default_tag):
    bv                = otTables.BaseValues()
    bv.DefaultIndex   = tags.index(default_tag)
    bv.BaseCoord      = coords
    bv.BaseCoordCount = len(coords)
    return bv


def make_horiz_axis(coord_dict):
    tags, coords = make_base_coords(coord_dict)

    tag_list              = otTables.BaseTagList()
    tag_list.BaselineTag  = tags
    tag_list.BaseTagCount = len(tags)

    # 全スクリプト共通・romn がデフォルト
    bv = make_base_values(tags, coords, "romn")

    records = []
    for script_tag in sorted(SCRIPTS):
        bs                  = otTables.BaseScript()
        bs.BaseValues       = bv
        bs.DefaultMinMax    = None
        bs.BaseLangSysCount = 0
        bs.BaseLangSys      = []

        rec               = otTables.BaseScriptRecord()
        rec.BaseScriptTag = script_tag
        rec.BaseScript    = bs
        records.append(rec)

    bsl                   = otTables.BaseScriptList()
    bsl.BaseScriptRecord  = records
    bsl.BaseScriptCount   = len(records)

    axis                = otTables.Axis()
    axis.BaseTagList    = tag_list
    axis.BaseScriptList = bsl
    return axis


def add_base_table(font, horiz_coords):
    base            = otTables.BASE()
    base.Version    = 0x00010000
    base.HorizAxis  = make_horiz_axis(horiz_coords)
    base.VertAxis   = None

    wrapper         = newTable("BASE")
    wrapper.table   = base
    font["BASE"]    = wrapper


# ============================================================
# メイン
# ============================================================

font_path = select_font_file()
if not font_path:
    Message("", "ファイルが選択されませんでした", OKButton="終了")
else:
    font = TTFont(font_path)

    if "fvar" in font:
        Message("", "❌\n\nバリアブルフォントには\n対応していません。\n\n" + os.path.basename(font_path), OKButton="終了")
    elif "vmtx" in font:
        Message("", "❌\n\nこのフォントはvmtxがある\nCJKフォントです。\n\nこのスクリプトは\n非CJKフォント用です。\n\n" + os.path.basename(font_path), OKButton="終了")
    else:
        upm        = font["head"].unitsPerEm
        cap_height = font["OS/2"].sCapHeight
        horiz_coords = derive_coords(font)

        status = "⚠️\n\n既存の BASE テーブルを\n上書きしました" if "BASE" in font else "✅\n\nBASE テーブルを\n新規追加しました"

        add_base_table(font, horiz_coords)
        font.save(font_path)

        result_text = (
            f"{status}\n\n"
            f"{os.path.basename(font_path)}\n"
        )
        Message("", result_text, OKButton="OK")
        