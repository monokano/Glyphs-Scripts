#MenuTitle: Set AJ1 Supplement

# -*- coding: utf-8 -*-
__doc__="""
Adobe-Japan1のフォントファイルのROSのSupplementを指定した値に変更します。
PythonモジュールのFontToolsのインストールが必要です。
"""


import os
from fontTools.ttLib import TTFont
from AppKit import NSOpenPanel, NSAlert, NSTextField

def chooseOTFFiles():
    panel = NSOpenPanel.openPanel()
    panel.setTitle_("OTFファイルを選択")
    panel.setAllowedFileTypes_(["otf"])
    panel.setCanChooseDirectories_(False)
    panel.setAllowsMultipleSelection_(True)
    if panel.runModal() == 1:
        return [url.path() for url in panel.URLs()]
    return []

def promptSupplementValue():
    alert = NSAlert.alloc().init()
    alert.setMessageText_("Supplement値を入力してください")
    input_field = NSTextField.alloc().initWithFrame_(((0, 0), (200, 24)))
    input_field.setStringValue_("7")
    alert.setAccessoryView_(input_field)
    alert.addButtonWithTitle_("OK")
    alert.addButtonWithTitle_("キャンセル")
    
    if alert.runModal() == 1000:  # OKボタン
        try:
            return int(input_field.stringValue())
        except:
            return None
    return None

def setSupplement(font_path, target_value):
    try:
        font = TTFont(font_path)
        if "CFF " not in font:
            return (font_path, "\n❌ CFFテーブルなし")
        
        cff = font["CFF "]
        top_dict = cff.cff.topDictIndex[0]
        if not hasattr(top_dict, "ROS"):
            return (font_path, "\n❌ ROS情報なし\n（非 OpenType CID？）")
        
        ros = top_dict.ROS
        current = ros[2]
        if current == target_value:
            return (font_path, f"\n✓ 変更不要\n（Supplement は {current} です）")
        
        top_dict.ROS = (ros[0], ros[1], target_value)
        font.save(font_path)
        return (font_path, f"\n✅ Supplement を {current} → {target_value} に変更")
    
    except Exception as e:
        return (font_path, f"\n❌ エラー: \n{str(e)}")

# 実行
font_paths = chooseOTFFiles()
if not font_paths:
    Message("", "ファイルが選択されませんでした", OKButton="OK")
else:
    supplement = promptSupplementValue()
    if supplement is None:
        Message("", "Supplementの入力がキャンセルされたか、無効な値です", OKButton="OK")
    else:
        results = [setSupplement(path, supplement) for path in font_paths]
        result_text = "\n".join([f"{os.path.basename(p)}: {msg}" for p, msg in results])
        Message("", result_text, OKButton="OK")
