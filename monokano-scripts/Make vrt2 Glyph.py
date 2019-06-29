# encoding: utf-8
#MenuTitle: Make vrt2 Glyph
# 007
# -*- coding: utf-8 -*-
__doc__="""
Creates a vrt2 glyph (.rotat) based on the selected glyph.
選択されたグリフを基にして vrt2グリフ（.rotat）を作成する。
"""
import traceback

##################################################
## Localize - English, Japanese
open_file = Glyphs.localize({ 'en': u'Open a glyphs file.', 'ja': u'glyphs ファイルを開いてください。', })
select_glyph = Glyphs.localize({ 'en': u'Please select a glyph.', 'ja': u'グリフを選択してください。', })
update_feature = Glyphs.localize({ 'en': u'Done. Update OpenType feature.', 'ja': u'完了しました。フィーチャ－を更新してください。', })

##################################################
if Glyphs.font is None:
	Glyphs.displayDialog_(open_file)
	
else:
	Font = Glyphs.font	
	
	selectedLayers = Font.selectedLayers
	if (selectedLayers is None) or (len(selectedLayers)==0):
		Glyphs.displayDialog_(select_glyph)
		
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
			
			# At this point, newName is both .rotat
			try:
				# Get baseGlyph
				baseGlyph = Font.glyphs[baseName]
				if baseGlyph is None:
					# If baseGlyph doesn't exist 
					# Remove .rotat
					del(Font.glyphs[newName])
				else:
					# Get baseLayer
					baseLayer = baseGlyph.layers[masterID]
					
					if (baseLayer.width >= emWidth) or (baseGlyph.name == ".notdef"):
						# If baseLayer width is greater than or equal to Em
						# If baseGlyph name is .notdef
						# Remove .rotat
						del(Font.glyphs[newName])
					else:
						# Only if baseLayer width is less than Em
						# Get newGlyph
						newGlyph = Font.glyphs[newName]
						
						# If newGlyph doesn't exist, add new .rotat glyph
						if newGlyph is None:
							newGlyph = GSGlyph()
							newGlyph.name = newName
							Font.glyphs.append(newGlyph)
				
						# Update glyph info
						newGlyph.updateGlyphInfo(True)
				
						# Get newLayer
						newLayer = newGlyph.layers[masterID]
						# Width Em
						newLayer.width = emWidth
						# empty
						newLayer.components = []
						newLayer.paths = []
				
						# If baseGlyph is not empty, place component 
						if baseLayer.bounds.size.width>0:
							newComponent = GSComponent(baseName)
							newComponent.automaticAlignment = False
							newComponent.transform = ((0, -1, 1, 0, transformX, transformY))
							newLayer.components.append(newComponent)					
			
						# Set vertWidth
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
		Glyphs.displayDialog_(update_feature)

