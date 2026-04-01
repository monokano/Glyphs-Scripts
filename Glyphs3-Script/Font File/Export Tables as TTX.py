#MenuTitle: Export Tables as TTX

# -*- coding: utf-8 -*-
__doc__="""
フォントファイルの各テーブルをTTXファイルとして
フォントファイルと同じフォルダに出力します。
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
    panel.setMessage_("テーブルをTTXとして出力するフォントファイルを選んでください")
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
    font      = TTFont(font_path)
    font_dir  = os.path.dirname(font_path)
    font_name = os.path.splitext(os.path.basename(font_path))[0]

    # 出力フォルダ: フォントファイルと同階層に「フォント名_ttx」フォルダを作成
    output_dir = os.path.join(font_dir, f"{font_name}_ttx")
    os.makedirs(output_dir, exist_ok=True)

    tables = font.keys()
    failed = []

    for table_tag in tables:
        # ファイル名に使えない文字（スラッシュ等）を除去
        safe_tag = table_tag.strip().replace("/", "_")
        output_path = os.path.join(output_dir, f"{font_name}_{safe_tag}.ttx")
        try:
            font.saveXML(output_path, tables=[table_tag])
        except Exception as e:
            failed.append(f"{table_tag}: {e}")

    result_text = (
        f"✅\n\nTTXファイルを出力しました。\n\n"
        f"{os.path.basename(font_path)}\n"
        f"{len(tables) - len(failed)} / {len(tables)} テーブル\n\n"
        f"出力先:\n{output_dir}"
    )
    if failed:
        result_text += "\n\n❌ 失敗:\n" + "\n".join(failed)

    Message("", result_text, OKButton="OK")