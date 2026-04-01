#MenuTitle: Make vrt2 Glyphs

# -*- coding: utf-8 -*-
__doc__="""
選択グリフを基にして vrt2グリフ（.rotat）を作成します
"""

##################################################
if Glyphs.font is None:
	Message("", "glyphsファイルを開いてください。", OKButton="OK")
	
else:
	Font = Glyphs.font	
	
	selectedLayers = Font.selectedLayers
	if (selectedLayers is None) or (len(selectedLayers)==0):
		Message("", "グリフを選択してください。", OKButton="OK")
		
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
				newGlyph.color = 3 # yellow
				
				# Get newLayer
				newLayer = newGlyph.layers[masterID]
				
				# Width Em
				newLayer.width = emWidth
				# empty
				newLayer.shapes = []
				#newLayer.components = []
				#newLayer.anchors = []
				
				# If baseGlyph is not empty, add component 
				if baseLayer.bounds.size.width>0:
					newComponent = GSComponent(baseName)
					newComponent.automaticAlignment = False
					newComponent.transform = ((0, -1, 1, 0, transformX, transformY))
					newLayer.components.append(newComponent)					
				
				# Set vertWidth
				thisWidth = baseLayer.width
				newLayer.vertOrigin = None
				newLayer.vertWidth = thisWidth
			
			except Exception as e:
				Font.enableUpdateInterface()
		
		Font.enableUpdateInterface()
		Message("OpenType フィーチャ－を更新してください。", "完了しました", OKButton="OK")
		