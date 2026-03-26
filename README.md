# Glyphsスクリプト

* Glyphs 3用のPythonスクリプト

## スクリプト一覧

### GUI（パネル）あり

* **矩形パスを追加：** 矩形パスを追加。要Vanilla
* **プロポーショナルメトリクスとVORGを設定：** 選択グリフのプロポーショナルメトリクスとVORGを設定。要Vanilla
* **組方向切り替え：** 編集ビューの組方向を切り替え。グリフ情報表示も更新。要Vanilla

### GUIなし

* **AJ1のSupplementを変更**：Adobe-Japan1フォントのROSのSupplementを指定値に変更。要FontTools
* **字形をボディの左右中央に**：字形をボディの左右中央に配置。グリフ幅は変えません。
* **VORGを設定**：縦組時に字形がボディの天地中央に位置するようVORGを設定。全角英数字・記号向け。
* **VORGを解除**：VORGをデフォルト（None）に戻す
* **vrt2グリフ：選択グリフから作成**：選択グリフをコンポーネントにしてvrt2グリフ（.rotat）を作成
* **vrt2グリフ：全てを最適化**：.rotatグリフ全てを最適化
* **AJ1（jp04）のUnicodeを設定**：AJ1のCMapに基づいてUnicodeを設定

## 更新履歴

* **2026.3.26**　「AJ1（jp04）のUnicodeを設定」（Glyphs 3.4用）を追加
* **2026.3.25**　Glyphs 3用に一新。旧ファイルを「OLD」に移動

## License

Licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
