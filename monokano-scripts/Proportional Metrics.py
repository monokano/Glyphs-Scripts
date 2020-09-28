# encoding: utf-8
#MenuTitle: Proportional Metrics
# 047
# -*- coding: utf-8 -*-
__doc__="""
Set and edit the proportional metrics and VORG for the selected glyph.
選択グリフのプロポーショナルメトリクスとVORGを設定編集する。
"""
import vanilla, traceback

##################################################
## Default values - Rewritable
sidebearingValue = "60"
shiftValue = "5"

##################################################
## Localize - English, Japanese
windowTitle = Glyphs.localize({ 'en': u'Proportional Metrics', 'ja': u'プロポーショナルメトリクス', })
Left_Sidebearing = Glyphs.localize({ 'en': u'Left Sidebearing:', 'ja': u'左 サイドベアリング:', })
Right_Sidebearing = Glyphs.localize({ 'en': u'Right Sidebearing:', 'ja': u'右 サイドベアリング:', })
Top_Sidebearing = Glyphs.localize({ 'en': u'Top Sidebearing:', 'ja': u'上 サイドベアリング:', })
Bottom_Sidebearing = Glyphs.localize({ 'en': u'Bottom Sidebearing:', 'ja': u'下 サイドベアリング:', })
Set_Anchors = Glyphs.localize({ 'en': u'Set Anchors', 'ja': u'アンカーをセット', })
Remove_Anchors = Glyphs.localize({ 'en': u'Remove Anchors', 'ja': u'アンカーを削除', })
Move_Positions = Glyphs.localize({ 'en': u'Move Anchor Positions', 'ja': u'アンカー位置を移動', })
Auto_Adjust = Glyphs.localize({ 'en': u'Auto Adjust', 'ja': u'自動調整', })
Reset = Glyphs.localize({ 'en': u'Reset', 'ja': u'リセット', })
Limit = Glyphs.localize({ 'en': u'Limit', 'ja': u'制限', })
Reverse = Glyphs.localize({ 'en': u'Reverse', 'ja': u'逆方向', })
Shift = Glyphs.localize({ 'en': u'Shift:', 'ja': u'増減値:', })
Auto_Direction = Glyphs.localize({ 'en': u'Auto', 'ja': u'自動方向', })
L = Glyphs.localize({ 'en': u'L', 'ja': u'左', })
R = Glyphs.localize({ 'en': u'R', 'ja': u'右', })
T = Glyphs.localize({ 'en': u'T', 'ja': u'上', })
B = Glyphs.localize({ 'en': u'B', 'ja': u'下', })
Single_Mode = Glyphs.localize({ 'en': u'Single Mode', 'ja': u'単グリフモード', })
Reset_to_Defaults = Glyphs.localize({ 'en': u'Reset to Defaults', 'ja': u'デフォルトに戻す', })
Script_Requires = Glyphs.localize({ 'en': u'Script “Proportional Metrics”\nRequires Glyphs 2.6.2 (1241) or later.', 'ja': u'スクリプト「プロポーショナルメトリクス」\nGlyphs 2.6.2 (1241) 以降が必要です', })

##################################################
## Global
isSingleMode = False # Not rewritable. Must be False

