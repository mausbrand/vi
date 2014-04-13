import html5
from network import NetworkService
from priorityqueue import actionDelegateSelector
from widgets.edit import EditWidget
from config import conf
from pane import Pane
from widgets.preview import Preview
from sidebar.internalpreview import InternalPreview
from sidebar.filterselector import FilterSelector
from i18n import translate

class EditPane( Pane ):
	pass

"""
	Provides the actions suitable for list applications
"""
class AddAction( html5.ext.Button ):
	"""
		Allows adding an entry in a list-modul.
	"""
	def __init__(self, *args, **kwargs):
		super( AddAction, self ).__init__(translate("Add"), *args, **kwargs )
		self["class"] = "icon add list"

	@staticmethod
	def isSuitableFor( modul, handler, actionName ):
		if modul is None:
			return( False )
		correctAction = actionName=="add"
		correctHandler = handler == "list" or handler.startswith("list.")
		hasAccess = conf["currentUser"] and ("root" in conf["currentUser"]["access"] or modul+"-add" in conf["currentUser"]["access"])
		isDisabled = modul is not None and "disabledFunctions" in conf["modules"][modul].keys() and conf["modules"][modul]["disabledFunctions"] and "add" in conf["modules"][modul]["disabledFunctions"]
		return(  correctAction and correctHandler and hasAccess and not isDisabled )

	def onClick(self, sender=None):
		pane = EditPane(translate("Add"), closeable=True, iconClasses=["modul_%s" % self.parent().parent().modul, "apptype_list", "action_add" ])
		conf["mainWindow"].stackPane( pane )
		edwg = EditWidget( self.parent().parent().modul, EditWidget.appList)
		pane.addWidget( edwg )
		pane.focus()

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert( 1, AddAction.isSuitableFor, AddAction )


class EditAction( html5.ext.Button ):
	"""
		Allows editing an entry in a list-modul.
	"""
	def __init__(self, *args, **kwargs):
		super( EditAction, self ).__init__( translate("Edit"), *args, **kwargs )
		self["class"] = "icon edit"
		self["disabled"]= True
		self.isDisabled=True

	def onAttach(self):
		super(EditAction,self).onAttach()
		self.parent().parent().selectionChangedEvent.register( self )
		self.parent().parent().selectionActivatedEvent.register( self )

	def onDetach(self):
		self.parent().parent().selectionChangedEvent.unregister( self )
		self.parent().parent().selectionActivatedEvent.unregister( self )
		super(EditAction,self).onDetach()

	def onSelectionChanged(self, table, selection ):
		if len(selection)>0:
			if self.isDisabled:
				self.isDisabled = False
			self["disabled"]= False
		else:
			if not self.isDisabled:
				self["disabled"]= True
				self.isDisabled = True

	def onSelectionActivated(self, table, selection ):
		if not self.parent().parent().isSelector and len(selection)==1:
			self.openEditor( selection[0]["id"] )

	@staticmethod
	def isSuitableFor( modul, handler, actionName ):
		if modul is None:
			return( False )
		correctAction = actionName=="edit"
		correctHandler = handler == "list" or handler.startswith("list.")
		hasAccess = conf["currentUser"] and ("root" in conf["currentUser"]["access"] or modul+"-edit" in conf["currentUser"]["access"])
		isDisabled = modul is not None and "disabledFunctions" in conf["modules"][modul].keys() and conf["modules"][modul]["disabledFunctions"] and "edit" in conf["modules"][modul]["disabledFunctions"]
		return(  correctAction and correctHandler and hasAccess and not isDisabled )

	def onClick(self, sender=None):
		selection = self.parent().parent().getCurrentSelection()
		if not selection:
			return
		for s in selection:
			self.openEditor( s["id"] )

	def openEditor(self, id ):
		selectioname = "%s"
		selection = self.parent().parent().getCurrentSelection()
		if not selection:
			return
		if selection:
			for s in selection:
				if "name" in s.keys() and s["id"]==id:
					selectioname = s["name"]+" (%s)"
		pane = Pane(selectioname % translate("Edit"), closeable=True, iconClasses=["modul_%s" % self.parent().parent().modul, "apptype_list", "action_edit" ])
		conf["mainWindow"].stackPane( pane )
		edwg = EditWidget( self.parent().parent().modul, EditWidget.appList, key=id)
		pane.addWidget( edwg )
		pane.focus()

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert( 1, EditAction.isSuitableFor, EditAction )



