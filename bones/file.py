# -*- coding: utf-8 -*-
import html5, utils
from priorityqueue import editBoneSelector, viewDelegateSelector, extractorDelegateSelector
from widgets.file import FileWidget, LeafFileWidget
from config import conf
from bones.relational import RelationalMultiSelectionBone, RelationalSingleSelectionBone, RelationalMultiSelectionBoneEntry
from widgets.file import Uploader
from i18n import translate
from network import NetworkService
from widgets.edit import EditWidget
from pane import Pane
from bones.base import BaseBoneExtractor

class FileImagePopup(html5.ext.Popup):
	def __init__(self, preview, *args, **kwargs):
		super(FileImagePopup, self).__init__(title=preview.currentFile.get("name", translate("Unnamed Image")), className="image-viewer", *args, **kwargs)
		self.sinkEvent("onClick")
		self.preview = preview

		img = html5.Img()
		img["src"] = utils.getImagePreview(preview.currentFile, size=None)
		self.appendChild(img)

		div = html5.Div()
		self.appendChild(div)

		btn = html5.ext.Button(translate("Download"), self.onDownloadBtnClick)
		btn.addClass("icon", "download")
		div.appendChild(btn)

		btn = html5.ext.Button(translate("Close"), self.onClick)
		btn.addClass("btn_no")
		div.appendChild(btn)


	def onClick(self, event):
		self.close()

	def onDownloadBtnClick(self, sender = None):
		self.preview.download()

class FilePreviewImage(html5.Div):
	def __init__(self, file = None, size=150, *args, **kwargs):
		super(FilePreviewImage, self).__init__(*args, **kwargs)
		self.addClass("previewimg")
		self.sinkEvent("onClick")

		self.size = size

		self.downloadA = html5.A()
		self.downloadA.hide()
		self.appendChild(self.downloadA)

		self.isImage = False
		self.downloadOnly = False
		self.currentFile = None

		self.setFile(file)

	def setFile(self, file):
		self.currentFile = file

		preview = utils.getImagePreview(file, cropped=True, size = self.size) if file else None

		if preview:
			self.downloadOnly = self.isImage = True

		else:
			self.isImage = False
			self.downloadOnly = True

			if file:
				preview = "icons/filetypes/file.svg"
				mime = file.get("mimetype")
				if mime:
					for icon in ["bmp", "doc", "gif", "jpg", "pdf", "png", "tiff", "image", "audio", "video", "zip"]:
						if icon in mime:
							preview = "icons/filetypes/%s.svg" % icon
							self.downloadOnly = False
							break

		if preview:
			self["style"]["background-image"] = "url('%s')" % preview
		else:
			self["style"]["background-image"] = None

		if self.currentFile:
			self.addClass("is-clickable")
		else:
			self.removeClass("is-clickable")


	def download(self):
		if not self.currentFile:
			return

		self.downloadA["href"] = "/file/download/" + self.currentFile["dlkey"]
		self.downloadA["download"] = self.currentFile.get("name", self.currentFile["dlkey"])
		self.downloadA.element.click()

	def onClick(self, event):
		if not self.currentFile:
			return

		if self.isImage:
			FileImagePopup(self)
		else:
			w = eval("window")

			if self.downloadOnly:
				self.download()
				return

			file = "/file/download/%s" % self.currentFile["dlkey"]

			if self.currentFile.get("name"):
				file += "?fileName=%s" % self.currentFile["name"]

			w.open(file)


class FileBoneExtractor(BaseBoneExtractor):
	def __init__(self, module, boneName, structure):
		super(FileBoneExtractor, self).__init__(module, boneName, structure)
		self.format = "$(dest.name)"
		if "format" in structure[boneName].keys():
			self.format = structure[boneName]["format"]

	def renderFileentry(self, fileentry):
		origin = eval("window.location.origin")
		return ("%s %s/file/download/%s?download=1&fileName=%s" %
		            (fileentry["dest"]["name"], origin,
		                str(fileentry["dest"]["dlkey"]), str(fileentry["dest"]["name"])))

	def render(self, data, field ):
		assert field == self.boneName, "render() was called with field %s, expected %s" % (field,self.boneName)
		val = data.get(field, "")

		if isinstance(val, list):
			return [self.renderFileentry(f) for f in val]
		elif isinstance(val, dict):
			return self.renderFileentry(val)

		return val

