# Glyphs 3用スクリプト

## GUI（パネル）あり

### パネル：矩形パスを追加
`GUI_Make Rect Path.py`

矩形パスを追加します。Pythonモジュール `Vanilla` のインストールが必要です。

### パネル：プロポーショナルメトリクスとVORGを設定
`GUI_Proportional Metrics.py`

選択グリフのプロポーショナルメトリクスと VORG を設定します。Pythonモジュール `Vanilla` のインストールが必要です。

### パネル：組方向切り替え
`GUI_Switch Direction.py`

パネルで編集ビューの組方向を切り替えます。グリフ情報表示も更新。Pythonモジュール `Vanilla` のインストールが必要です。

## GUI（パネル）なし

### フォントファイル：AJ1のSupplementを変更
`nonGUI_Change Supplement.py`

Adobe-Japan1 のフォントファイルを選択して、ROS の Supplement を指定した値に変更します。すでに指定した値だったらスキップします。Pythonモジュール `FontTools` のインストールが必要です。

### 選択グリフ：字形をボディの左右中央に
`nonGUI_Center Horizontally in Body.py`

選択グリフの字形をボディの左右中央にします。グリフ幅は変えません。

### 選択グリフ：VORGを設定
`nonGUI_VORG_Set.py`

選択グリフに VORG を設定します。VORG は縦組時に字形がボディの天地中央に位置するようボディの開始位置を変更する機能です。全角英数字や全角記号を選択してください。

### 選択グリフ：VORGを解除
`nonGUI_VORG_Unset.py`

選択グリフの VORG をデフォルト（None）にします。

### vrt2グリフ：選択グリフから作成
`nonGUI_vrt2 Glyph_Make New.py`

選択グリフをコンポーネントにして vrt2 グリフ（.rotat）を作成します。

### vrt2グリフ：全てを最適化
`nonGUI_vrt2 Glyph_ Optimization.py`

vrt2 グリフを最適化します。`.rotat` グリフ全てが対象です。

## 更新履歴

* **2026.3.25** Glyphs 3用に一新。旧ファイルを「OLD」に移動

## License

Licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
