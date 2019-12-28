# encoding: utf-8
#MenuTitle: Fix vrt2 Feature
# 002
# -*- coding: utf-8 -*-
__doc__="""
Add vert code to vrt2 feature.
vrt2フィーチャーにvertのコードを追加する。
"""
from AppKit import NSAlert

##################################################
## Localize - English, Japanese
open_file = Glyphs.localize({ 'en': u'Open a glyphs file.', 'ja': u'glyphs ファイルを開いてください。', })
Done = Glyphs.localize({ 'en': u'Done.', 'ja': u'完了しました。', })
vert_not_exist = Glyphs.localize({ 'en': u'vert feature does not exist.', 'ja': u'vert フィーチャーがありません。', })
vert_empty = Glyphs.localize({ 'en': u'vert feature is empty.', 'ja': u'vert フィーチャーが空です。', })
vrt2_not_exist = Glyphs.localize({ 'en': u'vrt2 feature does not exist.', 'ja': u'vrt2 フィーチャーがありません。', })
Not_generated_vrt2 = Glyphs.localize({ 'en': u'Not automatically generated vrt2 feature.', 'ja': u'自動生成された vrt2 フィーチャーではありません。', })
Requires_vrt2 = Glyphs.localize({ 'en': u'Requires automatically generated vrt2 feature.', 'ja': u'自動生成された vrt2 フィーチャーが必要です。', })
Not_Run = Glyphs.localize({ 'en': u'Did not run.', 'ja': u'実行されませんでした。', })

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
	
	if 'vert' in [ f.name for f in Font.features ]:
		# vert exists
		code_vert = Font.features['vert'].code
		
		if not (not code_vert):
			# vert is not empty
			
			if 'vrt2' in [ f.name for f in Font.features ]:
				# vrt2 exists
				feature_vrt2 = Font.features['vrt2']
				
				if feature_vrt2.automatic == 1: 
					# Automatic generation check ON
					
					# Automatically generate only vrt2
					feature_vrt2.update()
					# Add vert code
					feature_vrt2.code = "# All vert" + '\n' + code_vert + '\n' + "# Automatically generated vrt2" + '\n' + feature_vrt2.code
					# Turn off automatic generation check
					feature_vrt2.automatic = 0
					
					showAlert(Done)
					
				else:
					# Automatic generation check OFF
					showAlert(Not_generated_vrt2, Requires_vrt2)
			else:
				# vrt2 does not exist
				showAlert(vrt2_not_exist, Requires_vrt2)
		else:
			# vert is empty
			showAlert(vert_empty, Not_Run)
	else:
		# vert does not exist
		showAlert(vert_not_exist, Not_Run)

	Font.enableUpdateInterface()
