# MenuTitle: 選択グリフ：字形をボディの左右中央に

# -*- coding: utf-8 -*-
__doc__="""
選択グリフの字形をボディの左右中央にします。グリフ幅は変えません。
"""

font = Glyphs.font

for layer in font.selectedLayers:
    glyph = layer.parent
    leftSB = layer.LSB
    rightSB = layer.RSB
    totalSB = leftSB + rightSB
    
    # サイドベアリングを計算
    newLeftSB = totalSB // 2
    newRightSB = totalSB - newLeftSB
    
    # 新しいサイドベアリングを適用
    layer.LSB = newLeftSB
    layer.RSB = newRightSB
