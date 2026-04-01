# MenuTitle: Set VORG

# -*- coding: utf-8 -*-
__doc__="""
選択グリフにVORGを設定します。VORGは縦組時に字形がボディの天地中央に位置するようボディの開始位置を変更する機能です。全角英数字や全角記号を選択してください。
"""

import traceback

def getVertWidth(thisLayer):
	try:
		thisHeight = thisLayer.vertWidth
		if thisHeight is None:
			Font = thisLayer.parent.parent
			thisHeight = Font.selectedFontMaster.ascender - Font.selectedFontMaster.descender
		return thisHeight
	except Exception as e:
		print(traceback.format_exc())
		return

def refreshEditView():
	# Gryphs.redraw() does not work. The display is updated by scaling.
	if (Glyphs.font is not None) and (Glyphs.font.currentTab is not None):
		Font = Glyphs.font
		tmpScale = Font.currentTab.scale
		if tmpScale > 0.1:
			if tmpScale==0.15:
				Font.currentTab.scale = 0.16
			else:
				Font.currentTab.scale = 0.15
		else:
			Font.currentTab.scale = tmpScale - 0.01
		Font.currentTab.scale = tmpScale

isReset = False

Font.disableUpdateInterface()

try:
	Font = Glyphs.font
	thisAscender = Font.selectedFontMaster.ascender
	thisDescender = Font.selectedFontMaster.descender
	selectedLayers = Font.selectedLayers
	for thisLayer in selectedLayers:
	
		#Exclude an empty glyph
		if thisLayer.bounds.size.height == 0:
			continue
		
		if isReset:
			# Reset vertOrigin to default
			gsVertOrigin = None
		else:
			# Value of the top and bottom side-bearings equally allocated.
			equalValue = int( (getVertWidth(thisLayer) - thisLayer.bounds.size.height) / 2 )
			# Slurping distance
			distanceY = (thisAscender - (thisLayer.bounds.origin.y + thisLayer.bounds.size.height)) - equalValue
			# Value of VertOriginY
			vertOriginY = thisAscender - distanceY
			# Value of vertOrigin of Glyphs
			gsVertOrigin = thisAscender - vertOriginY
			# If it is -1 to 1, reset to default.
			if -2 < gsVertOrigin < 2:
				gsVertOrigin = None
		
		thisLayer.vertOrigin = gsVertOrigin
	refreshEditView()
except Exception as e:
	print(traceback.format_exc())

Font.enableUpdateInterface()