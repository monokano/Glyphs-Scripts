# Glyphsスクリプト

* Glyphs 3用のPythonスクリプト


## スクリプト一覧


### GUI（パネル）あり

#### Glyphsファイル
* **矩形パスを追加：** グリフに矩形パスを追加。要Pythonモジュール：Vanilla
* **プロポーショナルメトリクスとVORGを設定：** 選択グリフにプロポーショナルメトリクスとVORGを設定。要Pythonモジュール：Vanilla
* **組方向切り替え：** 編集ビューの組方向を切り替え。グリフ情報表示も更新。要Pythonモジュール：Vanilla


### GUIなし

#### フォントファイル
* **AJ1のSupplementを変更**：Adobe-Japan1フォントファイルのROSのSupplementを指定値に変更。要Pythonモジュール：FontTools
* **BASEテーブルを追加（CJK）**：CJKフォントファイルにBASEテーブルを追加。要Pythonモジュール：FontTools
* **BASEテーブルを追加（非CJK）**：非CJKフォントファイルにBASEテーブルを追加。要Pythonモジュール：FontTools

#### Glyphsファイル
* **VORGを設定**：縦組時に字形がボディの天地中央に位置するようVORGを設定。全角英数字・記号向け
* **VORGを解除**：VORGをデフォルト（None）に戻す
* **vrt2グリフ：選択グリフから作成**：選択グリフをコンポーネントにしてvrt2グリフ（.rotat）を作成
* **vrt2グリフ：全てを最適化**：全ての.rotatグリフを最適化
* **字形をボディの左右中央に**：字形をボディの左右中央に移動。グリフ幅は変えない
* **AJ1（jp04）のUnicodeを設定**：AJ1のCMapに基づいてUnicodeを設定


## 更新履歴

* **2026.3.27**
	* 「BASEテーブルを追加（CJK）」「BASEテーブルを追加（非CJK）」を追加
	* 「AJ1（jp04）のUnicodeを設定」をブラッシュアップ
	* ツールチップの文言を修正
* **2026.3.26**　「AJ1（jp04）のUnicodeを設定」（Glyphs 3.4用）を追加
* **2026.3.25**　Glyphs 3用に一新。旧ファイルを「OLD」に移動


## License

Licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
