# Glyphs 3用スクリプト

## GUI（パネル）あり

| スクリプト名 | ファイル | 説明 | 必要モジュール |
|---|---|---|---|
| パネル：矩形パスを追加 | `GUI_Make Rect Path.py` | 矩形パスを追加します | `Vanilla` |
| パネル：プロポーショナルメトリクスとVORGを設定 | `GUI_Proportional Metrics.py` | 選択グリフのプロポーショナルメトリクスと VORG を設定します | `Vanilla` |
| パネル：組方向切り替え | `GUI_Switch Direction.py` | 編集ビューの組方向を切り替えます。グリフ情報表示も更新 | `Vanilla` |

## GUI（パネル）なし

| スクリプト名 | ファイル | 説明 | 必要モジュール |
|---|---|---|---|
| フォントファイル：AJ1のSupplementを変更 | `nonGUI_Change Supplement.py` | Adobe-Japan1 フォントの ROS Supplement を指定値に変更します。すでに指定値の場合はスキップ | `FontTools` |
| 選択グリフ：字形をボディの左右中央に | `nonGUI_Center Horizontally in Body.py` | 字形をボディの左右中央に配置します。グリフ幅は変えません | — |
| 選択グリフ：VORGを設定 | `nonGUI_VORG_Set.py` | 縦組時に字形がボディの天地中央に位置するよう VORG を設定します。全角英数字・記号向け | — |
| 選択グリフ：VORGを解除 | `nonGUI_VORG_Unset.py` | VORG をデフォルト（None）に戻します | — |
| vrt2グリフ：選択グリフから作成 | `nonGUI_vrt2 Glyph_Make New.py` | 選択グリフをコンポーネントにして vrt2 グリフ（`.rotat`）を作成します | — |
| vrt2グリフ：全てを最適化 | `nonGUI_vrt2 Glyph_ Optimization.py` | `.rotat` グリフ全てを最適化します | — |

## 更新履歴

* **2026.3.25** Glyphs 3用に一新。旧ファイルを「OLD」に移動

## License

Licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