##################################################
## Class - ArrowEditText
# https://forum.glyphsapp.com/t/vanilla-make-edittext-arrow-savvy/5894/3
# Great!
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
class Mainwindow(object):
	def __init__(self):

		## window
		self.w = vanilla.FloatingWindow((232, 324), windowTitle, autosaveName="com.tama-san.ProportionalMetrics.mainwindow")
		self.w.bind("should close", self.savePreferences)
		
		## auto direction ON/OFF
		self.w.checkDirection = vanilla.CheckBox((10, 5, -10, 20), Auto_Direction, sizeStyle='small', value=True, callback=self.changeTabAction)
		
		## glyph name
		self.w.labelName = vanilla.TextBox((75, 5, -45, 20), "", alignment='center')
		self.w.labelName.getNSTextField().setTextColor_(NSColor.blueColor())		
		
		## reset menu		
		items = [dict(title=Reset_to_Defaults, callback=self.popupResetAction)]
		self.w.popupAction = vanilla.ActionButton((188, 4, -10, 20), items, sizeStyle='small')
		self.w.popupAction.getNSPopUpButton().setTransparent_(True)
		
		# toggle single mode
		self.w.toggleButton = vanilla.SquareButton((206, 7, 16, 16), "", callback=self.toggleSingleModeAction)
		self.w.toggleButton.getNSButton().setButtonType_(1) #NSButtonTypePushOnPushOff
		self.w.toggleButton.getNSButton().setToolTip_(Single_Mode)

		## tabs
		self.w.tabs = vanilla.Tabs((10, 26, -10, -14), ["LSB / RSB", "TSB / BSB", "VORG"], sizeStyle='small', callback=self.changeTabAction)
		
		## tab - palt
		tab1 = self.w.tabs[0]
		tab1.label1 = vanilla.TextBox((0, 12, 142, 20), Left_Sidebearing, alignment='right')
		tab1.label2 = vanilla.TextBox((0, 39, 142, 20), Right_Sidebearing, alignment='right')
		tab1.fieldLSB = ArrowEditText((146, 10, -10, 22), sidebearingValue, continuous=True)
		tab1.fieldRSB = ArrowEditText((146, 37, -10, 22), sidebearingValue, continuous=True)
		tab1.checkLimit = vanilla.CheckBox((10, 65-2, -10, 20), Limit, value=True)
		tab1.button1 = vanilla.Button((10, 86, -10, 20), Set_Anchors, callback=self.setAnchorsHorizontalAction)

		tab1.line1 = vanilla.HorizontalLine((10, 118, -10, 1))
		tab1.label3 = vanilla.TextBox((85, 134, 57, 20), Shift, alignment='right')
		tab1.checkReverse = vanilla.CheckBox((10, 133, 70, 20), Reverse)
		tab1.fieldChange = ArrowEditText((146, 132, -10, 22), shiftValue, continuous=True)
		tab1.checkLimitMove = vanilla.CheckBox((10, 160-2, -10, 20), Limit, value=True)
		tab1.checkLeft = vanilla.CheckBox((127, 160-2, -10, 20), L, sizeStyle='small', value=True)
		tab1.checkRight = vanilla.CheckBox((164, 160-2, -10, 20), R, sizeStyle='small', value=True)
		tab1.button2 = vanilla.Button((10, 181, -10, 20), Move_Positions, callback=self.moveAnchorsHorizontalAction)

		tab1.line2 = vanilla.HorizontalLine((10, 214, -10, 1))
		tab1.button3 = vanilla.Button((10, 228, -10, 20), Remove_Anchors, callback=self.removeAnchorsAction)

		## tab - vpal
		tab2 = self.w.tabs[1]
		tab2.label1 = vanilla.TextBox((0, 12, 142, 20), Top_Sidebearing, alignment='right')
		tab2.label2 = vanilla.TextBox((0, 39, 142, 20), Bottom_Sidebearing, alignment='right')
		tab2.fieldTSB = ArrowEditText((146, 10, -10, 22), sidebearingValue, continuous=True)
		tab2.fieldBSB = ArrowEditText((146, 37, -10, 22), sidebearingValue, continuous=True)
		tab2.checkLimit = vanilla.CheckBox((10, 65-2, -10, 20), Limit, value=True)
		tab2.button1 = vanilla.Button((10, 86, -10, 20), Set_Anchors, callback=self.setAnchorsVerticalAction)

		tab2.line1 = vanilla.HorizontalLine((10, 118, -10, 1))
		tab2.label3 = vanilla.TextBox((85, 134, 57, 20), Shift, alignment='right')
		tab2.checkReverse = vanilla.CheckBox((10, 133, 70, 20), Reverse)
		tab2.fieldChange = ArrowEditText((146, 132, -10, 22), shiftValue, continuous=True)
		tab2.checkLimitMove = vanilla.CheckBox((10, 160-2, -10, 20), Limit, value=True)
		tab2.checkTop = vanilla.CheckBox((127, 160-2, -10, 20), T, sizeStyle='small', value=True)
		tab2.checkBottom = vanilla.CheckBox((164, 160-2, -10, 20), B, sizeStyle='small', value=True)
		tab2.button2 = vanilla.Button((10, 181, -10, 20), Move_Positions, callback=self.moveAnchorsVerticalAction)

		tab2.line2 = vanilla.HorizontalLine((10, 214, -10, 1))
		tab2.button3 = vanilla.Button((10, 228, -10, 20), Remove_Anchors, callback=self.removeAnchorsAction)

		## tab - VORG
		tab3 = self.w.tabs[2]
		tab3.button1 = vanilla.Button((10, 12, -10, 20), Auto_Adjust, callback=self.adjustVORGAction)
		tab3.button2 = vanilla.Button((10, 45, -10, 20), Reset, callback=self.resetVORGAction)
		
		####
		self.readPreferences()
		
		####
		self.w.open()

	# ------------------------
	## Preferences
	def savePreferences(self, sender):
		try:
			Glyphs.defaults["com.tama-san.ProportionalMetrics.autoDirection"] = int(self.w.checkDirection.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.tabPanelIndex"] = int(self.w.tabs.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.LSB"] = resolveIntText(self.w.tabs[0].fieldLSB.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.RSB"] = resolveIntText(self.w.tabs[0].fieldRSB.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.changeValue0"] = resolveIntText(self.w.tabs[0].fieldChange.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.checkReverse0"] = int(self.w.tabs[0].checkReverse.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.checkLimit0"] = int(self.w.tabs[0].checkLimit.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.checkLimitMove0"] = int(self.w.tabs[0].checkLimitMove.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.checkLeft"] = int(self.w.tabs[0].checkLeft.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.checkRight"] = int(self.w.tabs[0].checkRight.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.TSB"] = resolveIntText(self.w.tabs[1].fieldTSB.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.BSB"] = resolveIntText(self.w.tabs[1].fieldBSB.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.changeValue1"] = resolveIntText(self.w.tabs[1].fieldChange.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.checkReverse1"] = int(self.w.tabs[1].checkReverse.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.checkLimit1"] = int(self.w.tabs[1].checkLimit.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.checkLimitMove1"] = int(self.w.tabs[1].checkLimitMove.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.checkTop"] = int(self.w.tabs[1].checkTop.get())
			Glyphs.defaults["com.tama-san.ProportionalMetrics.checkBottom"] = int(self.w.tabs[1].checkBottom.get())
			# Make sure to remove callback when finished.
			Glyphs.removeCallback(self.updateInterface_KOLDAVTVGJGPDKZOMU5OOPZMJI)
			return True
		except Exception as e:
			print traceback.format_exc()
			return True

	def readPreferences(self):
		try:
			self.w.checkDirection.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.autoDirection"])
			self.w.tabs.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.tabPanelIndex"])
			self.w.tabs[0].fieldLSB.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.LSB"])
			self.w.tabs[0].fieldRSB.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.RSB"])
			self.w.tabs[1].fieldTSB.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.TSB"])
			self.w.tabs[1].fieldBSB.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.BSB"])
			self.w.tabs[0].fieldChange.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.changeValue0"])
			self.w.tabs[1].fieldChange.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.changeValue1"])
			self.w.tabs[0].checkReverse.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.checkReverse0"])
			self.w.tabs[1].checkReverse.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.checkReverse1"])
			self.w.tabs[0].checkLimit.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.checkLimit0"])
			self.w.tabs[1].checkLimit.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.checkLimit1"])
			self.w.tabs[0].checkLimitMove.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.checkLimitMove0"])
			self.w.tabs[1].checkLimitMove.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.checkLimitMove1"])
			self.w.tabs[0].checkLeft.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.checkLeft"])
			self.w.tabs[0].checkRight.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.checkRight"])
			self.w.tabs[1].checkTop.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.checkTop"])
			self.w.tabs[1].checkBottom.set(Glyphs.defaults["com.tama-san.ProportionalMetrics.checkBottom"])
		except Exception as e:
			print traceback.format_exc()
			return
	
	# ------------------------
	## control actions
	
	def toggleSingleModeAction(self, sender):
		global isSingleMode
		isSingleMode = sender.getNSButton().state()
		self.w.labelName.set("")
		self.w.tabs[0].button1.enable(True)
		self.w.tabs[0].button2.enable(True)
		self.w.tabs[0].button3.enable(True)
		self.w.tabs[1].button1.enable(True)
		self.w.tabs[1].button2.enable(True)
		self.w.tabs[1].button3.enable(True)
		self.w.tabs[2].button1.enable(True)
		self.w.tabs[2].button2.enable(True)
		if isSingleMode:
			self.w.tabs[0].fieldLSB.getNSTextField().setTextColor_(NSColor.blueColor())
			self.w.tabs[0].fieldRSB.getNSTextField().setTextColor_(NSColor.blueColor())
			self.w.tabs[1].fieldTSB.getNSTextField().setTextColor_(NSColor.blueColor())
			self.w.tabs[1].fieldBSB.getNSTextField().setTextColor_(NSColor.blueColor())
			self.w.tabs[0].fieldChange.getNSTextField().setTextColor_(NSColor.blueColor())
			self.w.tabs[1].fieldChange.getNSTextField().setTextColor_(NSColor.blueColor())
			self.updateInterface_KOLDAVTVGJGPDKZOMU5OOPZMJI()
			# start notification
			Glyphs.addCallback(self.updateInterface_KOLDAVTVGJGPDKZOMU5OOPZMJI, UPDATEINTERFACE)
		else:
			self.w.tabs[0].fieldLSB.getNSTextField().setTextColor_(NSColor.textColor())
			self.w.tabs[0].fieldRSB.getNSTextField().setTextColor_(NSColor.textColor())
			self.w.tabs[1].fieldTSB.getNSTextField().setTextColor_(NSColor.textColor())
			self.w.tabs[1].fieldBSB.getNSTextField().setTextColor_(NSColor.textColor())
			self.w.tabs[0].fieldChange.getNSTextField().setTextColor_(NSColor.textColor())
			self.w.tabs[1].fieldChange.getNSTextField().setTextColor_(NSColor.textColor())
			if self.w.tabs[0].fieldLSB.get()=="":
				self.w.tabs[0].fieldLSB.set(sidebearingValue)
			if self.w.tabs[0].fieldRSB.get()=="":
				self.w.tabs[0].fieldRSB.set(sidebearingValue)
			if self.w.tabs[1].fieldTSB.get()=="":
				self.w.tabs[1].fieldTSB.set(sidebearingValue)
			if self.w.tabs[1].fieldBSB.get()=="":
				self.w.tabs[1].fieldBSB.set(sidebearingValue)
			
			# stop notification
			Glyphs.removeCallback(self.updateInterface_KOLDAVTVGJGPDKZOMU5OOPZMJI)
	
	def updateInterface_KOLDAVTVGJGPDKZOMU5OOPZMJI(self, layer=None, info=None, sender=None):
		# Note - make sure to use unique function name.
		# Run in response to a notification when Single Mode.
		self.w.tabs[0].fieldLSB.set("")
		self.w.tabs[0].fieldRSB.set("")
		self.w.tabs[1].fieldTSB.set("")
		self.w.tabs[1].fieldBSB.set("")
		self.w.tabs[0].button1.enable(False)
		self.w.tabs[0].button2.enable(False)
		self.w.tabs[0].button3.enable(False)
		self.w.tabs[1].button1.enable(False)
		self.w.tabs[1].button2.enable(False)
		self.w.tabs[1].button3.enable(False)
		self.w.tabs[2].button1.enable(False)
		self.w.tabs[2].button2.enable(False)
		try:
			if (Glyphs.font is not None) and (Glyphs.font.currentTab is not None):
				# Only one selection glyph
				if len(Glyphs.font.selectedLayers)==1:
					# Determine Selection Glyph
					thisLayer = Glyphs.font.selectedLayers[0]
					self.getSidebearing(thisLayer)
		except Exception as e:
			print traceback.format_exc()
			return
	
	def getSidebearing(self, thisLayer):
		# Convert the anchor position to the side-bearing and set it.
		try:
			glyphName = thisLayer.parent.name
			self.w.labelName.set(glyphName)			
			self.w.tabs[0].button1.enable(True)
			self.w.tabs[0].button2.enable(True)
			self.w.tabs[0].button3.enable(True)
			self.w.tabs[1].button1.enable(True)
			self.w.tabs[1].button2.enable(True)
			self.w.tabs[1].button3.enable(True)
			self.w.tabs[2].button1.enable(True)
			self.w.tabs[2].button2.enable(True)
			tabIndex = self.w.tabs.get()
			# the values of the side-bearing
			values = getAnchorToSidebearing(thisLayer, tabIndex)
			if (values is not None) and len(values)==2:
				if tabIndex==0:
					self.w.tabs[0].fieldLSB.set( str(int(values[0])) )
					self.w.tabs[0].fieldRSB.set( str(int(values[1])) )
				else:
					self.w.tabs[1].fieldTSB.set( str(int(values[0])) )
					self.w.tabs[1].fieldBSB.set( str(int(values[1])) )
		except Exception as e:
			print traceback.format_exc()
			return
	
	def popupResetAction(self, sender):
		# Reset to Defaults
		global isSingleMode
		isSingleMode = False
		Glyphs.removeCallback(self.updateInterface_KOLDAVTVGJGPDKZOMU5OOPZMJI)
		###
		self.w.toggleButton.getNSButton().setState_(False)
		self.w.labelName.set("")
		self.w.checkDirection.set(True)
		self.w.tabs[0].button1.enable(True)
		self.w.tabs[0].button2.enable(True)
		self.w.tabs[0].button3.enable(True)
		self.w.tabs[1].button1.enable(True)
		self.w.tabs[1].button2.enable(True)
		self.w.tabs[1].button3.enable(True)
		self.w.tabs[2].button1.enable(True)
		self.w.tabs[2].button2.enable(True)
		self.w.tabs[0].fieldLSB.getNSTextField().setTextColor_(NSColor.textColor())
		self.w.tabs[0].fieldRSB.getNSTextField().setTextColor_(NSColor.textColor())
		self.w.tabs[1].fieldTSB.getNSTextField().setTextColor_(NSColor.textColor())
		self.w.tabs[1].fieldBSB.getNSTextField().setTextColor_(NSColor.textColor())
		self.w.tabs[0].fieldChange.getNSTextField().setTextColor_(NSColor.textColor())
		self.w.tabs[1].fieldChange.getNSTextField().setTextColor_(NSColor.textColor())
		###
		self.w.tabs[0].fieldLSB.set(sidebearingValue)
		self.w.tabs[0].fieldRSB.set(sidebearingValue)
		self.w.tabs[1].fieldTSB.set(sidebearingValue)
		self.w.tabs[1].fieldBSB.set(sidebearingValue)
		self.w.tabs[0].fieldChange.set(shiftValue)
		self.w.tabs[1].fieldChange.set(shiftValue)
		self.w.tabs[0].checkReverse.set(False)
		self.w.tabs[1].checkReverse.set(False)
		self.w.tabs[0].checkLimit.set(True)
		self.w.tabs[1].checkLimit.set(True)
		self.w.tabs[0].checkLimitMove.set(True)
		self.w.tabs[1].checkLimitMove.set(True)
		self.w.tabs[0].checkLeft.set(True)
		self.w.tabs[0].checkRight.set(True)
		self.w.tabs[1].checkTop.set(True)
		self.w.tabs[1].checkBottom.set(True)
	
	def changeTabAction(self, sender):
		tabIndex = self.w.tabs.get()
		isSetDirection = (self.w.checkDirection.get()==1)
		if tabIndex==0:
			self.w.resize(232, 324, True)
			if isSingleMode:
				self.updateInterface_KOLDAVTVGJGPDKZOMU5OOPZMJI()
			if isSetDirection:
				setDirectionHorizontal()
		elif tabIndex==1:
			self.w.resize(232, 324, True)
			if isSingleMode:
				self.updateInterface_KOLDAVTVGJGPDKZOMU5OOPZMJI()
			if isSetDirection:
				setDirectionVertical()
		elif tabIndex==2:
			self.w.resize(232, 142, True)
			if isSetDirection:
				setDirectionVertical()

	def setAnchorsHorizontalAction(self, sender):
		v1 = resolveInt(self.w.tabs[0].fieldLSB.get())
		v2 = resolveInt(self.w.tabs[0].fieldRSB.get())
		isLimit = int(self.w.tabs[0].checkLimit.get())
		setAnchors(v1, v2, 0, isLimit)

	def setAnchorsVerticalAction(self, sender):
		v1 = resolveInt(self.w.tabs[1].fieldTSB.get())
		v2 = resolveInt(self.w.tabs[1].fieldBSB.get())
		isLimit = int(self.w.tabs[1].checkLimit.get())
		setAnchors(v1, v2, 1, isLimit)

	def moveAnchorsHorizontalAction(self, sender):
		unitValue = resolveInt(self.w.tabs[0].fieldChange.get())
		if self.w.tabs[0].checkReverse.get()==1:
			unitValue = -unitValue
		isLimit = int(self.w.tabs[0].checkLimitMove.get())
		isTarget1 = self.w.tabs[0].checkLeft.get()
		isTarget2 = self.w.tabs[0].checkRight.get()
		moveAnchorsWithUnit(unitValue, 0, isLimit, isTarget1, isTarget2)

	def moveAnchorsVerticalAction(self, sender):
		unitValue = resolveInt(self.w.tabs[1].fieldChange.get())
		if self.w.tabs[1].checkReverse.get()==1:
			unitValue = -unitValue
		isLimit = int(self.w.tabs[1].checkLimitMove.get())
		isTarget1 = self.w.tabs[1].checkTop.get()
		isTarget2 = self.w.tabs[1].checkBottom.get()
		moveAnchorsWithUnit(unitValue, 1, isLimit, isTarget1, isTarget2)

	def removeAnchorsAction(self, sender):
		removeAnchors( self.w.tabs.get() )

	def adjustVORGAction(self, sender):
		autoAdjustVORG(False)

	def resetVORGAction(self, sender):
		autoAdjustVORG(True)


