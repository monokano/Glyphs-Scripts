#MenuTitle: Optimize vrt2 Glyphs

# -*- coding: utf-8 -*-
__doc__="""
vrt2グリフを最適化します。「.rotat」グリフ全てが対象です。
"""

##################################################
if Glyphs.font is None:
	Message("", "glyphsファイルを開いてください。", OKButton="OK")
	
else:
	Font = Glyphs.font	
	
	Font.disableUpdateInterface()
	
	transformX = -(Font.selectedFontMaster.descender)
	transformY = Font.selectedFontMaster.ascender
	masterID = Font.selectedFontMaster.id
	
	for aGlyph in Font.glyphs:
	
		# Determine if aGlyph is .rotat
		nameArr = aGlyph.name.split(".")
		thisSuffix = nameArr.pop()
		if thisSuffix=="rotat":	
			thisLayer = aGlyph.layers[masterID]
		
			# Determine if thisLayer has one component
			if len(thisLayer.components) == 1:
				aComponent = thisLayer.components[0]
				
				# Set position
				aComponent.transform = ((0, -1, 1, 0, transformX, transformY))

				# Get Glyph
				componentGlyph = Font.glyphs[aComponent.componentName]

				# Set vertWidth
				thisWidth = componentGlyph.layers[masterID].width
				thisLayer.vertOrigin = None
				thisLayer.vertWidth = thisWidth
	
	Font.enableUpdateInterface()
	Message("", "完了しました。", OKButton="OK")