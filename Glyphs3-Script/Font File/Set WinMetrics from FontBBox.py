#MenuTitle: Set WinMetrics from FontBBox

# -*- coding: utf-8 -*-
__doc__="""
OS/2.usWinAscent/usWinDescentをhead.yMax/yMinの値に合わせて設定します。
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


def select_font_files():
    panel = NSOpenPanel.openPanel()
    panel.setTitle_("フォントファイルを選択")
    panel.setMessage_("WinAscent/WinDescentを設定するフォントファイルを選んでください")
    panel.setAllowedFileTypes_(["otf", "ttf"])
    panel.setAllowsMultipleSelection_(True)
    panel.setCanChooseDirectories_(False)
    if panel.runModal() == 1:
        return [url.path() for url in panel.URLs()]
    return []


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

        if "fvar" in font:
            results.append(f"❌ {os.path.basename(font_path)}\nバリアブルフォントには対応していません")
            continue

        y_max = font["head"].yMax
        y_min = font["head"].yMin

        old_ascent  = font["OS/2"].usWinAscent
        old_descent = font["OS/2"].usWinDescent

        font["OS/2"].usWinAscent  = y_max
        font["OS/2"].usWinDescent = -y_min

        font.save(font_path)

        entry = (
            f"{os.path.basename(font_path)}\n"
            f"WinAscent  : {old_ascent} → {y_max}\n"
            f"WinDescent : {old_descent} → {-y_min}"
        )
        results.append(entry)

    Message("", "✅ WinAscent/WinDescentを更新しました。\n\n" + "\n\n---\n\n".join(results), OKButton="OK")