##################################################
## functions
def getAnchorToSidebearing(thisLayer, index):
	# Convert to side-bearing and return list (2 elements).
	values=[]
	try:
		if index==0:
			#LSB
			if thisLayer.anchorForName_("LSB"):
				anchor = thisLayer.anchors["LSB"]
				valueLSB = thisLayer.bounds.origin.x - anchor.position.x
				values.append(valueLSB)
			#RSB
			if thisLayer.anchorForName_("RSB"):
				anchor = thisLayer.anchors["RSB"]
				valueRSB = anchor.position.x - (thisLayer.bounds.origin.x + thisLayer.bounds.size.width)
				values.append(valueRSB)
		else:
			if thisLayer.anchorForName_("TSB"):
				anchor = thisLayer.anchors["TSB"]
				valueTSB = anchor.position.y - thisLayer.bounds.origin.y - thisLayer.bounds.size.height
				values.append(valueTSB)
			#RSB
			if thisLayer.anchorForName_("BSB"):
				anchor = thisLayer.anchors["BSB"]
				valueRSB = thisLayer.bounds.origin.y - anchor.position.y
				values.append(valueRSB)
		return values
	except Exception as e:
		print traceback.format_exc()
		return []

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

def setDirectionHorizontal():
	if (Glyphs.font is not None) and (Glyphs.font.currentTab is not None):
		Font = Glyphs.font
		Font.currentTab.direction = LTR
		# Update
		Font.currentTab.textCursor = Font.currentTab.textCursor