class FileViewBoneDelegate(object):

	def __init__(self, modul, boneName, structure):
		super(FileViewBoneDelegate, self).__init__()
		self.format = "$(name)"

		if "format" in structure[boneName].keys():
			self.format = structure[boneName]["format"]

		self.module = modul
		self.structure = structure
		self.boneName = boneName

	def renderFileentry(self, fileEntry):
		if not "dest" in fileEntry.keys():
			return None

		fileEntry = fileEntry["dest"]

		if not "name" in fileEntry.keys() and not "dlkey" in fileEntry.keys():
			return None

		adiv = html5.Div()
		if "mimetype" in fileEntry.keys():
			try:
				ftype, fformat = fileEntry["mimetype"].split("/")
				adiv["class"].append("type_%s" % ftype )
				adiv["class"].append("format_%s" % fformat )
			except:
				pass

		adiv.appendChild(FilePreviewImage(fileEntry))

		aspan=html5.Span()
		aspan.appendChild(html5.TextNode(str(fileEntry.get("name", ""))))#fixme: formatstring!
		adiv.appendChild(aspan)

		adiv["class"].append("fileBoneViewCell")
		#adiv["draggable"]=True
		#metamime="application/octet-stream"

		#if "mimetype" in fileEntry.keys():
		#   metamime=str(fileEntry["mimetype"])

		#adiv["download"]="%s:%s:/file/download/%s?download=1&fileName=%s" % (metamime, str(fileEntry["name"]),
		#                                                            str(fileEntry["dlkey"]), str(fileEntry["name"]))
		#adiv["href"]="/file/download/%s?download=1&fileName=%s" % (str(fileEntry["dlkey"]), str(fileEntry["name"]))
		return adiv

	def render(self, data, field ):
		assert field == self.boneName, "render() was called with field %s, expected %s" % (field,self.boneName)
		val = data.get(field, "")

		if isinstance(val, list):
			#MultiFileBone
			cell = html5.Div()

			for f in val:
				cell.appendChild(self.renderFileentry(f))

			return cell

		elif isinstance(val, dict):
			return self.renderFileentry(val)

		if val:
			return self.renderFileentry(val)

		return html5.Div()

class FileMultiSelectionBoneEntry(RelationalMultiSelectionBoneEntry):

	def __init__(self, *args, **kwargs):
		super(FileMultiSelectionBoneEntry, self).__init__(*args, **kwargs)
		self["class"].append("fileentry")
		self.prependChild(FilePreviewImage(self.data["dest"]))

	def fetchEntry(self, key):
		NetworkService.request(self.module,"view/leaf/"+key,
		                        successHandler=self.onSelectionDataAvailable, cacheable=True)

	def onEdit(self, *args, **kwargs):
		"""
			Edit the image entry.
		"""
		pane = Pane(translate("Edit"), closeable=True, iconClasses=[ "modul_%s" % self.parent.destModule,
		                                                                "apptype_list", "action_edit" ] )
		conf["mainWindow"].stackPane(pane, focus=True)

		try:
			edwg = EditWidget(self.parent.destModule, EditWidget.appTree, key=self.data["dest"]["key"], skelType="leaf")
			pane.addWidget(edwg)
		except AssertionError:
			conf["mainWindow"].removePane(pane)

	def update(self):
		NetworkService.request(self.parent.destModule, "view/leaf",
		                        params={"key": self.data["dest"]["key"]},
		                        successHandler=self.onModuleViewAvailable)

class FileMultiSelectionBone( RelationalMultiSelectionBone ):

	def __init__(self, *args, **kwargs):
		super(FileMultiSelectionBone, self).__init__( *args, **kwargs )
		self.sinkEvent("onDragOver","onDrop")
		self["class"].append("supports_upload")

	def onDragOver(self, event):
		super(FileMultiSelectionBone,self).onDragOver(event)
		event.preventDefault()
		event.stopPropagation()

	def onDrop(self, event):
		event.preventDefault()
		event.stopPropagation()
		files = event.dataTransfer.files
		for x in range(0,files.length):
			ul = Uploader(files.item(x), None, context=self.context)
			ul.uploadSuccess.register( self )

	def onUploadSuccess(self, uploader, file ):
		self.setSelection([{"dest": file,"rel":{}}])
		self.changeEvent.fire(self)

	def onShowSelector(self, *args, **kwargs):
		"""
			Opens a TreeWidget sothat the user can select new values
		"""
		currentSelector = FileWidget(self.destModule, isSelector="leaf")
		currentSelector.selectionReturnEvent.register(self)
		conf["mainWindow"].stackWidget(currentSelector)
		self.parent()["class"].append("is-active")

	def onSelectionReturn(self, table, selection ):
		"""
			Merges the selection made in the TreeWidget into our value(s)
		"""
		hasValidSelection = False
		for s in selection:
			if isinstance( s, LeafFileWidget ):
				hasValidSelection = True
				break
		if not hasValidSelection: #Its just a folder that's been activated
			return
		self.setSelection( [{"dest": x.data, "rel": {}} for x in selection if isinstance(x, LeafFileWidget)] )
		self.changeEvent.fire(self)

	def setSelection(self, selection):
		"""
			Set our current value to 'selection'
			@param selection: The new entry that this bone should reference
			@type selection: dict | list[dict]
		"""
		print("setSelection", selection)

		if selection is None:
			return

		for data in selection:
			entry = FileMultiSelectionBoneEntry(self, self.destModule, data, using=self.using, errorInfo={})
			self.addEntry( entry )

