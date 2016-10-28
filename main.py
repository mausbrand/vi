#-*- coding: utf-8 -*-
import html5, i18n, pyjd, network
from login import LoginScreen
from admin import AdminScreen
from config import conf

from widgets.wysiwyg import Wysiwyg

try:
	import vi_plugins
except ImportError:
	pass

class Application(html5.Div):
	def __init__(self):
		super(Application, self).__init__()
		self["class"].append("vi-application")
		conf["theApp"] = self

		self.appendChild(Wysiwyg(""))
		return

		# Main Screens
		self.loginScreen = None
		self.adminScreen = None

		self.startup()

	def startup(self):
		network.NetworkService.request(None, "/vi/config",
		                                successHandler=self.startupSuccess,
										failureHandler=self.startupFailure,
                                        cacheable=True)

	def startupSuccess(self, req):
		conf["mainConfig"] = network.NetworkService.decode(req)

		self.adminScreen = AdminScreen()
		self.adminScreen.invoke()

	def startupFailure(self, req, err):
		if err in [403, 401]:
			self.login()
		else:
			alert("startupFailure TODO")

	def login(self, logout=False):
		if not self.loginScreen:
			self.loginScreen = LoginScreen()

		self.loginScreen.invoke(logout=logout)

	def admin(self):
		if not self.adminScreen:
			self.adminScreen = AdminScreen()

		if self.loginScreen:
			self.loginScreen.hide()

		self.adminScreen.invoke()

	def logout(self):
		self.adminScreen.remove()
		conf["mainWindow"] = self.adminScreen = None
		self.login(logout=True)

if __name__ == '__main__':
	pyjd.setup("public/main.html")

	# Configure vi as network render prefix
	network.NetworkService.prefix = "/vi"
	conf["currentlanguage"] = i18n.getLanguage()

	# Application
	app = Application()
	html5.Body().appendChild(app)

	pyjd.run()
