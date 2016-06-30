import html5

from pane import Pane
from config import conf
from network import NetworkService, DeferredCall
from priorityqueue import initialHashHandler, startupQueue

class ShellExec(html5.Div):
	def __init__(self, *args, **kwargs):
		super(ShellExec, self).__init__(*args, **kwargs)

		if not conf["nwjs.enabled"]:
			return
		
		self.srcAppUrl = html5.Input()
		self.srcAppUrl["placeholder"] = "Source URL"
		self.appendChild(self.srcAppUrl)
		self.appendChild(html5.Br())
		
		self.srcAppKey = html5.Input()
		self.srcAppKey["placeholder"] = "Source Key"
		self.appendChild(self.srcAppKey)
		self.appendChild(html5.Br())

		self.dstAppUrl = html5.Input()
		self.dstAppUrl["placeholder"] = "Destination URL"
		self.appendChild(self.dstAppUrl)
		self.appendChild(html5.Br())

		self.dstAppKey = html5.Input()
		self.dstAppKey["placeholder"] = "Destination Key"
		self.appendChild(self.dstAppKey)
		self.appendChild(html5.Br())

		lbl = html5.Label()
		self.dataImport = html5.Input()
		self.dataImport["type"] = "checkbox"
		self.dataImport["checked"] = True
		lbl.appendChild(self.dataImport)
		lbl.appendChild(html5.TextNode("Trigger data import after blob import"))
		self.appendChild(lbl)

		self.appendChild(html5.Br())

		self.startBtn = html5.ext.Button("START", self.onStartBtnClick)
		self.appendChild(self.startBtn)

		self.stopBtn = html5.ext.Button("STOP", self.onStopBtnClick)
		self.appendChild(self.stopBtn)

		self.stdoutDiv = html5.Div()
		self.appendChild(self.stdoutDiv)

		self.stderrDiv = html5.Div()
		self.appendChild(self.stderrDiv)

		self.childProcess = None
		self.interrupted = False

		self.reset()

	def reset(self):
		try:
			host = eval("window.location.host")
			if "localhost" in host or "127.0.0.1" in host:
				prot = "http"
			else:
				prot = "https"

			self.dstAppUrl["value"] = "%s://%s" % (prot, host)
		except:
			pass

		self.srcAppUrl["value"] = "https://%s.appspot.com" % conf["server"].get("dbtransfer.appId", "<your-app-id>")
		self.srcAppKey["value"] = conf["server"].get("dbtransfer.exportPassword", "")
		self.dstAppKey["value"] = conf["server"].get("dbtransfer.importPassword", "")

		self.setMaskMode(True)

	def setMaskMode(self, enabled):
		self.stopBtn["disabled"] = enabled
		self.startBtn["disabled"] = not enabled

		self.srcAppUrl["disabled"] = not enabled
		self.srcAppKey["disabled"] = not enabled
		self.dstAppUrl["disabled"] = not enabled
		self.dstAppKey["disabled"] = not enabled

		self.dataImport["disabled"] = not enabled

	def onStartBtnClick(self, sender):
		self.interrupted = False
		self.setMaskMode(False)

		self.stdoutDiv.removeAllChildren()
		self.stderrDiv.removeAllChildren()

		while self.srcAppUrl["value"].endswith("/"):
			self.srcAppUrl["value"] = self.srcAppUrl["value"][:-1]

		while self.dstAppUrl["value"].endswith("/"):
			self.dstAppUrl["value"] = self.dstAppUrl["value"][:-1]

		try:
			spawn = eval("global.spawn")

			opts = eval("Array()")

			opts.push("copyblobs.py")
			opts.push("--srcappid")
			opts.push(self.srcAppUrl["value"].replace("https://", "").replace("http://", "").replace("//", "").replace(".appspot.com", ""))
			opts.push("--srckey")
			opts.push(self.srcAppKey["value"])
			opts.push("--dstappid")
			opts.push(self.dstAppUrl["value"].replace("https://", "").replace("http://", "").replace("//", "").replace(".appspot.com", ""))
			opts.push("--dstkey")
			opts.push(self.dstAppKey["value"])

			self.childProcess = spawn("python", opts, self.stdout, self.stderr, self.close)
		except:
			alert("error")
			self.childProcess = None

	def onStopBtnClick(self, sender):
		if self.childProcess:
			self.childProcess.kill()
			self.interrupted = True

	def stdout(self, data):
		html5.utils.textToHtml(self.stdoutDiv, str(data))

	def stderr(self, data):
		html5.utils.textToHtml(self.stderrDiv, str(data))

	def close(self, *args, **kwargs):
		self.childProcess = None

		if self.dataImport["checked"] and not self.interrupted:
			NetworkService.host = self.dstAppUrl["value"]

			req = NetworkService.request(None,
					                        "/dbtransfer/triggerImport",
					                        {"module": "*",
					                            "source": "%s/dbtransfer/iterValues2" % self.dstAppUrl["value"],
					                            "exportkey": self.dstAppKey["value"]},
					                        successHandler=self.importTaskStarted,
			                                failureHandler=self.importTaskFailed)
			req.host = NetworkService.host

			NetworkService.host = ""
		else:
			self.setMaskMode(True)

	def importTaskStarted(self, req):
		conf["mainWindow"].log("success", "Import task on %s has been triggered!" % req.host)
		self.setMaskMode(True)

	def importTaskFailed(self, *args, **kwargs):
		conf["mainWindow"].log("error", "Import task could not be triggered.")
		self.setMaskMode(True)

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