# Glyphs 3用スクリプト

## スクリプト一覧

### GUI（パネル）あり

* **矩形パスを追加：** 矩形パスを追加します。要Vanilla
* **プロポーショナルメトリクスとVORGを設定：** 選択グリフのプロポーショナルメトリクスと VORG を設定します。要Vanilla
* **組方向切り替え：** 編集ビューの組方向を切り替えます。グリフ情報表示も更新。要Vanilla

### GUI（パネル）なし

* **AJ1のSupplementを変更：** Adobe-Japan1 フォントの ROS の Supplement を指定値に変更します。すでに指定値の場合はスキップ。要FontTools
* **字形をボディの左右中央に：** 字形をボディの左右中央に配置します。グリフ幅は変えません。
* **VORGを設定：** 縦組時に字形がボディの天地中央に位置するよう VORG を設定します。全角英数字・記号向け。
* **VORGを解除：** VORG をデフォルト（None）に戻します。
* **vrt2グリフ：選択グリフから作成：** 選択グリフをコンポーネントにして vrt2 グリフ（.rotat）を作成します。
* **vrt2グリフ：全てを最適化：** .rotat グリフ全てを最適化します。

## 更新履歴

* **2026.3.25** Glyphs 3用に一新。旧ファイルを「OLD」に移動

## License

Licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
