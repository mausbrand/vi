# -*- coding: utf-8 -*-
import html5, re
from widgets.actionbar import ActionBar
from widgets.file import FileWidget

from event import EventDispatcher
from priorityqueue import actionDelegateSelector
from config import conf
from i18n import translate
from network import DeferredCall

class BasicEditorAction(html5.ext.Button):
	cmd = None
	name = None
	value = True
	title = None

	isActiveTag = None

	def __init__(self, *args, **kwargs):
		super(BasicEditorAction, self).__init__(self.cmd, *args, **kwargs)

		self.removeClass("button") # dont use default button class here
		self.addClass("btn-vTextedit", self.cmd) #, "ql-%s" % self.name)

		if self.title:
			self["title"] = self.title
		
		self.setText('<img src="/vi/s/icons/actions/text/' + self.cmd + '.svg">')

	def getQuill(self):
		return self.parent().parent().editor.quill

	def onClick(self, sender = None):
		q = self.getQuill()

		fmt = q.getFormat()

		value = getattr(fmt, self.name, not self.value)
		if value == self.value:
			value = not value
		else:
			value = self.value

		print(self.name, value)
		q.format(self.name, value)

	def onAttach(self):
		self.parent().parent().editor.editorChangeEvent.register(self)

	def onDetach(self):
		self.parent().parent().editor.editorChangeEvent.unregister(self)

	def onEditorChange(self):
		try:
			fmt = self.getQuill().getFormat()
		except:
			return
		
		self.removeClass("is-active")
		if getattr(fmt, self.name, None):
			value = getattr(fmt, self.name, None)
			if value == "True" or self.value == value and self.name != "indent":
				self.addClass("is-active")


class TextStyleBold(BasicEditorAction):
	name = cmd = "bold"
	title = translate("Bold")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.bold", TextStyleBold)

class TextStyleItalic(BasicEditorAction):
	name = cmd = "italic"
	title = translate("Italic")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.italic", TextStyleItalic )

class TextStyleSuper(BasicEditorAction):
	cmd = "Super"
	name = "subsuper"
	value = "Sup"
	title = translate("Super")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.super", TextStyleSuper )

class TextStyleSub(BasicEditorAction):
	cmd = "Sub"
	name = "subsuper"
	value = "Sub"
	title = translate("Sub")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.sub", TextStyleSub )

class TextStyleH1(BasicEditorAction):
	cmd = "H1"
	name = "header"
	value = 1
	title = translate("H1")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.h1", TextStyleH1 )

class TextStyleH2(BasicEditorAction):
	cmd = "H2"
	name = "header"
	value = 2
	title = translate("H2")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.h2", TextStyleH2 )

class TextStyleH3(BasicEditorAction):
	cmd = "H3"
	name = "header"
	value = 3
	title = translate("H3")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.h3", TextStyleH3 )

class TextStyleH4(BasicEditorAction):
	cmd = "H4"
	name = "header"
	value = 4
	title = translate("H4")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.h4", TextStyleH4 )

class TextStyleBlockQuote(BasicEditorAction):
	name = cmd = "blockquote"
	title = translate("Blockqoute")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.blockquote", TextStyleBlockQuote )

class TextStyleJustifyCenter(BasicEditorAction):
	cmd = "justifyCenter"
	name = "align"
	value = "Center"
	title = translate("Justifiy Center")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.justifyCenter", TextStyleJustifyCenter )

class TextStyleJustifyLeft(BasicEditorAction):
	cmd = "justifyLeft"
	name = "align"
	value = "Left"
	title = translate("Justifiy Left")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.justifyLeft", TextStyleJustifyLeft )

class TextStyleJustifyRight(BasicEditorAction):
	cmd = "justifyRight"
	name = "align"
	value = "Right"
	title = translate("Justifiy Right")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.justifyRight", TextStyleJustifyRight )

class TextStyleJustifyRight(BasicEditorAction):
	cmd = "justifyBlock"
	name = "align"
	value = "Justify"
	title = translate("Justifiy Full")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.justifyBlock", TextStyleJustifyRight )

class TextInsertOrderedList(BasicEditorAction):
	cmd = "insertOrderedList"
	name = "list"
	value = "ordered"
	title = translate("Insert an ordered List")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.orderedList", TextInsertOrderedList )