def setDirectionVertical():
	if (Glyphs.font is not None) and (Glyphs.font.currentTab is not None):
		Font = Glyphs.font
		Font.currentTab.direction = RTLTTB
		# Update
		Font.currentTab.textCursor = Font.currentTab.textCursor

def getVertWidth(thisLayer):
	try:
		thisHeight = thisLayer.vertWidth
		if thisHeight is None:
			Font = thisLayer.parent.parent
			thisHeight = Font.selectedFontMaster.ascender - Font.selectedFontMaster.descender
		return thisHeight
	except Exception as e:
		print traceback.format_exc()
		return

def getVertOrigin(thisLayer):
	try:
		thisVertOrigin = thisLayer.vertOrigin
		if thisVertOrigin is None:
			thisVertOrigin = 0
		return thisVertOrigin
	except Exception as e:
		print traceback.format_exc()
		return


def moveAnchorsWithUnit(unitValue, index, isLimit, isTarget1, isTarget2):
	# If there is no anchor, do nothing.
	try:
		Font = Glyphs.font
		thisAscender = Font.selectedFontMaster.ascender
		thisDescender = Font.selectedFontMaster.descender
		selectedLayers = Font.selectedLayers
		
		for thisLayer in selectedLayers:
			if index==0:
				# posY：Y coordinate. Top and bottom center of the body.
				posY = getVertWidth(thisLayer) / 2 + thisDescender
				thisWidth = thisLayer.width
				if isTarget1:
					if thisLayer.anchorForName_("LSB"):
						anchor = thisLayer.anchors["LSB"]
						posX_LSB = anchor.position.x-unitValue
						if isLimit:
							if posX_LSB < 0:
								posX_LSB = 0
							elif posX_LSB > thisLayer.bounds.origin.x:
								posX_LSB = thisLayer.bounds.origin.x
						anchor.position = (posX_LSB, posY)
				if isTarget2:
					if thisLayer.anchorForName_("RSB"):
						anchor = thisLayer.anchors["RSB"]
						posX_RSB = anchor.position.x+unitValue
						if isLimit:
							if posX_RSB > thisWidth:
								posX_RSB = thisWidth
							elif posX_RSB < thisLayer.bounds.origin.x + thisLayer.bounds.size.width:
								posX_RSB = thisLayer.bounds.origin.x + thisLayer.bounds.size.width
						anchor.position = (posX_RSB, posY)
			
			elif index==1:
				# posX：X coordinate. Left and right center of the body.
				posX = thisLayer.width/2
				topPos = thisAscender - getVertOrigin(thisLayer)
				bottomPos = topPos - getVertWidth(thisLayer)
				if isTarget1:
					if thisLayer.anchorForName_("TSB"):
						anchor = thisLayer.anchors["TSB"]
						posY_TSB = anchor.position.y+unitValue
						if isLimit:
							if posY_TSB > topPos:
								posY_TSB = topPos
							elif posY_TSB < thisLayer.bounds.origin.y + thisLayer.bounds.size.height:
								posY_TSB = thisLayer.bounds.origin.y + thisLayer.bounds.size.height
						anchor.position = (posX, posY_TSB)
				if isTarget2:
					if thisLayer.anchorForName_("BSB"):
						anchor = thisLayer.anchors["BSB"]
						posY_BSB = anchor.position.y-unitValue
						if isLimit:
							if posY_BSB < bottomPos:
								posY_BSB = bottomPos
							elif posY_BSB > thisLayer.bounds.origin.y:
								posY_BSB = thisLayer.bounds.origin.y
						anchor.position = (posX, posY_BSB)
		
		refreshEditView()
	except Exception as e:
		print traceback.format_exc()
		return


