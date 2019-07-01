# encoding: utf-8
#MenuTitle: Make Rect Path
# 003
# -*- coding: utf-8 -*-
__doc__="""
Create a rectangular path.
矩形パスを作成する。
"""
import vanilla, traceback

##################################################
## Localize - English, Japanese
Make_Rect_Path = Glyphs.localize({ 'en': u'Make Rect Path', 'ja': u'矩形パス作成', })
Target_Glyph = Glyphs.localize({ 'en': u'Target Glyph:', 'ja': u'対象:', })
Selection = Glyphs.localize({ 'en': u'Selection', 'ja': u'選択グリフ', })
All = Glyphs.localize({ 'en': u'All', 'ja': u'全グリフ', })
Rectangle_Type = Glyphs.localize({ 'en': u'Rectangle Type:', 'ja': u'矩形タイプ:', })
White = Glyphs.localize({ 'en': u'White', 'ja': u'白', })
Black = Glyphs.localize({ 'en': u'Black', 'ja': u'黒', })
Line_Width = Glyphs.localize({ 'en': u'Line Width:', 'ja': u'線幅:', })
Rectangle_Size = Glyphs.localize({ 'en': u'Rectangle Size:', 'ja': u'矩形サイズ:', })
Body = Glyphs.localize({ 'en': u'Body', 'ja': u'ボディ', })
Bounds = Glyphs.localize({ 'en': u'Bounds', 'ja': u'パス領域', })
Offset_Value = Glyphs.localize({ 'en': u'Offset Value:', 'ja': u'ずらし量:', })
Empty_the_glyph = Glyphs.localize({ 'en': u'Empty the glyph before adding a path.', 'ja': u'矩形パスを追加する前にグリフを空にする', })
Run = Glyphs.localize({ 'en': u'Run', 'ja': u'実行', })
Target_glyph_does_not_exist = Glyphs.localize({ 'en': u'Target glyph does not exist.', 'ja': u'対象グリフがありません。', })
Done = Glyphs.localize({ 'en': u'Done.', 'ja': u'完了しました。', })

##################################################
## Class - ArrowEditText
# https://forum.glyphsapp.com/t/vanilla-make-edittext-arrow-savvy/5894/3
GSSteppingTextField = objc.lookUpClass("GSSteppingTextField")
class ArrowEditText(vanilla.EditText):
	nsTextFieldClass = GSSteppingTextField
	def _setCallback(self, callback):
		#self._nsObject.setFocusRingType_(1) #NSFocusRingTypeNone
		super(ArrowEditText, self)._setCallback(callback)
		if callback is not None and self._continuous:
			self._nsObject.setContinuous_(True)
			self._nsObject.setAction_(self._target.action_)
			self._nsObject.setTarget_(self._target)