class TextInsertUnorderedList(BasicEditorAction):
	cmd = "insertUnorderedList"
	name = "list"
	value = "bullet"
	title = translate("Insert an unordered List")
actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.unorderedList", TextInsertUnorderedList )

class TextOutdent(BasicEditorAction):
	cmd = "outdent"
	name = "indent"
	value = "-1"
	title = translate("Indent less")

	def onClick(self, sender = None):
		q = self.getQuill()
		fmt = q.getFormat()
		value = getattr(fmt, self.name, "0")
		r = q.getSelection()

	   	q.formatLine(r.index, r.length, "indent", int(value) - 1)

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.outdent", TextOutdent )

class TextIndent(BasicEditorAction):
	name = cmd = "indent"
	value = "+1"
	title = translate("Indent more")


	def onClick(self, sender = None):
		q = self.getQuill()
		fmt = q.getFormat()
		value = getattr(fmt, self.name, "0")
		r = q.getSelection()

	   	q.formatLine(r.index, r.length, "indent", int(value) + 1)

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.indent", TextIndent )

class TextRemoveFormat(BasicEditorAction):
	cmd = "removeformat"
	name = "clean"
	title = translate("Remove all formatting")

	def onClick(self, sender = None):
		q = self.getQuill()

		r = q.getSelection()
		if r.length > 0:
		   	q.removeFormat(r.index, r.length, "user")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.removeformat", TextRemoveFormat )


#FIXME:
class TextInsertImageAction(BasicEditorAction):
	name = cmd = "image"
	title = translate("Insert Image")

	def onClick(self, sender=None):
		currentSelector = FileWidget( "file", isSelector=True )
		currentSelector.selectionActivatedEvent.register( self )
		conf["mainWindow"].stackWidget( currentSelector )

	def onSelectionActivated(self, selectWdg, selection):
		print("onSelectionActivated")

		if not selection:
			return

		print(selection)

		for item in selection:
			dataUrl = "/file/download/%s/%s" % (item.data["dlkey"], item.data["name"].replace("\"",""))
			if "mimetype" in item.data.keys() and item.data["mimetype"].startswith("image/"):
				self.execCommand("insertImage", dataUrl)
			else:
				self.execCommand("createLink", dataUrl + "?download=1")

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.image" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TextInsertImageAction.isSuitableFor, TextInsertImageAction )



class TextInsertLinkAction(BasicEditorAction):
	name = cmd = "link"

	newLinkIdx = 0

	def onClick(self, sender=None):
		href = getattr(self.getQuill().getFormat(), self.name, "")
		html5.ext.InputDialog("URL", successHandler=self.onLinkAvailable, value=href)

	def onLinkAvailable(self, dialog, href):
		self.getQuill().format("link", href)

	def createLink(self, dialog, value):
		if value:
			self.parent().parent().editor.focus()

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.link" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TextInsertLinkAction.isSuitableFor, TextInsertLinkAction )


