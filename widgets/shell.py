import html5

from pane import Pane
from config import conf
from network import DeferredCall
from priorityqueue import initialHashHandler, startupQueue

class ShellExec(html5.Div):
	def __init__(self, cmd, *args, **kwargs):
		super(ShellExec, self).__init__(*args, **kwargs)

		if not conf["nwjs.enabled"]:
			return

		try:
			shell = eval("global.shell")
			shell(cmd, self.element)
		except:
			alert("error")


class Shell(Pane):

	@staticmethod
	def canHandle(path, params):
		return len(path) > 0 and path[0] == "shell"

	@staticmethod
	def insertPane(path, params):
		assert Shell.canHandle(path, params)

		shellPane = Shell(u"Shell", iconURL="icons/viur_logo.png", closeable=True)
		conf["mainWindow"].addPane(shellPane)

		shellPane.onClick()

	def onClick(self, event = None, *args, **kwargs):
		if not self.widgetsDomElm._children:
			widget = ShellExec("python --help")

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