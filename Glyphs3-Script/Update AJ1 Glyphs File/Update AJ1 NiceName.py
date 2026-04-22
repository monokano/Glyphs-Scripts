#MenuTitle: Update AJ1 NiceName
# -*- coding: utf-8 -*-
__doc__="""
旧バージョンと現バージョンの Glyphs.app から MapFileAdobe-Japan1.txt を読み込み、
Adobe-Japan1 nicename の変更を検出して、選択した Glyphs ファイルをテキストレベルで
一括置換し、新規ファイルとして保存します。

【使い方】
1. 本スクリプトを実行
2. ダイアログで旧バージョンの Glyphs.app を選択
3. 変更一覧を確認して「更新する」
4. 更新する .glyphs ファイルを選択（複数可）
5. 更新したファイルを同じ階層に保存
"""

import os
import re
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

# グリフ名に使われる文字（境界判定用のルックアヘッド・ルックビハインド）
_BOUNDARY_BEHIND = r'(?<![0-9a-zA-Z_.\-])'  # 直前がグリフ名文字でない
_BOUNDARY_AHEAD  = r'(?![0-9a-zA-Z_.\-])'   # 直後がグリフ名文字でない


# ============================================================
# MapFile
# ============================================================

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


def build_name_change_map(old_cid_map, new_cid_map):
    """同一 CID で名前が変わったものを検出して {旧名: 新名} を返す"""
    changes = {}
    for cid, new_name in new_cid_map.items():
        if cid in old_cid_map:
            old_name = old_cid_map[cid]
            if old_name != new_name:
                changes[old_name] = new_name
    return changes


# ============================================================
# アプリ情報
# ============================================================

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


# ============================================================
# ダイアログ
# ============================================================

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


def select_glyphs_files():
    """更新対象の .glyphs ファイルを NSOpenPanel で選択させる（複数可）"""
    panel = NSOpenPanel.openPanel()
    panel.setTitle_(".glyphs ファイルを選択")
    panel.setMessage_("nicename を更新する .glyphs ファイルを選択してください（複数可）")
    panel.setAllowedFileTypes_(["glyphs"])
    panel.setAllowsMultipleSelection_(True)
    panel.setCanChooseFiles_(True)
    panel.setCanChooseDirectories_(False)
    if panel.runModal() != NSFileHandlingPanelOKButton:
        return []
    return [url.path() for url in panel.URLs()]


# ============================================================
# テキスト置換
# ============================================================

def replace_name_in_text(text, old, new):
    """テキスト中のグリフ名 old を new に置換し、(新テキスト, 件数) を返す。
    グリフ名文字（英数字・ピリオド・ハイフン・アンダースコア）を境界として
    部分一致を回避する。"""
    pattern = re.compile(_BOUNDARY_BEHIND + re.escape(old) + _BOUNDARY_AHEAD)
    count = [0]

    def repl(m):
        count[0] += 1
        return new

    return pattern.sub(repl, text), count[0]


def apply_changes_to_text(text, name_changes):
    """依存関係を考慮した順序でグリフ名を置換し、(新テキスト, 置換件数) を返す。

    連鎖置換の防止:
    old_i → new_i を処理する際、new_i が別の old_j でもある場合は
    old_j → new_j を先に処理してから old_i → new_i を処理する。"""
    processed = set()
    total = 0

    for old, new in sorted(name_changes.items()):
        # new が別の old でもある場合は先にそちらを処理
        if new in name_changes and new not in processed:
            text, n = replace_name_in_text(text, new, name_changes[new])
            total += n
            processed.add(new)

        if old not in processed:
            text, n = replace_name_in_text(text, old, new)
            total += n
            processed.add(old)

    return text, total


# ============================================================
# 差分リスト保存
# ============================================================

def save_diff_file(changes, old_app_path, new_app_path):
    """変更差分をタブ区切りテキストファイルに保存。保存成功なら True を返す"""
    panel = NSSavePanel.savePanel()
    panel.setTitle_("nicename 差分リストを保存")
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


# ============================================================
# ファイル処理
# ============================================================

def update_glyphs_file(src_path, name_changes, new_version):
    """Glyphs ファイルをテキストとして読み込み、nicename を置換して
    {stem}-{new_version}.glyphs として同階層に保存する。
    戻り値: (保存パス, 置換件数)"""
    with open(src_path, "r", encoding="utf-8") as f:
        text = f.read()

    new_text, count = apply_changes_to_text(text, name_changes)

    stem = os.path.splitext(os.path.basename(src_path))[0]
    suffix = new_version if new_version else "updated"
    out_path = os.path.join(os.path.dirname(src_path), f"{stem}-{suffix}.glyphs")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(new_text)

    return out_path, count


# ============================================================
# メイン
# ============================================================

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

    # ⑥ 変更一覧をプレビュー表示して確認
    sorted_changes = sorted(name_changes.items())
    preview_lines = [f"  {old} → {new}" for old, new in sorted_changes[:20]]
    change_preview = "\n".join(preview_lines)
    if len(name_changes) > 20:
        change_preview += f"\n  … 他 {len(name_changes) - 20} 件"

    old_ver = get_glyphs_app_version(old_app_path)
    new_ver = get_glyphs_app_version(new_app_path)

    alert = NSAlert.alloc().init()
    alert.setMessageText_("nicename の変更を検出")
    alert.setInformativeText_(
        f"旧: {old_ver or old_app_path}\n"
        f"新: {new_ver or new_app_path}\n\n"
        f"{len(name_changes)} 件の変更が見つかりました。\n\n"
        f"{change_preview}\n\n"
        ".glyphs ファイルを選択して更新しますか？"
    )
    alert.addButtonWithTitle_("ファイルを選択")  # 1000
    alert.addButtonWithTitle_("リストを保存")    # 1001
    alert.addButtonWithTitle_("キャンセル")      # 1002

    while True:
        response = alert.runModal()
        if response == 1000:    # ファイルを選択
            break
        elif response == 1001:  # リストを保存（保存後にダイアログを再表示）
            save_diff_file(name_changes, old_app_path, new_app_path)
        else:                   # キャンセル
            return

    # ⑦ 更新する .glyphs ファイルを選択
    file_paths = select_glyphs_files()
    if not file_paths:
        return

    # ⑧ 各ファイルをテキストレベルで置換して保存
    results = []
    errors = []

    for src_path in file_paths:
        try:
            out_path, count = update_glyphs_file(src_path, name_changes, new_ver)
            results.append((os.path.basename(src_path), out_path, count))
        except Exception as e:
            errors.append(f"{os.path.basename(src_path)}: {e}")

    # ⑨ 結果を表示
    result_msg = f"完了（{len(results)} ファイル）\n\n"
    for src_name, out_path, count in results:
        result_msg += f"・{src_name}  →  {count} 件置換\n  {out_path}\n"
    if errors:
        result_msg += f"\n⚠️ エラー ({len(errors)} 件):\n" + "\n".join(errors)

    Message("", result_msg.strip(), OKButton="OK")


main()
