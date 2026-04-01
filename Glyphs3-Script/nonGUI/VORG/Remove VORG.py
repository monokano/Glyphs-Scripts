# MenuTitle: Remove VORG

# -*- coding: utf-8 -*-
__doc__="""
選択グリフのVORGをデフォルト（None）にします。
"""

import traceback

isReset = True

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
				
		thisLayer.vertOrigin = None
	refreshEditView()
except Exception as e:
	print(traceback.format_exc())

Font.enableUpdateInterface()