'''
class CreateTablePopup( html5.ext.Popup ):
	def __init__(self, targetNode, *args, **kwargs ):
		super( CreateTablePopup, self ).__init__( *args, **kwargs )
		assert targetNode

		while not "innerHTML" in dir(targetNode):
			targetNode = targetNode.parentNode

		self.targetNode = targetNode
		self["class"].append("createtable")
		self.rowInput = html5.Input()
		self.rowInput["type"] = "number"
		self.rowInput["value"] = 3
		self.appendChild( self.rowInput )
		l = html5.Label(translate("Rows"), forElem=self.rowInput)
		l["class"].append("rowlbl")
		self.appendChild( l )
		self.colInput = html5.Input()
		self.colInput["type"] = "number"
		self.colInput["value"] = 4
		self.appendChild( self.colInput )
		l = html5.Label(translate("Cols"), forElem=self.colInput)
		l["class"].append("collbl")
		self.appendChild( l )
		self.insertHeader = html5.Input()
		self.insertHeader["type"] = "checkbox"
		self.appendChild( self.insertHeader )
		l = html5.Label(translate("Insert Table Header"), forElem=self.insertHeader)
		l["class"].append("headerlbl")
		self.appendChild( l )
		self.appendChild( html5.ext.Button( "Cancel", callback=self.doClose ) )
		self.appendChild( html5.ext.Button( "Create", callback=self.createTable ) )

	def doClose(self, *args, **kwargs):
		self.targetNode = None
		self.close()

	def createTable(self, *args, **kwargs):
		rows = int(self.rowInput["value"])
		cols = int(self.colInput["value"])
		insertHeader = self.insertHeader["checked"]
		innerHtml = "<table>"
		if insertHeader:
			innerHtml += "<thead>"
			for c in range(0,cols):
				innerHtml += "<th>&nbsp;</th>"
			innerHtml += "</thead>"
		for x in range(0,rows):
			innerHtml += "<tr>"
			for y in range(0,cols):
				innerHtml += "<td>%s - %s</td>" % (x,y)
			innerHtml += "</tr>"
		innerHtml += "</table>"
		self.targetNode.innerHTML = self.targetNode.innerHTML+innerHtml
		self.doClose()

class TextInsertTableAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TextInsertTableAction, self ).__init__( translate("Insert Table"), *args, **kwargs )
		self["class"] = "icon text table"
		self["title"] = translate("Insert Table")

	def onClick(self, sender=None):
		self.parent().parent().editor.focus()
		node = eval("window.top.getSelection().anchorNode")

		if node:
			CreateTablePopup( node )

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.table" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TextInsertTableAction.isSuitableFor, TextInsertTableAction )

class TableInsertRowBeforeAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TableInsertRowBeforeAction, self ).__init__( translate("Insert Table Row before"), *args, **kwargs )
		self["class"] = "icon text table newrow before"
		self["title"] = translate("Insert Table Row before")

	def onClick(self, sender=None):
		node = eval("window.top.getSelection().anchorNode")
		i = 10
		while i>0 and node and node != self.parent().parent().editor.element:
			i -= 1
			if not "tagName" in dir( node ):
				node = node.parentNode
				continue
			if node.tagName=="TR":
				tr = html5.document.createElement("tr")
				for c in range(0,node.children.length):
					td = html5.document.createElement("td")
					tr.appendChild( td )
				node.parentNode.insertBefore( tr, node )
				return
			node = node.parentNode

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.table.newrow.before" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TableInsertRowBeforeAction.isSuitableFor, TableInsertRowBeforeAction )

class TableInsertRowAfterAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TableInsertRowAfterAction, self ).__init__( translate("Insert Table Row after"), *args, **kwargs )
		self["class"] = "icon text table newrow after"
		self["title"] = translate("Insert Table Row after")

	def onClick(self, sender=None):
		node = eval("window.top.getSelection().anchorNode")
		i = 10
		while i>0 and node and node != self.parent().parent().editor.element:
			i -= 1
			if not "tagName" in dir( node ):
				node = node.parentNode
				continue
			if node.tagName=="TR":
				tr = html5.document.createElement("tr")
				for c in range(0,node.children.length):
					td = html5.document.createElement("td")
					tr.appendChild( td )
				if node.nextSibling:
					node.parentNode.insertBefore( tr, node.nextSibling )
				else:
					node.parentNode.appendChild( tr )
				return
			node = node.parentNode

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.table.newrow.after" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TableInsertRowAfterAction.isSuitableFor, TableInsertRowAfterAction )

class TableInsertColBeforeAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TableInsertColBeforeAction, self ).__init__( translate("Insert Table Col before"), *args, **kwargs )
		self["class"] = "icon text table newcol before"
		self["title"] = translate("Insert Table Col before")

	def onClick(self, sender=None):
		node = eval("window.top.getSelection().anchorNode")
		td = None
		tr = None
		table = None
		i = 10
		#Try to extract the relevat nodes from the dom
		while i>0 and node and node != self.parent().parent().editor.element:
			i -= 1
			if not "tagName" in dir( node ):
				node = node.parentNode
				continue
			if node.tagName=="TD":
				td = node
			elif node.tagName=="TR":
				tr = node
			elif node.tagName=="TABLE":
				table = node
				break
			node = node.parentNode
		if td and tr and table:
			cellIdx = 0 # Before which column shall we insert a new col?
			for x in range(0, tr.children.length):
				if td==tr.children.item(x):
					break
				cellIdx += 1
			for trChildIdx in range(0,table.children.length):
				trChild = table.children.item(trChildIdx)
				if not "tagName" in dir( trChild ):
					continue
				if trChild.tagName=="THEAD":
					#Fix the table head
					for childIdx in range(0,trChild.children.length):
						child = trChild.children.item(childIdx)
						if not "tagName" in dir( child ):
							continue
						if child.tagName=="TR":
							newTd = html5.document.createElement("th")
							child.insertBefore( newTd, child.children.item(cellIdx) )
				elif trChild.tagName=="TBODY":
					#Fix all rows in the body
					for childIdx in range(0,trChild.children.length):
						child = trChild.children.item(childIdx)
						if not "tagName" in dir( child ):
							continue
						if child.tagName=="TR":
							newTd = html5.document.createElement("td")
							child.insertBefore( newTd, child.children.item(cellIdx) )

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.table.newcol.before" )

	def resetLoadingState(self):
		pass


actionDelegateSelector.insert(1, TableInsertColBeforeAction.isSuitableFor, TableInsertColBeforeAction )

class TableInsertColAfterAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TableInsertColAfterAction, self ).__init__( translate("Insert Table Col after"), *args, **kwargs )
		self["class"] = "icon text table newcol after"
		self["title"] = translate("Insert Table Col after")

	def onClick(self, sender=None):
		node = eval("window.top.getSelection().anchorNode")
		td = None
		tr = None
		table = None
		i = 10
		#Try to extract the relevat nodes from the dom
		while i>0 and node and node != self.parent().parent().editor.element:
			i -= 1
			if not "tagName" in dir( node ):
				node = node.parentNode
				continue
			if node.tagName=="TD":
				td = node
			elif node.tagName=="TR":
				tr = node
			elif node.tagName=="TABLE":
				table = node
				break
			node = node.parentNode
		if td and tr and table:
			cellIdx = 0 # Before which column shall we insert a new col?
			for x in range(0, tr.children.length):
				if td==tr.children.item(x):
					break
				cellIdx += 1
			for trChildIdx in range(0,table.children.length):
				trChild = table.children.item(trChildIdx)
				if not "tagName" in dir( trChild ):
					continue
				if trChild.tagName=="THEAD":
					#Fix the table head
					for childIdx in range(0,trChild.children.length):
						child = trChild.children.item(childIdx)
						if not "tagName" in dir( child ):
							continue
						if child.tagName=="TR":
							newTd = html5.document.createElement("th")
							if cellIdx+1<child.children.length:
								child.insertBefore( newTd, child.children.item(cellIdx+1) )
							else:
								child.appendChild( newTd )
				elif trChild.tagName=="TBODY":
					#Fix all rows in the body
					for childIdx in range(0,trChild.children.length):
						child = trChild.children.item(childIdx)
						if not "tagName" in dir( child ):
							continue
						if child.tagName=="TR":
							newTd = html5.document.createElement("td")
							if cellIdx+1<child.children.length:
								child.insertBefore( newTd, child.children.item(cellIdx+1) )
							else:
								child.appendChild( newTd )

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.table.newcol.after" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TableInsertColAfterAction.isSuitableFor, TableInsertColAfterAction )


class TableRemoveRowAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TableRemoveRowAction, self ).__init__( translate("Remove Table Row"), *args, **kwargs )
		self["class"] = "icon text table remove row"
		self["title"] = translate("Remove Table Row")

	def onClick(self, sender=None):
		node = eval("window.top.getSelection().anchorNode")
		i = 10
		while i>0 and node and node != self.parent().parent().editor.element:
			i -= 1
			if not "tagName" in dir( node ):
				node = node.parentNode
				continue
			if node.tagName=="TR":
				node.parentNode.removeChild(node)
				return
			node = node.parentNode

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.table.remove.row" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TableRemoveRowAction.isSuitableFor, TableRemoveRowAction )



class TableRemoveColAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TableRemoveColAction, self ).__init__( translate("Remove Table Col"), *args, **kwargs )
		self["class"] = "icon text table remove col"
		self["title"] = translate("Remove Table Col")

	def onClick(self, sender=None):
		node = eval("window.top.getSelection().anchorNode")
		td = None
		tr = None
		table = None
		i = 10
		#Try to extract the relevat nodes from the dom
		while i>0 and node and node != self.parent().parent().editor.element:
			i -= 1
			if not "tagName" in dir( node ):
				node = node.parentNode
				continue
			if node.tagName=="TD":
				td = node
			elif node.tagName=="TR":
				tr = node
			elif node.tagName=="TABLE":
				table = node
				break
			node = node.parentNode
		if td and tr and table:
			cellIdx = 0 # Which column shall we delete?
			for x in range(0, tr.children.length):
				if td==tr.children.item(x):
					break
				cellIdx += 1
			for trChildIdx in range(0,table.children.length):
				trChild = table.children.item(trChildIdx)
				if not "tagName" in dir( trChild ):
					continue
				if trChild.tagName=="THEAD":
					#Fix the table head
					for childIdx in range(0,trChild.children.length):
						child = trChild.children.item(childIdx)
						if not "tagName" in dir( child ):
							continue
						if child.tagName=="TR":
							child.removeChild(child.children.item(cellIdx))
				elif trChild.tagName=="TBODY":
					#Fix all rows in the body
					for childIdx in range(0,trChild.children.length):
						child = trChild.children.item(childIdx)
						if not "tagName" in dir( child ):
							continue
						if child.tagName=="TR":
							child.removeChild(child.children.item(cellIdx))

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.table.remove.col" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TableRemoveColAction.isSuitableFor, TableRemoveColAction )
'''

class TextSaveAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TextSaveAction, self ).__init__( translate("Save"), *args, **kwargs )
		self["class"] = "btn-vTextedit save f-right"
		self["title"] = translate("Save")
		self.setText('<img src="/vi/s/icons/actions/text/save.svg">')

	def onClick(self, event):
		self.parent().parent().saveText()

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.save" )

actionDelegateSelector.insert(1, TextSaveAction.isSuitableFor, TextSaveAction )

class TextAbortAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TextAbortAction, self ).__init__( translate("Abort"), *args, **kwargs )
		self["class"] = "btn-vTextedit abort f-right"
		self["title"] = translate("Abort")
		self.setText('<img src="/vi/s/icons/actions/text/cancel.svg">')

	def onClick(self, event):
		if self.parent().parent().editor.changed():
			html5.ext.popup.YesNoDialog(translate("Any changes will be lost. Do you really want to abort?"),
			                            yesCallback=self.doAbort)
		else:
			self.doAbort()

	def doAbort(self, *args, **kwargs):
		self.parent().parent().abortText()

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.abort" )

actionDelegateSelector.insert(1, TextAbortAction.isSuitableFor, TextAbortAction )

class LinkEditor( html5.Div ):
	newLinkIdx = 0
	def __init__(self, *args, **kwargs):
		super( LinkEditor, self ).__init__( *args, **kwargs )
		self["class"].append("linkeditor")
		self["style"]["display"] = "none"
		self.linkTxt = html5.Input()
		self.linkTxt["type"] = "text"
		self.appendChild(self.linkTxt)
		l = html5.Label(translate("URL"), forElem=self.linkTxt)
		l["class"].append("urllbl")
		self.appendChild( l )
		self.newTab = html5.Input()
		self.newTab["type"] = "checkbox"
		self.appendChild(self.newTab)
		l = html5.Label(translate("New window"), forElem=self.newTab)
		l["class"].append("newwindowlbl")
		self.appendChild( l )
		self.caller = None

	def getAFromTagStack(self, tagStack):
		for elem in tagStack:
			if not "tagName" in dir(elem):
				continue
			if elem.tagName=="A":
				return( elem )
		return( None )

	def onCursorMoved(self, tagStack):
		newElem = self.getAFromTagStack(tagStack)
		if newElem is not None and self.currentElem is not None:
			self.doClose()
			self.doOpen( newElem )
		elif self.currentElem is None and newElem is not None:
			self.doOpen( newElem )
		elif self.currentElem is not None and newElem is None:
			self.doClose()

	def doOpen(self, caller, href):
		self.caller = caller
		self.linkTxt["value"] = href
		#self.newTab["checked"] = self.currentElem.target=="_blank"

		self.isOpen = True
		self["style"]["display"] = "block"

	def doClose(self):
		self.caller.onLinkAvailable(self.linkTxt["value"])

		#if self.newTab["checked"]:
		#	self.currentElem.target = "_blank"
		#else:
		#	self.currentElem.target = "_self"

		self["style"]["display"] = "none"
		self.caller = None

	def findHref(self, linkTarget, elem):
		if "tagName" in dir(elem):
			if elem.tagName == "A":
				if elem.href == linkTarget or elem.href.endswith(linkTarget):
					return( elem )
		if "children" in dir(elem):
			for x in range(0,elem.children.length):
				child = elem.children.item(x)
				r = self.findHref( linkTarget, child)
				if r is not None:
					return( r )
		return( None )

	def openLink(self, caller, href = ""):
		self.doOpen(caller, href)
		self.linkTxt["value"] = ""
		self.linkTxt.focus()


