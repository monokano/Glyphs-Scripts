# encoding: utf-8
#MenuTitle: Make vrt2 Glyph
# 010
# -*- coding: utf-8 -*-
__doc__="""
Creates a vrt2 glyph (.rotat) based on the selected glyph.
選択されたグリフを基にして vrt2グリフ（.rotat）を作成する。
"""
from AppKit import NSAlert
import traceback

##################################################
## Localize - English, Japanese
open_file = Glyphs.localize({ 'en': u'Open a glyphs file.', 'ja': u'glyphs ファイルを開いてください。', })
select_glyph = Glyphs.localize({ 'en': u'Please select a glyph.', 'ja': u'グリフを選択してください。', })
Done = Glyphs.localize({ 'en': u'Done.', 'ja': u'完了しました。', })
Update_OpenType_feature = Glyphs.localize({ 'en': u'Update OpenType features.', 'ja': u'OpenType フィーチャ－を更新してください。', })

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
	
	selectedLayers = Font.selectedLayers
	if (selectedLayers is None) or (len(selectedLayers)==0):
		showAlert(select_glyph)
		
	else:
		Font.disableUpdateInterface()
		
		masterID = Font.selectedFontMaster.id
		emWidth = Font.upm
		transformX = -(Font.selectedFontMaster.descender)
		transformY = Font.selectedFontMaster.ascender
		appBuildNumber = Glyphs.buildNumber
		
		for thisLayer in selectedLayers:
			
			baseName = thisLayer.parent.name
			
			# Determine if the selected glyph is .rotat
			nameArr = baseName.split(".")
			thisSuffix = nameArr.pop()
			if thisSuffix=="rotat":
				# Reassign baseName
				baseName = ".".join(nameArr)
				newName = thisLayer.parent.name
			else:
				newName = baseName + ".rotat"
			
			# baseName has not .rotat
			# newName has .rotat
			try:
				if baseName[0:1] == ".":
					# baseGlyph is dot name
					continue
				
				# Get baseGlyph
				baseGlyph = Font.glyphs[baseName]
				
				if baseGlyph is None:
					# baseGlyph doesn't exist 
					# Remove .rotat glyph
					del(Font.glyphs[newName])
					continue
				
				# Get baseLayer
				baseLayer = baseGlyph.layers[masterID]
				
				if baseLayer.width >= emWidth:
					# baseLayer width is greater than or equal to Em
					# Remove .rotat glyph
					del(Font.glyphs[newName])
					continue
				
				# baseLayer width is less than Em
				# Get newGlyph
				newGlyph = Font.glyphs[newName]
			
				# newGlyph doesn't exist. Add new .rotat glyph
				if newGlyph is None:
					newGlyph = GSGlyph()
					newGlyph.name = newName
					Font.glyphs.append(newGlyph)
				
				# Remove unicode
				newGlyph.unicodes = []
				# Update glyph info
				newGlyph.updateGlyphInfo(True)
				# Label color
				newGlyph.color = 7 # dark blue
				
				# Get newLayer
				newLayer = newGlyph.layers[masterID]
				
				# Width Em
				newLayer.width = emWidth
				# empty
				newLayer.paths = []
				newLayer.components = []
				newLayer.anchors = []
				
				# If baseGlyph is not empty, add component 
				if baseLayer.bounds.size.width>0:
					newComponent = GSComponent(baseName)
					newComponent.automaticAlignment = False
					newComponent.transform = ((0, -1, 1, 0, transformX, transformY))
					newLayer.components.append(newComponent)					
				
				# Set vertWidth
				thisWidth = baseLayer.width
				if appBuildNumber < 1241:
					newLayer.setVertOrigin_(9.22337203685e+18)
					newLayer.setVertWidth_(thisWidth)
				else:
					newLayer.vertOrigin = None
					newLayer.vertWidth = thisWidth
			
			except Exception as e:
				Font.enableUpdateInterface()
				print traceback.format_exc()
		
		Font.enableUpdateInterface()
		showAlert(Done, Update_OpenType_feature)