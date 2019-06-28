# encoding: utf-8
#MenuTitle: Switch Direction JP
# v1.0.3
# -*- coding: utf-8 -*-
__doc__="""
専用パネルで編集ビューの組方向を切り替える。その際にグリフ情報表示を更新する。
"""
import vanilla

class MainWindow(object):
	def __init__(self):
		self.w = vanilla.FloatingWindow((120, 28), u"組方向", autosaveName="com.tama-san.SwitchDirection.mainwindow")
		
		self.w.radioGroup1 = vanilla.RadioGroup((10, 0, 100, 28), [u"ヨコ", u"タテ"], isVertical=False, callback=self.switchAction)
		
		self.setButtonSelecion()
		self.w.open()
	
	
	def switchAction(self, sender):
		# ボタン選択に合わせて組方向を切り替える
		# callback専用
		if (Glyphs.font is not None) and (Glyphs.font.currentTab is not None):
			Font = Glyphs.font
			if sender.get()==0:
				Font.currentTab.direction = LTR
			else:
				Font.currentTab.direction = RTLTTB
			 # グリフ情報表示を更新
			Font.currentTab.textCursor = Font.currentTab.textCursor

	def setButtonSelecion(self):
		# 現在の組方向に合わせてボタン選択を切り替える
		self.w.radioGroup1.set(0)
		if (Glyphs.font is not None) and (Glyphs.font.currentTab is not None):
			Font = Glyphs.font
			if Font.currentTab.direction == RTLTTB:
				self.w.radioGroup1.set(1)
			# グリフ情報表示を更新
			Font.currentTab.textCursor = Font.currentTab.textCursor


##################################################
MainWindow()