class ImageEditor( html5.Div ):
	def __init__(self, *args, **kwargs):
		super( ImageEditor, self ).__init__( *args, **kwargs )
		self["class"].append("imageeditor")
		self["style"]["display"] = "none"
		self.widthInput = html5.Input()
		self.widthInput["type"] = "number"
		self.appendChild(self.widthInput)
		l = html5.Label(translate("Width"), self.widthInput)
		l["class"].append("widthlbl")
		self.appendChild( l )
		self.keepAspectRatio = html5.Input()
		self.keepAspectRatio["type"] = "checkbox"
		self.appendChild( self.keepAspectRatio )
		l = html5.Label(translate("Keep aspect ratio"), self.keepAspectRatio)
		l["class"].append("aspectlbl")
		self.appendChild( l )
		self.heightInput = html5.Input()
		self.heightInput["type"] = "number"
		self.appendChild(self.heightInput)
		l = html5.Label(translate("Height"), self.heightInput)
		l["class"].append("heightlbl")
		self.appendChild( l )
		self.titleInput = html5.Input()
		self.titleInput["type"] = "text"
		self.appendChild(self.titleInput)
		l = html5.Label(translate("Title"), self.titleInput)
		l["class"].append("titlelbl")
		self.appendChild( l )
		self.currentElem = None
		self.sinkEvent("onChange")

	def onChange(self, event):
		super(ImageEditor,self).onChange( event )
		aspect = self.currentElem.naturalWidth/self.currentElem.naturalHeight
		if event.target == self.widthInput.element:
			if self.keepAspectRatio["checked"]:
				self.heightInput["value"] = int(float(self.widthInput["value"])/aspect)
		elif event.target == self.heightInput.element:
			if self.keepAspectRatio["checked"]:
				self.widthInput["value"] = int(float(self.heightInput["value"])*aspect)
		self.currentElem.width = int(self.widthInput["value"])
		self.currentElem.height = int(self.heightInput["value"])

	def getImgFromTagStack(self, tagStack):
		for elem in tagStack:
			if not "tagName" in dir(elem):
				continue
			if elem.tagName=="IMG":
				return( elem )
		return( None )

	def onCursorMoved(self, tagStack):
		newElem = self.getImgFromTagStack(tagStack)
		if newElem is not None and self.currentElem is not None:
			self.doClose()
			self.doOpen( newElem )
		elif self.currentElem is None and newElem is not None:
			self.doOpen( newElem )
		elif self.currentElem is not None and newElem is None:
			self.doClose()

	def doOpen(self, elem):
		self.currentElem = elem
		self["style"]["display"] = ""
		self.heightInput["value"] = elem.height
		self.widthInput["value"] = elem.width
		self.titleInput["value"] = elem.title

	def doClose(self):
		if self.currentElem is None:
			return
		self.currentElem.width = int( self.widthInput["value"] )
		self.currentElem.height = int( self.heightInput["value"] )
		self.currentElem.title = self.titleInput["value"]
		self["style"]["display"] = "none"
		self.currentElem = None

	def findImg(self, linkTarget, elem):
		if "tagName" in dir(elem):
			if elem.tagName == "IMG":
				if elem.href == linkTarget or elem.href.endswith(linkTarget):
					return( elem )
		if "children" in dir(elem):
			for x in range(0,elem.children.length):
				child = elem.children.item(x)
				r = self.findImg( linkTarget, child)
				if r is not None:
					return( r )
		return( None )

	def openLink(self, linkTarget):
		self.doOpen( self.findHref( linkTarget, self.parent().editor.element ) )
		self.linkTxt["value"] = ""
		self.linkTxt.focus()


