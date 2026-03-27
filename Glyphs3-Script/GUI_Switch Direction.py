#MenuTitle: パネル：組方向切り替え

# -*- coding: utf-8 -*-
__doc__="""
パネルで編集ビューの組方向を切り替えます。グリフ情報表示も更新。
PythonモジュールのVanillaのインストールが必要です。
"""

import vanilla

##################################################
## Localize - English, Japanese
Direction = Glyphs.localize({ 'en': u'Direction', 'ja': u'組方向', })
H = Glyphs.localize({ 'en': u'H', 'ja': u'ヨコ', })
V = Glyphs.localize({ 'en': u'V', 'ja': u'タテ', })
lang = Glyphs.localize({ 'en': u'en', 'ja': u'ja', })

##################################################
## Class - Mainwindow
class MainWindow(object):
	def __init__(self):
		
		if lang=="ja":
			posX= 10
		else:
			posX= 21
		
		self.w = vanilla.FloatingWindow((120, 28), Direction, autosaveName="com.tama-san.SwitchDirection.mainwindow")
		self.w.radioGroup1 = vanilla.RadioGroup((posX, 0, -10, 28), [H, V], isVertical=False, callback=self.switchAction)
		self.setButtonSelecion()
		# start notification
		Glyphs.addCallback(self.updateInterface_SwitchDirection, UPDATEINTERFACE)
		self.w.open()
	
	def switchAction(self, sender):
		if (Glyphs.font is not None) and (Glyphs.font.currentTab is not None):
			Font = Glyphs.font
			if sender.get()==0:
				Font.currentTab.direction = GSLTR
			else:
				Font.currentTab.direction = GSVertical
			Font.currentTab.textCursor = Font.currentTab.textCursor
	
	def setButtonSelecion(self):
		self.w.radioGroup1.set(0)
		if (Glyphs.font is not None) and (Glyphs.font.currentTab is not None):
			Font = Glyphs.font
			if Font.currentTab.direction == GSVertical:
				self.w.radioGroup1.set(1)
			Font.currentTab.textCursor = Font.currentTab.textCursor

	def updateInterface_SwitchDirection(self, layer=None, info=None, sender=None):
		try:
			if (Glyphs.font is not None) and (Glyphs.font.currentTab is not None):
				Font = Glyphs.font
				if Font.currentTab.direction == GSLTR:
					self.w.radioGroup1.set(0)
				elif Font.currentTab.direction == GSVertical:
					self.w.radioGroup1.set(1)
		except Exception as e:
			print(traceback.format_exc())
			return
			
##################################################
MainWindow()
