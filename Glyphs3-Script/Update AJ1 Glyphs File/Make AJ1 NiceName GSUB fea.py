#MenuTitle: Make AJ1 NiceName GSUB fea

# -*- coding: utf-8 -*-
__doc__="""
Adobe-Japan1のGSUBファイルをGitHubから取得し、CID参照（\\N）をnicenameに変換して保存します。

【取得元】
https://github.com/adobe-type-tools/Adobe-Japan1/tree/master/GSUB

CID→nicenameの変換には、実行中のGlyphsアプリ内のMapFileAdobe-Japan1.txtを使用します。
"""

import os
import re
import ssl
import json
import urllib.request
from AppKit import (
    NSAlert, NSPopUpButton, NSMakeRect, NSSavePanel
)
from Foundation import NSBundle

GSUB_API_URL = (
    "https://api.github.com/repos/adobe-type-tools/Adobe-Japan1/contents/GSUB"
)


def fetch_url(url):
    """URLからコンテンツを取得"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "GlyphsScript"})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
        return response.read().decode("utf-8")


def list_gsub_files():
    """GitHubのGSUBディレクトリから.feaファイルの一覧を取得"""
    data = json.loads(fetch_url(GSUB_API_URL))
    files = [
        (item["name"], item["download_url"])
        for item in data
        if item["name"].endswith(".fea")
    ]
    files.sort()
    return files


def get_glyphs_version():
    """Glyphsのバージョンとビルド番号を "3.4.1 (3436)" 形式で取得"""
    info = NSBundle.mainBundle().infoDictionary()
    version = info.get("CFBundleShortVersionString", "?")
    build = info.get("CFBundleVersion", "?")
    return f"{version} ({build})"


def load_cid_name_map():
    """MapFileAdobe-Japan1.txtからCID→グリフ名マッピングを読み込む"""
    map_path = os.path.join(
        NSBundle.mainBundle().bundlePath(),
        "Contents/Frameworks/GlyphsCore.framework/Versions/A/Resources/"
        "MapFileAdobe-Japan1.txt"
    )
    cid_to_name = {}
    with open(map_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    cid_to_name[int(parts[0])] = parts[1]
                except ValueError:
                    continue
    return cid_to_name


def choose_from_list(title, message, options):
    """NSAlert + NSPopUpButtonで選択肢から選ばせる"""
    alert = NSAlert.alloc().init()
    alert.setMessageText_(title)
    alert.setInformativeText_(message)
    alert.addButtonWithTitle_("OK")
    alert.addButtonWithTitle_("キャンセル")

    popup = NSPopUpButton.alloc().initWithFrame_(NSMakeRect(0, 0, 360, 26))
    for option in options:
        popup.addItemWithTitle_(option)
    alert.setAccessoryView_(popup)

    response = alert.runModal()
    if response == 1000:  # NSAlertFirstButtonReturn
        return popup.indexOfSelectedItem()
    return None


def translate_fea_cid_to_name(fea_source, cid_to_name):
    """feaソース内の \\N CID参照をグリフ名に変換"""
    missing = set()

    def replace_cid(m):
        n = int(m.group(1))
        if n in cid_to_name:
            return cid_to_name[n]
        missing.add(n)
        return m.group(0)

    translated = re.sub(r'\\(\d+)', replace_cid, fea_source)
    return translated, missing


def save_fea_file(default_name, content):
    """保存ダイアログを表示してfeaファイルを保存"""
    panel = NSSavePanel.savePanel()
    panel.setTitle_("変換後のfeaファイルを保存")
    panel.setNameFieldStringValue_(default_name)
    panel.setAllowedFileTypes_(["fea"])
    if panel.runModal() != 1:
        return None
    path = panel.URL().path()
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def main():
    # GSUBファイル一覧を取得
    try:
        files = list_gsub_files()
    except Exception as e:
        Message("", f"GSUBファイル一覧の取得に失敗しました:\n{e}", OKButton="終了")
        return

    if not files:
        Message("", "GSUBファイルが見つかりませんでした", OKButton="終了")
        return

    # 一覧から選択
    names = [name for name, url in files]
    idx = choose_from_list(
        "AJ1 GSUB選択",
        "CID→グリフ名に変換するGSUB .feaファイルを選んでください",
        names
    )
    if idx is None:
        return
    selected_name, selected_url = files[idx]

    # feaファイルを取得
    try:
        fea_source = fetch_url(selected_url)
    except Exception as e:
        Message("", f"feaファイルの取得に失敗しました:\n{e}", OKButton="終了")
        return

    # CID→グリフ名マッピングを読み込む
    try:
        cid_to_name = load_cid_name_map()
    except Exception as e:
        Message(
            "",
            f"MapFileAdobe-Japan1.txtの読み込みに失敗しました:\n{e}",
            OKButton="終了"
        )
        return

    # CID → グリフ名に変換
    translated, missing = translate_fea_cid_to_name(fea_source, cid_to_name)

    # 変換情報をヘッダとして付加
    header = f"# Converted with Glyphs {get_glyphs_version()}\n\n"
    translated = header + translated

    # 保存
    base, ext = os.path.splitext(selected_name)
    default_name = f"{base}-nicename{ext}"
    saved_path = save_fea_file(default_name, translated)
    if saved_path is None:
        return

    # 結果表示
    msg = f"✅ 変換完了\n保存先: {saved_path}"
    if missing:
        missing_sorted = sorted(missing)[:10]
        msg += f"\n\n⚠️ マッピングが見つからないCID: {len(missing)} 件"
        msg += f"\n例: {', '.join(str(n) for n in missing_sorted)}"
    Message("", msg, OKButton="OK")


# ============================================================
# メイン
# ============================================================

main()
