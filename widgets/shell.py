import html5

from pane import Pane
from config import conf
from network import DeferredCall
from priorityqueue import initialHashHandler, startupQueue

class ShellExec(html5.Div):
	def __init__(self, *args, **kwargs):
		super(ShellExec, self).__init__(*args, **kwargs)

		if not conf["nwjs.enabled"]:
			return
		
		self.srcAppUrl = html5.Input()
		self.srcAppUrl["placeholder"] = "Source URL"
		self.appendChild(self.srcAppUrl)
		
		self.srcAppKey = html5.Input()
		self.srcAppKey["placeholder"] = "Source Key"
		self.appendChild(self.srcAppKey)

		self.dstAppUrl = html5.Input()
		self.dstAppUrl["placeholder"] = "Destination URL"
		self.appendChild(self.dstAppUrl)

		self.dstAppKey = html5.Input()
		self.dstAppKey["placeholder"] = "Destination Key"
		self.appendChild(self.dstAppKey)

		self.startBtn = html5.ext.Button("START", self.onStartBtnClick)
		self.appendChild(self.startBtn)

		self.stopBtn = html5.ext.Button("STOP", self.onStopBtnClick)
		self.stopBtn["disabled"] = True
		self.appendChild(self.stopBtn)

		self.stdoutDiv = html5.Div()
		self.appendChild(self.stdoutDiv)

		self.stderrDiv = html5.Div()
		self.appendChild(self.stderrDiv)

		self.childProcess = None

	def onStartBtnClick(self, sender):
		self.startBtn["disabled"] = True
		self.stopBtn["disabled"] = False

		self.stdoutDiv.removeAllChildren()
		self.stderrDiv.removeAllChildren()

		try:
			spawn = eval("global.spawn")

			opts = eval("Array()")

			opts.push("copyblobs.py")
			opts.push("--srcappid")
			opts.push(self.srcAppUrl["value"])
			opts.push("--srckey")
			opts.push(self.srcAppKey["value"])
			opts.push("--dstappid")
			opts.push(self.dstAppUrl["value"])
			opts.push("--dstkey")
			opts.push(self.dstAppKey["value"])

			self.childProcess = spawn("python", opts, self.stdout, self.stderr, self.close)
		except:
			alert("error")
			self.childProcess = None

	def onStopBtnClick(self, sender):
		self.childProcess.kill()

	def stdout(self, data):
		html5.utils.textToHtml(self.stdoutDiv, str(data))

	def stderr(self, data):
		html5.utils.textToHtml(self.stderrDiv, str(data))

	def close(self, *args, **kwargs):
		self.startBtn["disabled"] = False
		self.stopBtn["disabled"] = True

class Shell(Pane):

	@staticmethod
	def canHandle(path, params):
		return len(path) > 0 and path[0] == "shell"

	@staticmethod
	def insertPane(path, params):
		assert Shell.canHandle(path, params)

		shellPane = Shell(u"Shell", iconURL="icons/viur_logo.png")
		conf["mainWindow"].addPane(shellPane)

		shellPane.onClick()

	def onClick(self, event = None, *args, **kwargs):
		if not self.widgetsDomElm._children:
			widget = ShellExec()

			div = html5.Div()
			div.addClass("vi_operator")
			div["style"]["padding-top"] = "65px"
			div.appendChild(widget)

			self.widgetsDomElm.appendChild(div)

		conf["mainWindow"].focusPane(self)

		if event:
			super(Shell, self).onClick(event, *args, **kwargs)

initialHashHandler.insert(5, Shell.canHandle, Shell.insertPane)



def checkNWJS():
	try:
		eval("global")
		conf["nwjs.enabled"] = True

		script = html5.Script()
		script["src"] = "nwjs.js"

		html5.Body().appendChild(script)
		print("!!! DESKTOP MODE IS ENABLED !!!")
	except:
		conf["nwjs.enabled"] = False
		print("No desktop mode, normal web mode")

	DeferredCall(startupQueue.next)

startupQueue.insertElem(5, checkNWJS)