class FileSingleSelectionBone( RelationalSingleSelectionBone ):

	def __init__(self, *args, **kwargs):
		super(FileSingleSelectionBone, self).__init__( *args, **kwargs )
		self.sinkEvent("onDragOver","onDrop")
		self["class"].append("supports_upload")

		self.previewImg = FilePreviewImage()
		self.prependChild(self.previewImg)

		self.selection = None

	def onDragOver(self, event):
		super(FileSingleSelectionBone,self).onDragOver(event)
		event.preventDefault()
		event.stopPropagation()

	def onDrop(self, event):
		event.preventDefault()
		event.stopPropagation()
		files = event.dataTransfer.files

		if files.length > 1:
			conf["mainWindow"].log("error",translate("You cannot drop more than one file here!"))
			return

		for x in range(0,files.length):
			ul = Uploader(files.item(x), None, context = self.context)
			ul.uploadSuccess.register( self )

	def onUploadSuccess(self, uploader, file):
		self.setSelection({"dest": file, "rel":{}})
		self.changeEvent.fire(self)

	def onShowSelector(self, *args, **kwargs):
		"""
			Opens a TreeWidget sothat the user can select new values
		"""
		currentSelector = FileWidget( self.destModule, isSelector="leaf" )
		currentSelector.selectionReturnEvent.register( self )
		conf["mainWindow"].stackWidget( currentSelector )
		self.parent()["class"].append("is-active")

	def onSelectionReturn(self, table, selection ):
		"""
			Merges the selection made in the TreeWidget into our value(s)
		"""
		hasValidSelection = False
		for s in selection:
			if isinstance( s, LeafFileWidget ):
				hasValidSelection = True
				break
		if not hasValidSelection: #Its just a folder that's been activated
			return

		self.setSelection([{"dest": x.data for x in selection if isinstance(x,LeafFileWidget)}][0] )
		self.changeEvent.fire(self)

	def onEdit(self, *args, **kwargs):
		"""
			Edit the image.
		"""
		if not self.selection:
			return

		pane = Pane(translate("Edit"), closeable=True, iconClasses=[ "modul_%s" % self.destModule,
		                                                                "apptype_list", "action_edit" ] )
		conf["mainWindow"].stackPane(pane, focus=True)

		try:
			edwg = EditWidget(self.destModule, EditWidget.appTree, key=self.selection["dest"]["key"], skelType="leaf")
			pane.addWidget(edwg)
		except AssertionError:
			conf["mainWindow"].removePane(pane)

	def setSelection(self, selection):
		"""
			Set our current value to 'selection'
			@param selection: The new entry that this bone should reference
			@type selection: dict
		"""
		self.selection = selection

		if selection:
			NetworkService.request(self.destModule, "view/leaf/%s" % selection["dest"]["key"],
			                        successHandler=self.onSelectionDataAvailable,
			                        cacheable=True)
			self.selectionTxt["value"] = translate("Loading...")

			self.previewImg.setFile(self.selection["dest"])
		else:
			self.previewImg.setFile(None)
			self.selectionTxt["value"] = ""

		self.updateButtons()


def CheckForFileBoneSingleSelection( moduleName, boneName, skelStructure, *args, **kwargs ):
	isMultiple = "multiple" in skelStructure[boneName].keys() and skelStructure[boneName]["multiple"]
	return CheckForFileBone( moduleName, boneName, skelStructure ) and not isMultiple

def CheckForFileBoneMultiSelection( moduleName, boneName, skelStructure, *args, **kwargs ):
	isMultiple = "multiple" in skelStructure[boneName].keys() and skelStructure[boneName]["multiple"]
	return CheckForFileBone( moduleName, boneName, skelStructure ) and isMultiple

def CheckForFileBone(  moduleName, boneName, skelStucture, *args, **kwargs ):
	#print("CHECKING FILE BONE", skelStucture[boneName]["type"])
	return( skelStucture[boneName]["type"].startswith("treeitem.file") )

#Register this Bone in the global queue
editBoneSelector.insert( 5, CheckForFileBoneSingleSelection, FileSingleSelectionBone)
editBoneSelector.insert( 5, CheckForFileBoneMultiSelection, FileMultiSelectionBone)
viewDelegateSelector.insert( 3, CheckForFileBone, FileViewBoneDelegate)
extractorDelegateSelector.insert(3, CheckForFileBone, FileBoneExtractor)
