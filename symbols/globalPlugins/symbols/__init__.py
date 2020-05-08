# -*- coding: UTF-8 -*-

import globalPluginHandler
import api
import ui
import wx
import gui
import addonHandler
from gui.settingsDialogs import SettingsDialog
from .symbolsList import Symbols

try:
	from globalCommands import SCRCAT_SPEECH, SCRCAT_TOOLS
except:
	SCRCAT_SPEECH = SCRCAT_TOOLS = None

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	scriptCategory = SCRCAT_SPEECH

	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()

	def onInsertSymbolDialog(self, evt):
		gui.mainFrame._popupSettingsDialog(InsertSymbolDialog)

	def script_insertSymbol(self, gesture):
		self.onInsertSymbolDialog(None)
	script_insertSymbol.category = SCRCAT_TOOLS
	# Translators: Message presented in input help mode.
	script_insertSymbol.__doc__ = _("Shows a dialog to insert a symbol.")

	__gestures = {
		"kb:NVDA+control+4": "insertSymbol",
	}

class InsertSymbolDialog(SettingsDialog):

	# Translators: This is the label for the InsertSymbol dialog.
	title = _("Insert Symbol")

	def makeSettings(self, settingsSizer):
		symbolsListSizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label for a setting in Insert Symbols to select a symbol.
		availableSymbolsLabel = _("Available Symbols")
		symbolsListLabel = wx.StaticText(self,-1,label=u"{labelString} ({labelInt})".format(labelString=availableSymbolsLabel, labelInt=str(len(Symbols))))
		symbolsListSizer.Add(symbolsListLabel)
		symbolsListID = wx.ID_ANY
		# Translators: A combo box to choose a smiley.
		self.symbolsList=wx.Choice(self ,symbolsListID, name=_("Available symbols to insert:"), choices = list(Symbols.keys()), style = 8)
		self.symbolsList.SetSelection(0)
		symbolsListSizer.Add(self.symbolsList)
		settingsSizer.Add(symbolsListSizer, border=10, flag=wx.BOTTOM)

	def postInit(self):
		self.symbolsList.SetFocus()

	def onOk(self,evt):
		#super(InsertSymbolDialog, self).onOk(evt)
		sSymbol = Symbols[self.symbolsList.GetString(self.symbolsList.GetSelection())]
		if api.copyToClip(sSymbol):
			# Translators: This is the message when smiley has been copied to the clipboard.
			wx.CallLater(100, ui.message, _("Symbol copied."))
		else:
			wx.CallLater(100, ui.message, _("Cannot copy symbol."))
