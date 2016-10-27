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

		self.appendChild(Wysiwyg("Ich glaube mein Donald Trump preift..."))
		return

		# Main Screens
		self.loginScreen = LoginScreen()
		self.adminScreen = None

		self.loginScreen.invoke()

	def login(self):
		if not self.adminScreen:
			self.adminScreen = AdminScreen()

		self.loginScreen.hide()
		self.adminScreen.invoke()

	def logout(self):
		self.adminScreen.remove()
		conf["mainWindow"] = self.adminScreen = None

		self.loginScreen.invoke(logout=True)

if __name__ == '__main__':
	pyjd.setup("public/main.html")

	# Configure vi as network render prefix
	network.NetworkService.prefix = "/vi"

	conf["currentlanguage"] = i18n.getLanguage()

	app = Application()
	html5.Body().appendChild(app)

	pyjd.run()
