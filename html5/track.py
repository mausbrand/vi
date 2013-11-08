from html5.widget import Widget

class Track( Widget ):
    _baseClass = "track"

    def __init__(self, *args, **kwargs):
        super(Track,self).__init__( *args, **kwargs )

	def _getKind(self):
		return self.element.kind
	def _setKind(self,val):
		self.element.kind=val

	def _getLabel(self):
		return self.element.label
	def _setLabel(self,val):
		self.element.label=val

	def _getSrc(self):
		return self.element.src
	def _setSrc(self,val):
		self.element.src=val

	def _getSrclang(self):
		return self.element.srclang
	def _setSrclang(self,val):
		self.element.srclang=val

	def _getDefault(self):
		return( True if self.element.hasAttribute("default") else False )
	def _setDefault(self,val):
		if val==True:
			self.element.setAttribute("default","")
		else:
			self.element.removeAttribute("default")