class TextUndoAction(BasicEditorAction):
	cmd = "undo"
	title = translate("Undo the last action")

	def onClick(self, sender = None):
		self.parent().parent().editor.quill.history.undo()

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.undo", TextUndoAction )

class TextRedoAction( BasicEditorAction ):
	cmd = "redo"
	title = translate("Redo the last undone action")

	def onClick(self, sender=None):
		self.parent().parent().editor.quill.history.redo()

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.redo", TextRedoAction )




class FlipViewAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( FlipViewAction, self ).__init__( translate("Flip View"), *args, **kwargs )
		self["class"] = "btn-vTextedit flipview"
		self["title"] = translate("Flip View")
		self.setText('<img src="/vi/s/icons/actions/text/code.svg">')

	def onAttach(self):
		super( FlipViewAction, self ).onAttach()
		if self.parent().parent().isWysiwygMode:
			self["class"].append("is_wysiwyg")
		else:
			self["class"].append("is_htmlview")

	def onClick(self, sender=None):
		if "is_wysiwyg" in self["class"]:
			self["class"].remove("is_wysiwyg")
		if "is_htmlview" in self["class"]:
			self["class"].remove("is_htmlview")

		if self.parent().parent().flipView():
			self["class"].append("is_wysiwyg")
		else:
			self["class"].append("is_htmlview")

	def resetLoadingState(self):
		pass
actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.flipView", FlipViewAction )




def dumpNode(obj):
	try:
		print("obj", obj)
		print("type", obj.nodeType)
		print("child", obj.childElementCount)

		div = html5.Div()
		div.element.appendChild(obj.cloneNode(True))
		print("html", div.element.innerHTML)
		print("children", div.element.childNodes.length)
		print("children[1]", obj.childNodes.length)
	except:
		print("ERROR DUMPING %s" % obj)


class Editor(html5.Div):
	__editorCount__ = 0

	def __init__(self, parent, html, *args, **kwargs ):
		super(Editor, self).__init__(*args, **kwargs)
		self.addClass("contentdiv")

		self["id"] = "wysiwyg%d" % Editor.__editorCount__
		Editor.__editorCount__ += 1

		self.initial_txt = self.element.innerHTML = html
		self.sinkEvent("onBlur", "onFocus")
		parent.appendChild(self)
		self.quill = None

		self.editorChangeEvent = EventDispatcher("editorChange")
		DeferredCall(self.init)

	def init(self):
		self.quill = eval("""
					new window.top.quill("#%s",
						{

							modules:
							{
								toolbar: "#%s",
							}
						})
					""" % (self["id"], self.parent().actionbar["id"]))

		self.quill.on("editor-change", self.updateActionBar)

	def changed(self):
		return self.initial_txt != self.element.innerHTML

	def updateActionBar(self, *args, **kwargs):
		print("CHANGE!")
		print(args)
		print(kwargs)
		self.editorChangeEvent.fire()

	def execCommand(self, commandName, valueArgument=None):
		"""
		Wraps the document.execCommand() function for easier usage.
		"""

		if valueArgument is None:
			valueArgument = "null"
		else:
			valueArgument = "\"%s\"" % str(valueArgument)

		print("execCommand(\"%s\", false, %s)" % (commandName, valueArgument))
		return bool(eval("window.top.document.execCommand(\"%s\", false, %s)" % (commandName, valueArgument)))


