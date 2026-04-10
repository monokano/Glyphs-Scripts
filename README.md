
# Glyphsスクリプト

* Glyphs 3用のPythonスクリプト


## スクリプト一覧


### フォントファイル
* フォントファイル用。要Pythonモジュール：FontTools
* **Add BASE Table (CJK)**: CJKフォントファイルにBASEテーブルを追加
* **Add BASE Table (nonCJK)**:  非CJKフォントファイルにBASEテーブルを追加
* **Add Japanese Legacy Compatibility**: 日本語フォントとして認識されるように各種設定を追加
* **Export Tables as TTX**: フォントファイルの各テーブルを同階層にTTXファイルとして出力
* **Set AJ1 Supplement**: Adobe-Japan1フォントファイルのROSのSupplementを指定値に変更
* **Set WinMetrics from FontBBox**: OS/2.WinAscentをhead.FontBBox.yMaxに、OS/2.WinDescentをhead.FontBBox.yMinの絶対値に設定


### GUIあり
* パネルで操作。要Pythonモジュール：Vanilla
* **Add Rect Path**: グリフに矩形パスを追加
* **Set Proportional Metrics**: 選択グリフにプロポーショナルメトリクスとVORGを設定
* **Switch Direction**:  編集ビューの組み方向を切り替え。グリフ情報表示も更新


### GUIなし
* **Center Paths in Glyph Width**: 選択グリフの字形パスをグリフ幅の左右中央に移動。グリフ幅は変えない
* **Set AJ1 Unicode JP04 (Glyphs 3.4)**: AJ1のCMapに基づいてUnicodeを設定

#### VORG
* **Remove VORG**: VORGをデフォルト（None）に戻す
* **Set VORG**: 縦組時に字形パスがボディの天地中央に位置するようVORGを設定。全角英数字・記号向け

#### vrt2
* **Make vrt2 Glyphs**: 選択グリフをコンポーネントにしてvrt2グリフ（.rotat）を作成
* **Optimize vrt2 Glyphs**: 全ての.rotatグリフを最適化


## 更新履歴

* **2026.4.10**
	* 「Add Japanese Legacy Compatibility」を修正
	* 「Set AJ1 Supplement」をブラシュアップ
	* 複数のフォントファイルを選択して実行できるように改善
		* 「Add Japanese Legacy Compatibility」
		* 「Set AJ1 Supplement」
		* 「Set WinMetrics from FontBBox」
* **2026.4.3**
	* 「Add Japanese Legacy Compatibility」でバリアブルフォントを対象に含めた
	* 「Set AJ1 Unicode JP04 (Glyphs 3.4)」をブラッシュアップ
* **2026.4.2**
	* 全面的に整理した
	* 「Add Japanese Legacy Compatibility」を追加
	* 「Export Tables as TTX」を追加
* **2026.4.1**
	* 「Set WinMetrics from FontBBox」を追加
	* 「Add BASE Table (nonCJK)」を修正
* **2026.3.27**
	* 「Add BASE Table (CJK)」を追加
	* 「BASEテーブルを追加（非CJK）」を追加
	* 「Set AJ1 Unicode JP04 (Glyphs 3.4)」をブラッシュアップ
* **2026.3.26**
	* 「Set AJ1 Unicode JP04 (Glyphs 3.4)」を追加
* **2026.3.25**
	* Glyphs 3用に一新。旧ファイルを「OLD」に移動


## License

Licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