class DeleteAction( html5.ext.Button ):
	"""
		Allows deleting an entry in a list-modul.
	"""
	def __init__(self, *args, **kwargs):
		super( DeleteAction, self ).__init__( translate("Delete"), *args, **kwargs )
		self["class"] = "icon delete"
		self["disabled"]= True
		self.isDisabled=True

	def onAttach(self):
		super(DeleteAction,self).onAttach()
		self.parent().parent().selectionChangedEvent.register( self )

	def onDetach(self):
		self.parent().parent().selectionChangedEvent.unregister( self )
		super(DeleteAction,self).onDetach()

	def onSelectionChanged(self, table, selection ):
		if len(selection)>0:
			if self.isDisabled:
				self.isDisabled = False
			self["disabled"]= False
		else:
			if not self.isDisabled:
				self["disabled"]= True
				self.isDisabled = True

	@staticmethod
	def isSuitableFor( modul, handler, actionName ):
		if modul is None:
			return( False )
		correctAction = actionName=="delete"
		correctHandler = handler == "list" or handler.startswith("list.")
		hasAccess = conf["currentUser"] and ("root" in conf["currentUser"]["access"] or modul+"-delete" in conf["currentUser"]["access"])
		isDisabled = modul is not None and "disabledFunctions" in conf["modules"][modul].keys() and conf["modules"][modul]["disabledFunctions"] and "delete" in conf["modules"][modul]["disabledFunctions"]
		return(  correctAction and correctHandler and hasAccess and not isDisabled )


	def onClick(self, sender=None):
		selection = self.parent().parent().getCurrentSelection()
		if not selection:
			return
		d = html5.ext.YesNoDialog(translate("Delete {amt} Entries?",amt=len(selection)) ,title=translate("Delete them?"), yesCallback=self.doDelete, yesLabel=translate("Delete"), noLabel=translate("Keep") )
		d.deleteList = [x["id"] for x in selection]
		d["class"].append( "delete" )

	def doDelete(self, dialog):
		deleteList = dialog.deleteList
		for x in deleteList:
			NetworkService.request( self.parent().parent().modul, "delete", {"id": x}, secure=True, modifies=True )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert( 1, DeleteAction.isSuitableFor, DeleteAction )

class ListPreviewAction( html5.Span ):
	def __init__(self, *args, **kwargs ):
		super( ListPreviewAction, self ).__init__( *args, **kwargs )
		self.urlCb = html5.Select()
		self.appendChild( self.urlCb )
		btn = html5.ext.Button( translate("Preview"), callback=self.onClick )
		btn["class"] = "icon preview"
		self.appendChild(btn)
		self.urls = None

	def onChange(self, event):
		event.stopPropagation()
		newUrl = self.urlCb["options"].item(self.urlCb["selectedIndex"]).value
		self.setUrl( newUrl )

	def rebuildCB(self, *args, **kwargs):
		self.urlCb.element.innerHTML = ""
		for name,url in self.urls.items():
			o = html5.Option()
			o["value"] = url
			o.appendChild(html5.TextNode(name))
			self.urlCb.appendChild(o)
		if len( self.urls.keys() ) == 1:
			self.urlCb["style"]["display"] = "none"
		else:
			self.urlCb["style"]["display"] = ""

	def onAttach(self):
		super(ListPreviewAction,self).onAttach()
		modul = self.parent().parent().modul
		if modul in conf["modules"].keys():
			modulConfig = conf["modules"][modul]
			if "previewurls" in modulConfig.keys() and modulConfig["previewurls"]:
				self.urls = modulConfig["previewurls"]
				self.rebuildCB()


	def onClick(self, sender=None):
		if self.urls is None:
			return
		selection = self.parent().parent().getCurrentSelection()
		if not selection:
			return
		if len( selection )>0:
			if len( self.urls.keys() )==1:
				newUrl = self.urls.values()[0]
			else:
				newUrl = self.urlCb["options"].item(self.urlCb["selectedIndex"]).value
			newUrl = newUrl.replace("{{id}}",selection[0]["id"]).replace("{{modul}}", self.parent().parent().modul )
			if "'" in newUrl:
				return
			print( """var win=window.open('"""+newUrl+"""', 'ViPreview');""" )
			eval("""var win=window.open('"""+newUrl+"""', 'ViPreview');""")
			#widget = Preview( self.urls, selection[0], self.parent().parent().modul )
			#conf["mainWindow"].stackWidget( widget )

	@staticmethod
	def isSuitableFor( modul, handler, actionName ):
		if modul is None:
			return( False )
		correctAction = actionName=="preview"
		correctHandler = handler == "list" or handler.startswith("list.")
		hasAccess = conf["currentUser"] and ("root" in conf["currentUser"]["access"] or modul+"-view" in conf["currentUser"]["access"])
		isDisabled = modul is not None and "disabledFunctions" in conf["modules"][modul].keys() and conf["modules"][modul]["disabledFunctions"] and "view" in conf["modules"][modul]["disabledFunctions"]
		isAvailable = False
		if modul in conf["modules"].keys():
			modulConfig = conf["modules"][modul]
			if "previewurls" in modulConfig.keys() and modulConfig["previewurls"]:
				isAvailable = True
		return(  correctAction and correctHandler and hasAccess and not isDisabled and isAvailable )

