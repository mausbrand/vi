# -*- coding: utf-8 -*-
import html5
from priorityqueue import editBoneSelector, viewDelegateSelector, extendedSearchWidgetSelector
from config import conf
from event import EventDispatcher
from i18n import translate

class BooleanViewBoneDelegate( object ):
	def __init__(self, moduleName, boneName, skelStructure, *args, **kwargs ):
		super( BooleanViewBoneDelegate, self ).__init__()
		self.skelStructure = skelStructure
		self.boneName = boneName
		self.moduleName = moduleName

	def render( self, data, field ):
		if field in data.keys():
			return html5.Label(translate(str(data[field])))
		return html5.Label(conf["empty_value"])

class BooleanEditBone( html5.Input ):

	def __init__(self, moduleName, boneName,readOnly, *args, **kwargs ):
		super( BooleanEditBone,  self ).__init__( *args, **kwargs )
		self.boneName = boneName
		self.readOnly = readOnly
		self["type"]="checkbox"
		if readOnly:
			self["disabled"]=True


	@staticmethod
	def fromSkelStructure(moduleName, boneName, skelStructure, *args, **kwargs):
		readOnly = "readonly" in skelStructure[ boneName ].keys() and skelStructure[ boneName ]["readonly"]
		return BooleanEditBone(moduleName, boneName, readOnly)

	def unserialize(self, data, extendedErrorInformation=None):
		if self.boneName in data.keys():
			self._setChecked(data[self.boneName])

	def serializeForPost(self):
		return {self.boneName: str(self._getChecked())}

	def serializeForDocument(self):
		return {self.boneName: self._getChecked()}


class ExtendedBooleanSearch( html5.Div ):
	def __init__(self, extension, view, modul, *args, **kwargs ):
		super( ExtendedBooleanSearch, self ).__init__( *args, **kwargs )
		self.view = view
		self.extension = extension
		self.module = modul
		self.filterChangedEvent = EventDispatcher("filterChanged")
		self.appendChild( html5.TextNode(extension["name"]))
		self.selectionCb = html5.Select()
		self.appendChild( self.selectionCb )
		o = html5.Option()
		o["value"] = ""
		o.appendChild(html5.TextNode(translate("Ignore")))
		self.selectionCb.appendChild(o)
		o = html5.Option()
		o["value"] = "0"
		o.appendChild(html5.TextNode(translate("No")))
		self.selectionCb.appendChild(o)
		o = html5.Option()
		o["value"] = "1"
		o.appendChild(html5.TextNode(translate("Yes")))
		self.selectionCb.appendChild(o)
		self.sinkEvent("onChange")

	def onChange(self, event):
		event.stopPropagation()
		self.filterChangedEvent.fire()


	def updateFilter(self, filter):
		val = self.selectionCb["options"].item(self.selectionCb["selectedIndex"]).value
		if not val:
			if self.extension["target"] in filter.keys():
				del filter[ self.extension["target"] ]
		else:
			filter[ self.extension["target"] ] = val
		return( filter )

	@staticmethod
	def canHandleExtension( extension, view, modul ):
		return( isinstance( extension, dict) and "type" in extension.keys() and (extension["type"]=="boolean" or extension["type"].startswith("boolean.") ) )



def CheckForBooleanBone(moduleName, boneName, skelStucture, *args, **kwargs):
	return skelStucture[boneName]["type"] == "bool"

#Register this Bone in the global queue
editBoneSelector.insert( 3, CheckForBooleanBone, BooleanEditBone)
viewDelegateSelector.insert( 3, CheckForBooleanBone, BooleanViewBoneDelegate)
extendedSearchWidgetSelector.insert( 1, ExtendedBooleanSearch.canHandleExtension, ExtendedBooleanSearch )