##################################################
## Class - Mainwindow
class MainWindow(object):
	def __init__(self):
		self.w = vanilla.FloatingWindow((310, 240), Make_Rect_Path, autosaveName="com.tama-san.MakeRectPath.mainwindow")
		self.w.bind("should close", self.savePreferences)

		self.w.label1 = vanilla.TextBox((0, 18, 122, 20), Target_Glyph, alignment="right")
		self.w.radioTarget = vanilla.RadioGroup((125, 18, -10, 20), [Selection, All], isVertical=False)
		self.w.radioTarget.set(0)
		
		self.w.label2 = vanilla.TextBox((0, 46, 122, 20), Rectangle_Type, alignment="right")
		self.w.radioType = vanilla.RadioGroup((125, 46, -10, 20), [White, Black], isVertical=False, callback=self.changeTypeAction)
		self.w.radioType.set(0)
		self.w.label3 = vanilla.TextBox((0, 75, 122, 22), Line_Width, alignment="right", sizeStyle='small')
		self.w.fieldLineWidth = ArrowEditText((125, 70, 50, 22), "10", continuous=True, callback=self.changeLineWidthAction)

		self.w.label4 = vanilla.TextBox((0, 102, 122, 20), Rectangle_Size, alignment="right")
		self.w.radioSize = vanilla.RadioGroup((125, 102, -10, 20), [Body, Bounds], isVertical=False)
		self.w.radioSize.set(0)
		self.w.label5 = vanilla.TextBox((0, 130, 122, 22), Offset_Value, alignment="right", sizeStyle='small')
		self.w.fieldOffset = ArrowEditText((125, 125, 50, 22), "0", continuous=True)

		self.w.checkEmpty = vanilla.CheckBox((20, 165, -0, 20), Empty_the_glyph, value=True)

		self.w.button1 = vanilla.Button((-95, -40, 80, 20), Run, callback=self.runButtonAction)

		####
		self.readPreferences()
		
		####
		self.w.open()
		
		# remove focus
		self.w.getNSWindow().endEditingFor_(self.w.fieldLineWidth.getNSTextField())

	# ------------------------
	## Preferences
	def savePreferences(self, sender):
		try:
			Glyphs.defaults["com.tama-san.MakeRectPath.Target"] = int(self.w.radioTarget.get())
			Glyphs.defaults["com.tama-san.MakeRectPath.Type"] = int(self.w.radioType.get())
			Glyphs.defaults["com.tama-san.MakeRectPath.LineWidth"] = resolveIntText(self.w.fieldLineWidth.get())
			Glyphs.defaults["com.tama-san.MakeRectPath.Size"] = int(self.w.radioSize.get())
			Glyphs.defaults["com.tama-san.MakeRectPath.Offset"] = resolveIntText(self.w.fieldOffset.get())
			Glyphs.defaults["com.tama-san.MakeRectPath.isEmpty"] = int(self.w.checkEmpty.get())
			return True
		except Exception as e:
			print traceback.format_exc()
			return True

	def readPreferences(self):
		try:
			if Glyphs.defaults["com.tama-san.MakeRectPath.isEmpty"] is not None: 
				self.w.radioTarget.set(Glyphs.defaults["com.tama-san.MakeRectPath.Target"])
				self.w.radioType.set(Glyphs.defaults["com.tama-san.MakeRectPath.Type"])
				self.w.fieldLineWidth.set(Glyphs.defaults["com.tama-san.MakeRectPath.LineWidth"])
				self.w.radioSize.set(Glyphs.defaults["com.tama-san.MakeRectPath.Size"])
				self.w.fieldOffset.set(Glyphs.defaults["com.tama-san.MakeRectPath.Offset"])
				self.w.checkEmpty.set(Glyphs.defaults["com.tama-san.MakeRectPath.isEmpty"])
		except Exception as e:
			print traceback.format_exc()
			return

	# ------------------------
	## control actions
	
	def changeTypeAction(self, sender):
		if sender.get()<=0:
			self.w.label3.getNSTextField().setTextColor_(NSColor.textColor())
			self.w.fieldLineWidth.enable(True)
			self.w.button1.enable( (resolveInt(self.w.fieldLineWidth.get())>0) )
		else:
			self.w.label3.getNSTextField().setTextColor_(NSColor.headerColor())
			self.w.fieldLineWidth.enable(False)
			self.w.button1.enable(True)
		
	def changeLineWidthAction(self, sender):
		self.w.button1.enable( (resolveInt(sender.get())>0) )

	def runButtonAction(self, sender):
		if Glyphs.font is not None:
			Font = Glyphs.font
			target = self.w.radioTarget.get()
			type = self.w.radioType.get()
			lineWidth = resolveInt(self.w.fieldLineWidth.get())
			size = self.w.radioSize.get()
			OffsetValue = resolveInt(self.w.fieldOffset.get())
			isEmpty = self.w.checkEmpty.get()
			###
			makeRectPath(Font, target, type, lineWidth, size, OffsetValue, isEmpty) 

		
##################################################
def makeRectPath(Font, target, type, lineWidth, size, OffsetValue, isEmpty):
	
	masterID = Font.selectedFontMaster.id
	
	# get targetLayers
	targetLayers = []
	if target==0:
		targetLayers = Font.selectedLayers
	else:
		allGlyphs = Font.glyphs
		for aGlyph in Glyphs.font.glyphs:
			targetLayers.append( aGlyph.layers[masterID] )

	if (targetLayers is None) or (len(targetLayers)==0):
		showAlert(Target_glyph_does_not_exist)
		
	else:
		# start
		Font.disableUpdateInterface()
		
		for thisLayer in targetLayers:
			
			if size==0:
				thisLeftX = 0.0
				thisTopY = Font.selectedFontMaster.ascender
				thisBottomY = Font.selectedFontMaster.descender
				thisRightX = thisLayer.width
			else:
				thisLeftX = thisLayer.bounds.origin.x
				thisTopY = thisLayer.bounds.origin.y + thisLayer.bounds.size.height
				thisBottomY = thisLayer.bounds.origin.y
				thisRightX = thisLayer.bounds.origin.x + thisLayer.bounds.size.width
			
			if (thisRightX - thisLeftX)>0:
				if type==0:
					# White
					makeWhiteRect(Font, thisLayer, OffsetValue, isEmpty, thisLeftX, thisTopY, thisBottomY, thisRightX, lineWidth)
				else:
					# Black
					makeBlackRect(Font, thisLayer, OffsetValue, isEmpty, thisLeftX, thisTopY, thisBottomY, thisRightX)
				thisLayer.correctPathDirection()
	
		# end
		Font.enableUpdateInterface()
		showAlert(Done)


