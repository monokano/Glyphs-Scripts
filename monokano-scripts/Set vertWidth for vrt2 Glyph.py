# encoding: utf-8
#MenuTitle: Set vertWidth for vrt2 Glyph
# 003
# -*- coding: utf-8 -*-
__doc__="""
Set the vertWidth of the vrt2 glyph (.rotat) to be the same as the Width of the component.
vrt2グリフ（.rotat）のvertWidthをコンポーネントのWidthに合わせる。
"""
from AppKit import NSAlert
import traceback

##################################################
## Localize - English, Japanese
open_file = Glyphs.localize({ 'en': u'Open a glyphs file.', 'ja': u'glyphs ファイルを開いてください。', })
Done = Glyphs.localize({ 'en': u'Done.', 'ja': u'完了しました。', })

##################################################
def showAlert(messageText, InformativeText=""):
	alert = NSAlert.alloc().init()
	alert.setMessageText_(messageText)
	alert.setInformativeText_(InformativeText)
	alert.runModal()
	
##################################################
if Glyphs.font is None:
	showAlert(open_file)
	
else:
	Font = Glyphs.font	
	
	Font.disableUpdateInterface()
	
	transformX = -(Font.selectedFontMaster.descender)
	transformY = Font.selectedFontMaster.ascender
	masterID = Font.selectedFontMaster.id
	appBuildNumber = Glyphs.buildNumber
	
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
				if appBuildNumber < 1241:
					thisLayer.setVertOrigin_(9223372036854775807)
					thisLayer.setVertWidth_(thisWidth)
				else:
					thisLayer.vertOrigin = None
					thisLayer.vertWidth = thisWidth
	
	Font.enableUpdateInterface()
	showAlert(Done)