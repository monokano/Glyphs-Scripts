[更新履歴](CHANGELOG.md)

# Glyphsスクリプト

* Glyphs 3用のPythonスクリプト


## フォントファイル用
* 要Pythonモジュール：FontTools

### Glyphs 3の不備を修正
* **Add Japanese Legacy Compatibility**: 日本語フォントとして認識されるように各種設定を追加
* **Set WinMetrics from FontBBox**: OS/2.usWinAscent/usWinDescentをhead.yMax/yMinの値に合わせて設定

### BASE
* **Add BASE Table (CJK)**: CJKフォントファイルにBASEテーブルを追加
* **Add BASE Table (nonCJK)**:  非CJKフォントファイルにBASEテーブルを追加

### その他
* **Set AJ1 Supplement**: Adobe-Japan1フォントファイルのROSのSupplementを指定値に変更
* **Export Tables as TTX**: フォントファイルの各テーブルをTTXファイルとして出力


## Glyphsファイル用

### GUIあり
* パネルで操作。要Pythonモジュール：Vanilla
* **Add Rect Path**: グリフに矩形パスを追加
* **Set Proportional Metrics**: 選択グリフにプロポーショナルメトリクスとVORGを設定
* **Switch Direction**:  編集ビューの組み方向を切り替え。グリフ情報表示も更新


### GUIなし
* **Center Paths in Glyph Width**: 選択グリフの字形パスをグリフ幅の左右中央に移動。グリフ幅は変えない
* **Set AJ1 Unicode JP04 (Glyphs 3.4)**: AJ1のCMapに基づいてUnicodeを設定

#### VORG
* **Set VORG**: 縦組時に字形パスがボディの天地中央に位置するようVORGを設定。全角英数字・記号向け
* **Remove VORG**: VORGをデフォルト（None）に戻す

#### vrt2
* **Make vrt2 Glyphs**: 選択グリフをコンポーネントにしてvrt2グリフ（.rotat）を作成
* **Optimize vrt2 Glyphs**: 全ての.rotatグリフを最適化

#### GSUB File
* **Make AJ1 NiceName GSUB fea**: Adobe-Japan1のGSUBをGitHubから取得し、CIDをnicenameに変換してファイル保存

## License

Licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