def makeWhiteRect(Font, thisLayer, OffsetValue, isEmpty, thisLeftX, thisTopY, thisBottomY, thisRightX, lineWidth):
	
	# Outside
	pos0 = NSPoint()
	pos0.x = thisLeftX - OffsetValue
	pos0.y = thisTopY + OffsetValue
	node0 = GSNode(  )
	node0.position = pos0
	node0.type = GSLINE
	node0.connection = GSSHARP

	pos1 = NSPoint()
	pos1.x = thisLeftX - OffsetValue
	pos1.y = thisBottomY - OffsetValue
	node1 = GSNode(  )
	node1.position = pos1
	node1.type = GSLINE
	node1.connection = GSSHARP

	pos2 = NSPoint()
	pos2.x = thisRightX + OffsetValue
	pos2.y = thisBottomY - OffsetValue
	node2 = GSNode(  )
	node2.position = pos2
	node2.type = GSLINE
	node2.connection = GSSHARP

	pos3 = NSPoint()
	pos3.x = thisRightX + OffsetValue
	pos3.y = thisTopY + OffsetValue
	node3 = GSNode(  )
	node3.position = pos3
	node3.type = GSLINE
	node3.connection = GSSHARP

	tmpPath = GSPath()
	tmpPath.nodes = [ node0, node1, node2, node3 ]
	tmpPath.closed = True
	
	# Inside
	pos0 = NSPoint()
	pos0.x = thisLeftX + lineWidth - OffsetValue
	pos0.y = thisTopY - lineWidth + OffsetValue
	node0 = GSNode(  )
	node0.position = pos0
	node0.type = GSLINE
	node0.connection = GSSHARP

	pos1 = NSPoint()
	pos1.x = thisLeftX + lineWidth - OffsetValue
	pos1.y = thisBottomY + lineWidth - OffsetValue
	node1 = GSNode(  )
	node1.position = pos1
	node1.type = GSLINE
	node1.connection = GSSHARP

	pos2 = NSPoint()
	pos2.x = thisRightX - lineWidth + OffsetValue
	pos2.y = thisBottomY + lineWidth - OffsetValue
	node2 = GSNode(  )
	node2.position = pos2
	node2.type = GSLINE
	node2.connection = GSSHARP

	pos3 = NSPoint()
	pos3.x = thisRightX - lineWidth + OffsetValue
	pos3.y = thisTopY - lineWidth + OffsetValue
	node3 = GSNode(  )
	node3.position = pos3
	node3.type = GSLINE
	node3.connection = GSSHARP

	tmpPath2 = GSPath()
	tmpPath2.nodes = [ node0, node1, node2, node3 ]
	tmpPath2.closed = True
	
	if isEmpty:
		thisLayer.paths = []
		thisLayer.components = []
		thisLayer.anchors = []

	thisLayer.paths.append( tmpPath )
	thisLayer.paths.append( tmpPath2 )


def makeBlackRect(Font, thisLayer, OffsetValue, isEmpty, thisLeftX, thisTopY, thisBottomY, thisRightX):

	pos0 = NSPoint()
	pos0.x = thisLeftX - OffsetValue
	pos0.y = thisTopY + OffsetValue
	node0 = GSNode(  )
	node0.position = pos0
	node0.type = GSLINE
	node0.connection = GSSHARP

	pos1 = NSPoint()
	pos1.x = thisLeftX - OffsetValue
	pos1.y = thisBottomY - OffsetValue
	node1 = GSNode(  )
	node1.position = pos1
	node1.type = GSLINE
	node1.connection = GSSHARP

	pos2 = NSPoint()
	pos2.x = thisRightX + OffsetValue
	pos2.y = thisBottomY - OffsetValue
	node2 = GSNode(  )
	node2.position = pos2
	node2.type = GSLINE
	node2.connection = GSSHARP

	pos3 = NSPoint()
	pos3.x = thisRightX + OffsetValue
	pos3.y = thisTopY + OffsetValue
	node3 = GSNode(  )
	node3.position = pos3
	node3.type = GSLINE
	node3.connection = GSSHARP

	tmpPath = GSPath()
	tmpPath.nodes = [ node0, node1, node2, node3 ]
	tmpPath.closed = True

	if isEmpty:
		thisLayer.paths = []
		thisLayer.components = []
		thisLayer.anchors = []

	thisLayer.paths.append( tmpPath )


def resolveInt(value):
	try:
		return int(value)
	except ValueError:
		return 0

def resolveIntText(value):
	try:
		return str(int(value))
	except ValueError:
		return "0"

def showAlert(messageText, InformativeText=""):
	alert = NSAlert.alloc().init()
	alert.setMessageText_(messageText)
	alert.setInformativeText_(InformativeText)
	alert.runModal()

##################################################
MainWindow()
