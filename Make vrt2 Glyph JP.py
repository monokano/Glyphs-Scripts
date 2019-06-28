# encoding: utf-8
#MenuTitle: Make vrt2 Glyph JP
# v1.0.5
# -*- coding: utf-8 -*-
__doc__="""
選択グリフを基にして vrt2グリフ（.rotat）を新規追加する。
すでに .rotat グリフがあったり、選択グリフが .rotat の場合は、そこにベースグリフのコンポーネントを配置する。
"""
import traceback

if Glyphs.font is None:
	Glyphs.displayDialog_(u".glyphs ファイルを開いて実行してください。")
	
else:
	Font = Glyphs.font
	selectedLayers = Font.selectedLayers
	if (selectedLayers is None) or (len(selectedLayers)==0):
		Glyphs.displayDialog_(u"グリフを選択してから実行してください。")
		
	else:
		Font.disableUpdateInterface()
		
		transformX = -(Font.selectedFontMaster.descender)
		transformY = Font.selectedFontMaster.ascender
		emWidth = Font.upm
		appBuildNumber = Glyphs.buildNumber
		
		for thisLayer in selectedLayers:
			
			baseName = thisLayer.parent.name
			
			# 選択グリフが .rotat かどうか確認する
			nameArr = baseName.split(".")
			thisSuffix = nameArr.pop()
			if thisSuffix=="rotat":
				# baseNameを代入しなおす
				baseName = ".".join(nameArr)
				newName = thisLayer.parent.name
			else:
				newName = baseName + ".rotat"
			
			# ここでnewNameはいずれも.rotatになっている
			try:
				newGlyph = Font.glyphs[newName]
				
				# 同名の.rotatグリフがなかったら新規追加
				if newGlyph is None:
					newGlyph = GSGlyph()
					newGlyph.name = newName
					Font.glyphs.append(newGlyph)
				
				# グリフ情報を更新
				newGlyph.updateGlyphInfo(True)
				
				# newLayer取得
				newLayer = newGlyph.layers[Font.selectedFontMaster.id]
				# 横幅をEmにする
				newLayer.width = emWidth
				# 空グリフにする
				newLayer.components = []
				newLayer.paths = []
				
				# ベースグリフ取得
				baseGlyph = Font.glyphs[baseName]
				if baseGlyph is not None:
					baseLayer = baseGlyph.layers[Font.selectedFontMaster.id]
					# ベースグリフが空グリフではなかったらコンポーネントを配置
					if baseLayer.bounds.size.width>0:
						newComponent = GSComponent(baseName)
						newComponent.automaticAlignment = False
						newComponent.transform = ((0, -1, 1, 0, transformX, transformY))
						newLayer.components.append(newComponent)					
				
					# vertWidthを設定する
					# いろいろ考慮すると設定しておくのがベスト
					thisWidth = baseLayer.width
					if appBuildNumber < 1241:
						newLayer.setVertOrigin_(None)
						newLayer.setVertWidth_(thisWidth)
					else:
						newLayer.vertOrigin = None
						newLayer.vertWidth = thisWidth
				
			except Exception as e:
				print traceback.format_exc()
		
		Font.enableUpdateInterface()
		Glyphs.displayDialog_(u"完了しました。フィーチャ－を更新してください。")

