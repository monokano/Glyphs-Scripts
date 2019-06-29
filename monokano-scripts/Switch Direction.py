# encoding: utf-8
#MenuTitle: Switch Direction
# 004
# -*- coding: utf-8 -*-
__doc__="""
Toggle the writing direction of Edit View in the panel to update the glyph information display.
パネルで編集ビューの組方向を切り替え、グリフ情報表示を更新する。
"""
import vanilla

##################################################
## Localize - English, Japanese
Direction = Glyphs.localize({ 'en': u'Direction', 'ja': u'組方向', })
H = Glyphs.localize({ 'en': u'H', 'ja': u'ヨコ', })
V = Glyphs.localize({ 'en': u'V', 'ja': u'タテ', })

##################################################
## Class - Mainwindow
class MainWindow(object):
	def __init__(self):
		self.w = vanilla.FloatingWindow((120, 28), Direction, autosaveName="com.tama-san.SwitchDirection.mainwindow")
		self.w.radioGroup1 = vanilla.RadioGroup((10, 0, 100, 28), [H, V], isVertical=False, callback=self.switchAction)
		self.setButtonSelecion()
		self.w.open()
	
	def switchAction(self, sender):
		if (Glyphs.font is not None) and (Glyphs.font.currentTab is not None):
			Font = Glyphs.font
			if sender.get()==0:
				Font.currentTab.direction = LTR
			else:
				Font.currentTab.direction = RTLTTB
			Font.currentTab.textCursor = Font.currentTab.textCursor

	def setButtonSelecion(self):
		self.w.radioGroup1.set(0)
		if (Glyphs.font is not None) and (Glyphs.font.currentTab is not None):
			Font = Glyphs.font
			if Font.currentTab.direction == RTLTTB:
				self.w.radioGroup1.set(1)
			Font.currentTab.textCursor = Font.currentTab.textCursor

##################################################
MainWindow()
