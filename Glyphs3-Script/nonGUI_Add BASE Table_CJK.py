#MenuTitle: フォントファイル：BASEテーブルを追加（CJK用）

# -*- coding: utf-8 -*-
__doc__="""
CJKフォントファイルにBASEテーブルを追加します。
平均字面の1辺のサイズの入力が必要です。その他は自動算出。
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

from fontTools.ttLib import TTFont, newTable
import fontTools.ttLib.tables.otTables as otTables
from AppKit import NSOpenPanel, NSAlert, NSTextField, NSMakeRect

CJK_SCRIPTS   = ["DFLT", "hani", "kana"]
LATIN_SCRIPTS = ["cyrl", "grek", "latn"]


def select_font_file():
    panel = NSOpenPanel.openPanel()
    panel.setTitle_("CJKフォントファイルを選択")
    panel.setMessage_("BASEテーブルを追加するCJKフォントファイルを選んでください")
    panel.setAllowedFileTypes_(["otf", "ttf"])
    panel.setAllowsMultipleSelection_(False)
    panel.setCanChooseDirectories_(False)
    if panel.runModal() == 1:
        return panel.URL().path()
    return None


def ask_em_size(default):
    """仮想ボディ横幅入力ダイアログ。キャンセル時は None を返す"""
    alert = NSAlert.alloc().init()
    alert.setMessageText_("仮想ボディの横幅を入力")
    alert.setInformativeText_("仮想ボディの横幅（unit）を\n入力してください。")
    alert.addButtonWithTitle_("OK")
    alert.addButtonWithTitle_("キャンセル")

    field = NSTextField.alloc().initWithFrame_(NSMakeRect(0, 0, 200, 24))
    field.setStringValue_(str(default))
    alert.setAccessoryView_(field)
    alert.window().setInitialFirstResponder_(field)

    response = alert.runModal()
    if response == 1000:
        try:
            value = int(field.stringValue())
            if value > 0:
                return value
        except ValueError:
            pass
    return None


def ask_icf_size(default=880):
    """字面サイズ入力ダイアログ。キャンセル時は None を返す"""
    alert = NSAlert.alloc().init()
    alert.setMessageText_("字面サイズ（ICF）を入力")
    alert.setInformativeText_("平均字面の1辺のサイズ（unit）を\n入力してください。")
    alert.addButtonWithTitle_("OK")
    alert.addButtonWithTitle_("キャンセル")

    field = NSTextField.alloc().initWithFrame_(NSMakeRect(0, 0, 200, 24))
    field.setStringValue_(str(default))
    alert.setAccessoryView_(field)
    alert.window().setInitialFirstResponder_(field)

    response = alert.runModal()
    if response == 1000:  # NSAlertFirstButtonReturn
        try:
            value = int(field.stringValue())
            if value > 0:
                return value
        except ValueError:
            pass
    return None


def derive_coords(font, icf_size, em_size):
    upm            = font["head"].unitsPerEm
    typo_descender = font["OS/2"].sTypoDescender  # negative value

    margin = (em_size - icf_size) / 2      # 左右の余白（天地にも共通適用）

    icf_size_h = upm - margin * 2          # HorizAxis での ICF 高さ（天地方向）

    center_h = typo_descender + upm / 2    # em center (HorizAxis)
    center_v = em_size / 2                 # em center (VertAxis)

    horiz_coords = {
        "icfb": round(center_h - icf_size_h / 2),
        "icft": round(center_h + icf_size_h / 2),
        "ideo": typo_descender,
        "idtp": typo_descender + upm,
        "romn": 0,
    }
    vert_coords = {
        "icfb": round(center_v - icf_size / 2),
        "icft": round(center_v + icf_size / 2),
        "ideo": 0,
        "idtp": em_size,
        "romn": -typo_descender,
    }
    return horiz_coords, vert_coords


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


def make_axis(coord_dict, cjk_default_tag, latin_default_tag):
    tags, coords = make_base_coords(coord_dict)

    tag_list              = otTables.BaseTagList()
    tag_list.BaselineTag  = tags
    tag_list.BaseTagCount = len(tags)

    bv_cjk   = make_base_values(tags, coords, cjk_default_tag)
    bv_latin = make_base_values(tags, coords, latin_default_tag)

    all_scripts = (
        [(s, bv_cjk)   for s in CJK_SCRIPTS] +
        [(s, bv_latin) for s in LATIN_SCRIPTS]
    )
    all_scripts.sort(key=lambda x: x[0])

    records = []
    for script_tag, bv in all_scripts:
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


def add_base_table(font, horiz_coords, vert_coords):
    base         = otTables.BASE()
    base.Version = 0x00010000
    base.HorizAxis = make_axis(horiz_coords,
                               cjk_default_tag="ideo",
                               latin_default_tag="romn")
    base.VertAxis  = make_axis(vert_coords,
                               cjk_default_tag="ideo",
                               latin_default_tag="romn")

    wrapper       = newTable("BASE")
    wrapper.table = base
    font["BASE"]  = wrapper


# ============================================================
# メイン
# ============================================================

font_path = select_font_file()
if not font_path:
    Message("", "ファイルが選択されませんでした", OKButton="終了")
else:
    font      = TTFont(font_path)

    if "fvar" in font:
        Message("", "❌\n\nバリアブルフォントには\n対応していません。\n\n" + os.path.basename(font_path), OKButton="終了")
    elif "vmtx" not in font:
        Message("", "❌\n\nこのフォントはvmtxがないので\nCJKフォントではありません。\n\n" + os.path.basename(font_path), OKButton="終了")
    else:
        upm       = font["head"].unitsPerEm
        typo_desc = font["OS/2"].sTypoDescender

        em_size = ask_em_size(default=upm)
        if em_size is None:
            Message("", "キャンセルされました", OKButton="終了")
        else:
            icf_size = ask_icf_size(default=round(em_size * 0.92))
            if icf_size is None:
                Message("", "キャンセルされました", OKButton="終了")
            else:
                horiz_coords, vert_coords = derive_coords(font, icf_size, em_size)

                status = "⚠️\n\n既存の BASE テーブルを\n上書きしました" if "BASE" in font else "✅\n\nBASE テーブルを\n新規追加しました"

                add_base_table(font, horiz_coords, vert_coords)
                font.save(font_path)

                result_text = (
                    f"{status}\n\n"
                    f"{os.path.basename(font_path)}"
                )
                Message("", result_text, OKButton="OK")