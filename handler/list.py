import json
from network import NetworkService
from priorityqueue import HandlerClassSelector, initialHashHandler
from widgets import ListWidget
from config import conf
from pane import Pane
from widgets.edit import EditWidget
from i18n import translate

class ListHandler( Pane ):
	def __init__(self, moduleName, moduleInfo, isView = False, *args, **kwargs):
		icon = "icons/modules/list.svg"
		if "icon" in moduleInfo.keys():
			icon = moduleInfo["icon"]

		super(ListHandler, self).__init__(moduleInfo.get("visibleName", moduleInfo["name"]), icon)

		self.moduleName = moduleName
		self.moduleInfo = moduleInfo

		if "hideInMainBar" in moduleInfo.keys() and moduleInfo["hideInMainBar"]:
			self["style"]["display"] = "none"
		else:
			if "views" in moduleInfo.keys():
				for view in moduleInfo["views"]:
					self.addChildPane(ListHandler(moduleName, view, isView=True))

		if not isView:
			initialHashHandler.insert(1, self.canHandleInitialHash, self.handleInitialHash)

	def canHandleInitialHash(self, pathList, params ):
		if len(pathList)>1:
			if pathList[0]==self.moduleName:
				if pathList[1] in ["add","list"] or (pathList[1]=="edit" and len(pathList)>2):
					return True

		return False

	def handleInitialHash(self, pathList, params):
		assert self.canHandleInitialHash( pathList, params )
		if pathList[1] == "list":
			filter = None
			columns = None
			if "filter" in self.moduleInfo.keys():
				filter = self.moduleInfo["filter"]
			if "columns" in self.moduleInfo.keys():
				columns = self.moduleInfo["columns"]
			self.addWidget( ListWidget( self.moduleName, filter=filter, columns=columns ) )
			self.focus()
		elif pathList[1] == "add":
			pane = Pane(translate("Add"), closeable=True, iconClasses=["modul_%s" % self.moduleName, "apptype_list", "action_add" ])
			edwg = EditWidget( self.moduleName, EditWidget.appList, hashArgs=(params or None) )
			pane.addWidget( edwg )
			conf["mainWindow"].addPane( pane, parentPane=self)
			pane.focus()
		elif pathList[1] == "edit" and len(pathList)>2:
			pane = Pane(translate("Edit"), closeable=True, iconClasses=["modul_%s" % self.moduleName, "apptype_list", "action_edit" ])
			edwg = EditWidget( self.moduleName, EditWidget.appList, key=pathList[2], hashArgs=(params or None))
			pane.addWidget( edwg )
			conf["mainWindow"].addPane( pane, parentPane=self)
			pane.focus()

	@staticmethod
	def canHandle( moduleName, moduleInfo ):
		return moduleInfo["handler"]=="list" or moduleInfo["handler"].startswith("list.")

	def onClick(self, *args, **kwargs):
		if not self.widgetsDomElm.children():
			self.addWidget(ListWidget(self.moduleName,
			                            filter=self.moduleInfo.get("filter"),
			                            columns=self.moduleInfo.get("columns"),
			                            context=self.moduleInfo.get("context"),
			                            filterID=self.moduleInfo.get("__id"),
			                            filterDescr=self.moduleInfo.get("visibleName", "")))

		super(ListHandler, self).onClick(*args, **kwargs)


HandlerClassSelector.insert( 1, ListHandler.canHandle, ListHandler )
