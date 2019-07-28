## 変更点

### 2019.7.28
* 「Set vrt2 VertWidth」の名称を「**Set vertWidth for vrt2 Glyph**」に変更（002）。
    * vertWidthの設定だけでなく、コンポーネントの位置も正常に直すようにした。
* **Make vrt2 Glyph**（011）
    * .rotatグリフのラベル色を濃青にしていたが、情報表示が見にくいので黄色に変更。

### 2019.7.27
* **Set vrt2 VertWidth**（001）を新規追加。
* **Make vrt2 Glyph**（010）
    * Glyphs build 1240 までで.rotatグリフのvertWidthが設定されていなかった不具合を修正。

### 2019.7.7
* **Make Rect Path**（005）
    * 矩形サイズがボディ枠のときにvertWidthとvertOriginを反映するかどうかを設定するチェックボックスを追加。
    * 矩形パス追加後に一律にパス方向を修正していたが、改善して、パス方向を修正するかどうかを設定するチェックボックスを追加。