actionDelegateSelector.insert( 2, ListPreviewAction.isSuitableFor, ListPreviewAction )


class ListPreviewInlineAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs ):
		super( ListPreviewInlineAction, self ).__init__( translate("Preview"), *args, **kwargs )
		self["class"] = "icon preview"
		self["disabled"] = True
		self.urls = None

	def onAttach(self):
		super( ListPreviewInlineAction,self ).onAttach()
		modul = self.parent().parent().modul
		self.parent().parent().selectionChangedEvent.register( self )
		return

	def onDetach(self):
		self.parent().parent().selectionChangedEvent.unregister( self )
		super( ListPreviewInlineAction, self ).onDetach()


	def onSelectionChanged(self, table, selection):
		if self.parent().parent().isSelector:
			return
		if len(selection)==1:
			preview = InternalPreview( self.parent().parent().modul, self.parent().parent()._structure, selection[0])
			self.parent().parent().sideBar.setWidget( preview )
		else:
			if isinstance( self.parent().parent().sideBar.getWidget(), InternalPreview ):
				self.parent().parent().sideBar.setWidget( None )

	@staticmethod
	def isSuitableFor( modul, handler, actionName ):
		if modul is None:
			return( False )
		correctAction = actionName=="preview"
		correctHandler = handler == "list" or handler.startswith("list.")
		hasAccess = conf["currentUser"] and ("root" in conf["currentUser"]["access"] or modul+"-view" in conf["currentUser"]["access"])
		isDisabled = modul is not None and "disabledFunctions" in conf["modules"][modul].keys() and conf["modules"][modul]["disabledFunctions"] and "view" in conf["modules"][modul]["disabledFunctions"]
		return(  correctAction and correctHandler and hasAccess and not isDisabled )

actionDelegateSelector.insert( 1, ListPreviewInlineAction.isSuitableFor, ListPreviewInlineAction )


class CloseAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs ):
		super( CloseAction, self ).__init__( translate("Close"), *args, **kwargs )
		self["class"] = "icon close"

	def onClick(self, sender=None):
		conf["mainWindow"].removeWidget( self.parent().parent() )

	@staticmethod
	def isSuitableFor( modul, handler, actionName ):
		return( actionName=="close" )

actionDelegateSelector.insert( 1, CloseAction.isSuitableFor, CloseAction )

class ActivateSelectionAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs ):
		super( ActivateSelectionAction, self ).__init__( translate("Select"), *args, **kwargs )
		self["class"] = "icon select"

	def onClick(self, sender=None):
		self.parent().parent().activateCurrentSelection()

	@staticmethod
	def isSuitableFor( modul, handler, actionName ):
		return( actionName=="select" )

