import html5, utils
from network import NetworkService, DeferredCall
from widgets.tree import TreeWidget, LeafWidget
from priorityqueue import displayDelegateSelector
from event import EventDispatcher
from config import conf
import json
from i18n import translate
from widgets.search import Search

class LeafFileWidget( LeafWidget ):
	"""
		Displays a file inside a tree application.
	"""
	def __init__(self, modul, data, structure, *args, **kwargs ):
		super( LeafFileWidget, self ).__init__( modul, data, structure, *args, **kwargs )

		if utils.getImagePreview( data ):
			self.appendChild( html5.Img( utils.getImagePreview( data ) ) )

		if "mimetype" in data.keys():
			try:
				ftype, fformat = data["mimetype"].split("/")
				self["class"].append("type_%s" % ftype )
				self["class"].append("format_%s" % fformat.replace( "+", "_" ) )
			except:
				pass

		self["class"].append("file")
		self.sinkEvent("onDragOver","onDragLeave")

	def onDragOver(self, event):
		if not "insert_before" in self["class"]:
			self["class"].append("insert_before")
		super(LeafFileWidget, self).onDragOver(event)

	def onDragLeave(self, event):
		if "insert_before" in self["class"]:
			self["class"].remove("insert_before")
		super(LeafFileWidget,self).onDragLeave( event )


class Uploader( html5.Progress ):
	"""
		Uploads a file to the server while providing visual feedback of the progress.
	"""
	def __init__(self, file, node, context = None, *args, **kwargs):
		"""
			@param file: The file to upload
			@type file: A javascript "File" Object
			@param node: Key of the desired node of our parents tree application or None for an anonymous upload.
			@type node: String or None
		"""
		super(Uploader, self).__init__( *args, **kwargs )
		self.uploadSuccess = EventDispatcher("uploadSuccess")
		self.responseValue = None
		self.context = context
		#self.files = files
		r = NetworkService.request("file","getUploadURL", successHandler=self.onUploadUrlAvaiable, secure=True)
		r.file = file
		r.node = node
		conf["mainWindow"].log("progress", self)
		self.parent()["class"].append( "is_uploading" )

	def onUploadUrlAvaiable(self, req ):
		"""
			Internal callback - the actual upload url (retrieved by calling /file/getUploadURL) is known.
		"""
		r = NetworkService.request("","/admin/skey", successHandler=self.onSkeyAvaiable)
		r.file = req.file
		r.node = req.node
		r.destUrl = req.result

	def onSkeyAvaiable(self, req):
		"""
			Internal callback - the Security-Key is known.
		"""
		formData = eval("new FormData();")
		formData.append("file", req.file )

		if self.context:
			for k, v in self.context.items():
				formData.append(k, v)

		if req.node and str(req.node)!="null":
			formData.append("node", req.node )

		formData.append("skey", NetworkService.decode(req) )
		self.xhr = eval("new XMLHttpRequest()")
		self.xhr.open("POST", req.destUrl )
		self.xhr.onload = self.onLoad
		self.xhr.upload.onprogress = self.onProgress
		self.xhr.send( formData )

	def onLoad(self, *args, **kwargs ):
		"""
			Internal callback - The state of our upload changed.
		"""
		if self.xhr.status==200:
			self.responseValue = json.loads( self.xhr.responseText )
			DeferredCall(self.onSuccess, _delay=1000)
		else:
			DeferredCall(self.onFailed, self.xhr.status, _delay=1000)

	def onProgress(self, event):
		"""
			Internal callback - further bytes have been transmitted
		"""
		if event.lengthComputable:
			complete = int(event.loaded / event.total * 100)
			self["value"] = complete
			self["max"] = 100

	def onSuccess(self, *args, **kwargs):
		"""
			Internal callback - The upload succeeded.
		"""
		for v in self.responseValue["values"]:
			self.uploadSuccess.fire(self, v)

		NetworkService.notifyChange("file")
		self.replaceWithMessage("Upload complete", isSuccess=True)

	def onFailed(self, errorCode, *args, **kwargs ):
		self.replaceWithMessage( "Upload failed with status code %s" % errorCode, isSuccess=False )

	def replaceWithMessage(self, message, isSuccess):
		self.parent()["class"].remove("is_uploading")
		self.parent()["class"].remove("log_progress")
		if isSuccess:
			self.parent()["class"].append("log_success")
		else:
			self.parent()["class"].append("log_failed")
		msg = html5.Span()
		msg.appendChild( html5.TextNode( message ) )
		self.parent().appendChild( msg )
		self.parent().removeChild( self )


class FileWidget( TreeWidget ):
	"""
		Extends the TreeWidget to allow drag&drop upload of files to the current node.
	"""
	defaultActions = ["add.node", "add.leaf", "selectrootnode", "edit", "delete", "reload", "download"]
	leafWidget = LeafFileWidget

	def __init__(self,*args, **kwargs):
		super( FileWidget, self ).__init__( *args, **kwargs)
		self.sinkEvent("onDragOver", "onDrop")
		self["class"].append("supports_upload")
		self.search = Search()
		self.appendChild( self.search )
		self.search.startSearchEvent.register( self )

	def onStartSearch(self, searchStr, *args, **kwargs):
		if not searchStr:
			self.setRootNode( self.rootNode )
		else:
			for c in self.pathList._children[:]:
				self.pathList.removeChild( c )
			s = html5.Span()
			s.appendChild(html5.TextNode("Search"))
			self.pathList.appendChild( s )
			self.reloadData( {"node":self.rootNode,"search": searchStr} )

	def setNode(self, node):
		"""
			Override setNode sothat we can reset our search field if a folder has been clicked
		:param node:
		:return:
		"""
		self.search.searchInput["value"] = ""
		super( FileWidget, self ).setNode( node )

	@staticmethod
	def canHandle( modul, moduleInfo ):
		return( moduleInfo["handler"].startswith("tree.simple.file" ) )

	def onDragOver(self, event):
		event.preventDefault()
		event.stopPropagation()
		#print("%s %s" % (event.offsetX, event.offsetY))


	def onDrop(self, event):
		event.preventDefault()
		event.stopPropagation()
		files = event.dataTransfer.files
		for x in range(0,files.length):
			Uploader(files.item(x), self.node )

displayDelegateSelector.insert( 3, FileWidget.canHandle, FileWidget )
