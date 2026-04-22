#MenuTitle: Check AJ1 NiceName Diff
# -*- coding: utf-8 -*-
__doc__="""
旧バージョンと現バージョンの Glyphs.app から MapFileAdobe-Japan1.txt を読み込み、
Adobe-Japan1 nicename の変更差分をタブ区切りテキストファイルとして保存します。

【使い方】
1. 本スクリプトを実行
2. ダイアログで旧バージョンの Glyphs.app を選択
3. 検出された変更一覧を確認して保存

【出力フォーマット】
旧 nicename<TAB>新 nicename（1 行 1 件）
"""

import os
import plistlib
from AppKit import (
    NSAlert, NSBundle, NSOpenPanel, NSSavePanel, NSURL,
    NSFileHandlingPanelOKButton
)

# バージョン3以降のパス → バージョン2のパスの順で検索
MAP_FILE_CANDIDATES = [
    "Contents/Frameworks/GlyphsCore.framework/Versions/A/Resources/"
    "MapFileAdobe-Japan1.txt",
    "Contents/PlugIns/OTF.glyphsFileFormat/Contents/Resources/"
    "MapFileAdobe-Japan1.txt",
]


def find_map_file(app_path):
    """MapFileAdobe-Japan1.txt のパスを候補順に探して返す。見つからなければ None"""
    for rel in MAP_FILE_CANDIDATES:
        path = os.path.join(app_path, rel)
        if os.path.isfile(path):
            return path
    return None


def load_cid_name_map(app_path):
    """MapFileAdobe-Japan1.txt から CID → グリフ名マッピングを読み込む"""
    map_path = find_map_file(app_path)
    if map_path is None:
        raise FileNotFoundError(
            f"MapFileAdobe-Japan1.txt が見つかりません:\n{app_path}"
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


def get_current_glyphs_app_path():
    """現在実行中の Glyphs.app バンドルパスを取得"""
    return NSBundle.mainBundle().bundlePath()


def get_glyphs_app_version(app_path):
    """Info.plist からバージョン文字列を "3.3.1 (3343)" 形式で取得"""
    plist_path = os.path.join(app_path, "Contents/Info.plist")
    try:
        with open(plist_path, "rb") as f:
            info = plistlib.load(f)
        short = info.get("CFBundleShortVersionString", "")
        build = info.get("CFBundleVersion", "")
        if short and build:
            return f"{short} ({build})"
        return short or build or ""
    except Exception:
        return ""


def select_old_glyphs_app():
    """旧バージョンの Glyphs.app を NSOpenPanel で選択させる"""
    panel = NSOpenPanel.openPanel()
    panel.setTitle_("旧バージョンの Glyphs.app を選択")
    panel.setMessage_("nicename 変更前の Glyphs.app を選択してください")
    panel.setAllowedFileTypes_(["app"])
    panel.setAllowsMultipleSelection_(False)
    panel.setCanChooseFiles_(True)
    panel.setCanChooseDirectories_(False)
    panel.setDirectoryURL_(NSURL.fileURLWithPath_("/Applications"))
    if panel.runModal() != NSFileHandlingPanelOKButton:
        return None
    return panel.URL().path()


def build_name_change_map(old_cid_map, new_cid_map):
    """同一 CID で名前が変わったものを検出して {旧名: 新名} を返す"""
    changes = {}
    for cid, new_name in new_cid_map.items():
        if cid in old_cid_map:
            old_name = old_cid_map[cid]
            if old_name != new_name:
                changes[old_name] = new_name
    return changes


def save_diff_file(changes, old_app_path, new_app_path):
    """差分をタブ区切りテキストファイルに保存。保存成功なら True を返す"""
    panel = NSSavePanel.savePanel()
    panel.setTitle_("nicename 差分を保存")
    panel.setNameFieldStringValue_("nicename-changes.txt")
    panel.setAllowedFileTypes_(["txt"])
    if panel.runModal() != NSFileHandlingPanelOKButton:
        return False

    old_version = get_glyphs_app_version(old_app_path)
    new_version = get_glyphs_app_version(new_app_path)
    old_label = old_app_path + (f"  [{old_version}]" if old_version else "")
    new_label = new_app_path + (f"  [{new_version}]" if new_version else "")

    lines = [
        "# nicename 変更リスト",
        f"# 旧: {old_label}",
        f"# 新: {new_label}",
        f"# 変更件数: {len(changes)} 件",
        "",
        "旧 nicename\t新 nicename",
    ] + [f"{old}\t{new}" for old, new in sorted(changes.items())]

    path = panel.URL().path()
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return True


def main():
    # ① 現在の Glyphs.app パスを先に取得（ダイアログ表示前）
    try:
        new_app_path = get_current_glyphs_app_path()
    except Exception as e:
        Message("", f"現バージョンの Glyphs.app パスの取得に失敗しました:\n{e}", OKButton="終了")
        return

    # ② 旧 Glyphs.app を選択
    old_app_path = select_old_glyphs_app()
    if not old_app_path:
        return

    if old_app_path == new_app_path:
        Message("", "選択された Glyphs.app は現在実行中のものと同じです。\n旧バージョンを選択してください。", OKButton="終了")
        return

    # ③ 旧 MapFile を読み込む
    try:
        old_map = load_cid_name_map(old_app_path)
    except Exception as e:
        Message("", f"旧 MapFileAdobe-Japan1.txt の読み込みに失敗しました:\n{e}", OKButton="終了")
        return

    # ④ 新 MapFile を読み込む
    try:
        new_map = load_cid_name_map(new_app_path)
    except Exception as e:
        Message("", f"新 MapFileAdobe-Japan1.txt の読み込みに失敗しました:\n{e}", OKButton="終了")
        return

    # ⑤ nicename の変更を検出
    name_changes = build_name_change_map(old_map, new_map)

    if not name_changes:
        Message("", "nicename に変更はありませんでした。", OKButton="OK")
        return

    # ⑥ 変更一覧をプレビュー表示して保存確認
    sorted_changes = sorted(name_changes.items())
    preview_lines = [f"  {old} → {new}" for old, new in sorted_changes[:20]]
    change_preview = "\n".join(preview_lines)
    if len(name_changes) > 20:
        change_preview += f"\n  … 他 {len(name_changes) - 20} 件"

    alert = NSAlert.alloc().init()
    alert.setMessageText_("nicename の変更を検出")
    alert.setInformativeText_(
        f"{len(name_changes)} 件の変更が見つかりました。\n\n"
        f"{change_preview}"
    )
    alert.addButtonWithTitle_("保存")
    alert.addButtonWithTitle_("キャンセル")
    if alert.runModal() != 1000:
        return

    # ⑦ ファイルに保存
    if save_diff_file(name_changes, old_app_path, new_app_path):
        Message("", f"保存しました（{len(name_changes)} 件）", OKButton="OK")


# ============================================================
# メイン
# ============================================================

main()