actionDelegateSelector.insert( 1, ActivateSelectionAction.isSuitableFor, ActivateSelectionAction )


class SelectFieldsPopup( html5.ext.Popup ):
	def __init__(self, listWdg, *args, **kwargs):
		super( SelectFieldsPopup, self ).__init__( title=translate("Select fields"), *args, **kwargs )
		self["class"].append("selectfields")
		self.listWdg = listWdg
		if self.listWdg._structure:
			for key, bone in self.listWdg._structure:
				chkBox = html5.Input()
				chkBox["type"] = "checkbox"
				chkBox["value"] = key
				self.appendChild(chkBox)
				if key in self.listWdg.getFields():
					chkBox["checked"] = True
				lbl = html5.Label(bone["descr"],forElem=chkBox)
				self.appendChild(lbl)
		else:
			self.close()
			return
		self.applyBtn = html5.ext.Button("Apply", callback=self.doApply)
		self.appendChild(self.applyBtn)


	def doApply(self, *args, **kwargs):
		self.applyBtn["class"].append("is_loading")
		self.applyBtn["disabled"] = True
		res = []
		for c in self._children:
			if isinstance(c,html5.Input) and c["checked"]:
				res.append( c["value"] )
		self.listWdg.setFields( res )
		self.close()

class SelelectFieldsAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs ):
		super( SelelectFieldsAction, self ).__init__( translate("Select fields"), *args, **kwargs )
		self["class"] = "icon selectfields"

	def onClick(self, sender=None):
		SelectFieldsPopup( self.parent().parent() )

	@staticmethod
	def isSuitableFor( modul, handler, actionName ):
		return( actionName=="selectfields" )

actionDelegateSelector.insert( 1, SelelectFieldsAction.isSuitableFor, SelelectFieldsAction )

class ReloadAction( html5.ext.Button ):
	"""
		Allows adding an entry in a list-modul.
	"""
	def __init__(self, *args, **kwargs):
		super( ReloadAction, self ).__init__( translate("Reload"), *args, **kwargs )
		self["class"] = "icon reload"

	@staticmethod
	def isSuitableFor( modul, handler, actionName ):
		correctAction = actionName=="reload"
		correctHandler = handler == "list" or handler.startswith("list.")
		return(  correctAction and correctHandler )

	def onClick(self, sender=None):
		self["class"].append("is_loading")
		NetworkService.notifyChange( self.parent().parent().modul )

	def resetLoadingState(self):
		if "is_loading" in self["class"]:
			self["class"].remove("is_loading")


actionDelegateSelector.insert( 1, ReloadAction.isSuitableFor, ReloadAction )


class ListSelectFilterAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs ):
		super( ListSelectFilterAction, self ).__init__( translate("Select Filter"), *args, **kwargs )
		self["class"] = "icon selectfilter"
		self.urls = None

	def onAttach(self):
		super(ListSelectFilterAction,self).onAttach()
		modul = self.parent().parent().modul
		if modul in conf["modules"].keys():
			modulConfig = conf["modules"][modul]
			print("-------LISTFILTERSELECT----")
			print( modulConfig )


	def onClick(self, sender=None):
		if self.parent().parent().isSelector:
			return
		self.parent().parent().sideBar.setWidget( FilterSelector( self.parent().parent().modul ) )

	@staticmethod
	def isSuitableFor( modul, handler, actionName ):
		if modul is None:
			return( False )
		correctAction = actionName=="selectfilter"
		correctHandler = handler == "list" or handler.startswith("list.")
		hasAccess = conf["currentUser"] and ("root" in conf["currentUser"]["access"] or modul+"-view" in conf["currentUser"]["access"])
		isDisabled = modul is not None and "disabledFunctions" in conf["modules"][modul].keys() and conf["modules"][modul]["disabledFunctions"] and "view" in conf["modules"][modul]["disabledFunctions"]
		return(  correctAction and correctHandler and hasAccess and not isDisabled )

actionDelegateSelector.insert( 1, ListSelectFilterAction.isSuitableFor, ListSelectFilterAction )