class Wysiwyg( html5.Div ):
	def __init__(self, editHtml, actionBarHint=translate("Text Editor"), *args, **kwargs ):
		super( Wysiwyg, self ).__init__(*args, **kwargs)
		self.cursorMovedEvent = EventDispatcher("cursorMoved")
		self.saveTextEvent = EventDispatcher("saveText")
		self.abortTextEvent = EventDispatcher("abortText")
		self.textActions = ["text.undo",
							"text.redo",
							"text.removeformat",
							"text.flipView",
							"style.text.bold",
							"style.text.italic",
							"style.text.super",
							"style.text.sub"]+\
						   [("style.text.h%s" % x) for x in range(1, 4+1)]+\
						   ["style.text.blockquote",
							"style.text.justifyLeft",
							"style.text.justifyCenter",
							"style.text.justifyRight",
							"style.text.justifyBlock",
							"text.orderedList",
							"text.unorderedList",
							"text.outdent",
							"text.indent",
							"text.image",
							"text.link",
							"text.table",
							"text.abort",
							"text.save"]

		#self["type"] = "text"
		self.actionbar = ActionBar(None, None, actionBarHint)
		self.isWysiwygMode = True
		self.discardNextClickEvent = False
		self.appendChild( self.actionbar )
		self.tableDiv = html5.Div()
		self.tableDiv["class"].append("tableeditor")
		self.appendChild(self.tableDiv)
		for c in [TableInsertRowBeforeAction,TableInsertRowAfterAction,TableInsertColBeforeAction,TableInsertColAfterAction,TableRemoveRowAction,TableRemoveColAction]:
			self.tableDiv.appendChild( c() )
		self.tableDiv["style"]["display"]="none"
		self.linkEditor = LinkEditor()
		self.appendChild(self.linkEditor)
		self.imgEditor = ImageEditor()
		self.appendChild(self.imgEditor)

		self.editor = Editor(self, editHtml)

		self.actionbar.setActions( self.textActions )
		#btn = html5.ext.Button("Apply", self.saveText)
		#btn["class"].append("icon apply")
		#self.appendChild( btn )
		self.currentImage = None
		self.cursorImage = None
		self.lastMousePos = None
		self.sinkEvent("onMouseDown", "onMouseUp", "onMouseMove", "onClick")

		self.source = html5.form.Textarea()
		self.source["class"].append("sourceCode")
		self.source["class"].append("hide")
		self.appendChild(self.source)

	def flipView(self, *args, **kwargs ):
		htmlStr = eval("window.parent.document.getElementsByClassName('ql-editor')[0].innerHTML")

		if self.isWysiwygMode:
		#	FIXME: doesnt work with new texteditor so far
		#	self.imgEditor.doClose()
		#	self.linkEditor.doClose()
		#	self.tableDiv["style"]["display"] = None
			outStr = ""
			indent = 0
			indestStr = "    "
			inStr = htmlStr
			while inStr:
				if inStr.startswith("<div"):
					outStr += "\n"
					outStr += indestStr*indent
					indent +=1
				elif inStr.startswith("</div>"):
					indent -=1
					outStr += "\n"
					outStr += indestStr*indent
				if inStr.startswith("<p"):
					outStr += "\n"
					outStr += indestStr*indent
					indent +=1
				elif inStr.startswith("</p>"):
					indent -=1
					outStr += "\n"
					outStr += indestStr*indent
				elif inStr.startswith("<br"):
					outStr += "\n"
					outStr += indestStr*indent
				elif inStr.startswith("<table"):
					outStr += "\n"
					outStr += indestStr*indent
					indent +=1
				elif inStr.startswith("</table"):
					indent -=1
					outStr += "\n"
					outStr += indestStr*indent
				elif inStr.startswith("<tr"):
					outStr += "\n"
					outStr += indestStr*indent
					indent +=1
				elif inStr.startswith("</tr"):
					indent -=1
					outStr += "\n"
					outStr += indestStr*indent
				elif inStr.startswith("<td"):
					outStr += "\n"
					outStr += indestStr*indent
				elif inStr.startswith("<th>"):
					outStr += "\n"
					outStr += indestStr*indent
				elif inStr.startswith("<thead"):
					outStr += "\n"
					outStr += indestStr*indent
					indent +=1
				elif inStr.startswith("</thead>"):
					indent -=1
					outStr += "\n"
					outStr += indestStr*indent
				elif inStr.startswith("<tbody"):
					outStr += "\n"
					outStr += indestStr*indent
					indent +=1
				elif inStr.startswith("</tbody>"):
					indent -=1
					outStr += "\n"
					outStr += indestStr*indent
				outStr += inStr[0]
				inStr = inStr[ 1: ]
	
			self.editor.addClass("hide")
			self.source.removeClass("hide");
			self.source.element.value = outStr.strip();
			self.actionbar.setActions( ["text.flipView"] )
		else:
			htmlStr = self.source.element.value
			htmlStr = re.sub("\n", '', htmlStr)
			htmlStr = re.sub("&nbsp;", '', htmlStr).strip()

			eval("window.parent.document.getElementsByClassName('ql-editor')[0].innerHTML = '%s'" % htmlStr)
			self.editor.removeClass("hide")
			self.source.addClass("hide")
			self.actionbar.setActions( self.textActions )

		self.isWysiwygMode = not self.isWysiwygMode
		return self.isWysiwygMode


	def saveText(self, *args, **kwargs):
		htmlStr = eval("window.parent.document.getElementsByClassName('ql-editor')[0].innerHTML")
		self.saveTextEvent.fire(self, htmlStr)

	def abortText(self, *args, **kwargs):
		self.abortTextEvent.fire(self)
