#MenuTitle: Set WinMetrics from FontBBox

# -*- coding: utf-8 -*-
__doc__="""
OS/2.WinAscentをhead.FontBBox.yMaxに、
OS/2.WinDescentをhead.FontBBox.yMinの絶対値に設定します。
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
from AppKit import NSOpenPanel


def select_font_file():
    panel = NSOpenPanel.openPanel()
    panel.setTitle_("フォントファイルを選択")
    panel.setMessage_("WinAscent/WinDescentを設定するフォントファイルを選んでください")
    panel.setAllowedFileTypes_(["otf", "ttf"])
    panel.setAllowsMultipleSelection_(False)
    panel.setCanChooseDirectories_(False)
    if panel.runModal() == 1:
        return panel.URL().path()
    return None


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
    else:
        y_max = font["head"].yMax
        y_min = font["head"].yMin

        old_ascent  = font["OS/2"].usWinAscent
        old_descent = font["OS/2"].usWinDescent

        font["OS/2"].usWinAscent  = y_max
        font["OS/2"].usWinDescent = -y_min   # usWinDescent は正の値

        font.save(font_path)

        result_text = (
            f"✅\n\nWinAscent/WinDescentを更新しました。\n\n"
            f"{os.path.basename(font_path)}\n\n"
            f"WinAscent  : {old_ascent} → {y_max}\n"
            f"WinDescent : {old_descent} → {-y_min}"
        )
        Message("", result_text, OKButton="OK")