def setAnchors(value1, value2, index, isLimit):
	#if there is no anchor, add a new anchor.
	#if there is anchor, set the position.
	try:
		Font = Glyphs.font
		thisAscender = Font.selectedFontMaster.ascender
		thisDescender = Font.selectedFontMaster.descender
		selectedLayers = Font.selectedLayers

		for thisLayer in selectedLayers:
			
			#Exclude an empty glyph
			if thisLayer.bounds.size.height == 0:
				continue
			
			if index==0:
				# posY：Y coordinate. Top and bottom center of the body.
				posY = getVertWidth(thisLayer) / 2 + thisDescender
				# Width
				thisWidth = thisLayer.width
				# X coordinate
				posX_LSB = thisLayer.bounds.origin.x - value1
				posX_RSB = thisLayer.bounds.origin.x + thisLayer.bounds.size.width + value2
				if isLimit:
					if posX_LSB < 0:
						posX_LSB = 0
					elif posX_LSB > thisLayer.bounds.origin.x:
						posX_LSB = thisLayer.bounds.origin.x
					if posX_RSB > thisWidth:
						posX_RSB = thisWidth
					elif posX_RSB < thisLayer.bounds.origin.x + thisLayer.bounds.size.width:
						posX_RSB = thisLayer.bounds.origin.x + thisLayer.bounds.size.width
				# LSB anchor
				if not thisLayer.anchorForName_("LSB"):
					anchor = GSAnchor.alloc().init()
					anchor.name = "LSB"
					anchor.position = (posX_LSB, posY)
					thisLayer.anchors.append(anchor)
				else:
					anchor = thisLayer.anchors["LSB"]
					anchor.position = (posX_LSB, posY)
				# RSB anchor
				if not thisLayer.anchorForName_("RSB"):
					anchor = GSAnchor.alloc().init()
					anchor.name = "RSB"
					anchor.position = (posX_RSB, posY)
					thisLayer.anchors.append(anchor)
				else:
					anchor = thisLayer.anchors["RSB"]
					anchor.position = (posX_RSB, posY)

			elif index==1:
				# posX：X coordinate. Left and right center of the body.
				posX = thisLayer.width / 2
				# Y coordinate
				posY_TSB = thisLayer.bounds.origin.y + thisLayer.bounds.size.height + value1
				posY_BSB = thisLayer.bounds.origin.y - value2
				if isLimit:
					topPos = thisAscender - getVertOrigin(thisLayer)
					bottomPos = topPos - getVertWidth(thisLayer)
					if posY_TSB > topPos:
						posY_TSB = topPos
					elif posY_TSB < thisLayer.bounds.origin.y + thisLayer.bounds.size.height:
						posY_TSB = thisLayer.bounds.origin.y + thisLayer.bounds.size.height
					if posY_BSB < bottomPos:
						posY_BSB = bottomPos
					if posY_BSB > thisLayer.bounds.origin.y:
						posY_BSB = thisLayer.bounds.origin.y
				# TSB anchor
				if not thisLayer.anchorForName_("TSB"):
					anchor = GSAnchor.alloc().init()
					anchor.name = "TSB"
					anchor.position = (posX, posY_TSB)
					thisLayer.anchors.append(anchor)
				else:
					anchor = thisLayer.anchors["TSB"]
					anchor.position = (posX, posY_TSB)
				# BSB anchor
				if not thisLayer.anchorForName_("BSB"):
					anchor = GSAnchor.alloc().init()
					anchor.name = "BSB"
					anchor.position = (posX, posY_BSB)
					thisLayer.anchors.append(anchor)
				else:
					anchor = thisLayer.anchors["BSB"]
					anchor.position = (posX, posY_BSB)
		
		refreshEditView()
	except Exception as e:
		print traceback.format_exc()
		return


def removeAnchors(index):
	try:
		Font = Glyphs.font
		selectedLayers = Font.selectedLayers
		for thisLayer in selectedLayers:
			if index==0:
				del(thisLayer.anchors["LSB"])
				del(thisLayer.anchors["RSB"])
			elif index==1:
				del(thisLayer.anchors["TSB"])
				del(thisLayer.anchors["BSB"])
		refreshEditView()
	except Exception as e:
		print traceback.format_exc()
		return


def autoAdjustVORG(isReset):
	# Set vertOrigin so that the glyph shape is centered on the body top and bottom (The upper and lower side-bearings are uniform).
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
		print traceback.format_exc()
		return


##################################################
if Glyphs.buildNumber < 1241:
	Glyphs.displayDialog_(Script_Requires)
else:
	Mainwindow()
