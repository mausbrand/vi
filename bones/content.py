#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import html5
from priorityqueue import editBoneSelector, viewDelegateSelector, extractorDelegateSelector
from widgets.file import FileWidget
from config import conf
from i18n import translate
import utils, re, pynetree

class ContentBoneExtractor( object ):
	def __init__(self, modulName, boneName, skelStructure, *args, **kwargs):
		super(ContentBoneExtractor, self).__init__()
		self.skelStructure = skelStructure
		self.boneName = boneName
		self.modulName = modulName

	def render( self, data, field ):
		if field in data.keys():
			return str(data[field])
		return conf["empty_value"]


class ContentViewBoneDelegate( object ):
	def __init__(self, modulName, boneName, skelStructure, *args, **kwargs ):
		super(ContentViewBoneDelegate, self).__init__()
		self.skelStructure = skelStructure
		self.boneName = boneName
		self.modulName = modulName

	def render( self, data, field ):
		if field in data.keys():
			return html5.Label(str( data[field]))
		return html5.Label(conf[ "empty_value" ])

class ContentFieldParser(pynetree.Parser):
	def __init__(self):
		super(ContentFieldParser, self).__init__("""
			$               /\s+/   %ignore;

			name            : /\w+/ %emit;
			value           : /[^\s,:=]+/ %emit;
			valuelist       : valuelist ',' value | value ;

			option %emit    : "type" [:=] ("input"|"textarea"|"dropdown"|"image")
			                | "descr" [:=] value
			                | "values" [:=] valuelist ;

			field           : name option* ;
			""")

	def compile(self, fielddef):
		print(fielddef)
		fielddef = fielddef.strip()
		if not fielddef:
			return None

		ast = self.parse(fielddef)
		if ast is None:
			print("PARSE ERROR")
			name = re.match(r"\w+", fielddef).group(0)
		else:
			name = ast[0][1][0][1]

		ret = {"name": name,
		       "type": "input",
		       "descr": name,
		       "values": []}

		if ast is None:
			return ret

		self.dump(ast)

		for node in ast[1:]:
			if node[0] == "option":
				opt = node[1][0][1]

				if opt == "type":
					ret["type"] = node[1][1][1]
				elif opt == "descr":
					ret["descr"] = node[1][1][1][0][1]
				elif opt == "values":
					print(node[1][1:])
					ret["values"] = [val[1][0][1] for val in node[1][1:]]

		return ret

parser = ContentFieldParser()

class ContentEditBoneWidget(html5.Div):
	def __init__(self, parent, name, type, descr = None, lang = None, *args, **kwargs):
		super(ContentEditBoneWidget, self).__init__()

		self.parent = parent
		self.lang = lang
		self.name = name
		self.type = type
		self.descr = descr or name

		self.label = html5.Label()
		self.label.appendChild(html5.TextNode(self.descr))
		self.appendChild(self.label)

		if self.type == "textarea":
			self.widget = html5.Textarea()

		elif self.type == "dropdown":
			self.widget = html5.Select()

			for item in kwargs.get("values", []):
				opt = html5.Option()
				opt["value"] = item
				opt.appendChild(html5.TextNode(item))
				self.widget.appendChild(opt)

		elif self.type == "input":
			self.widget = html5.Input()

		elif self.type == "image":
			self.widget = html5.Div()

			self.image = html5.Img()
			self.widget.appendChild(self.image)

			self.selectBtn = html5.ext.Button(translate("Select image"), callback=self.onSelectBtnClick)
			self.selectBtn["class"].append("icon text image")
			self.widget.appendChild(self.selectBtn)

		else:
			self.widget = html5.Input()
			self.widget["placeholder"] = "MISSING TYPE"

		self.appendChild(self.widget)

	def onSelectBtnClick(self, sender = None):
		currentSelector = FileWidget("file", isSelector=True)
		currentSelector.selectionActivatedEvent.register(self)
		conf["mainWindow"].stackWidget(currentSelector)

	def onSelectionActivated(self, selectWdg, selection):
		if not selection:
			return

		for item in selection:
			if "mimetype" in item.data.keys() and item.data["mimetype"].startswith("image/"):
				self.image["src"] = ("%s=s400" % item.data["servingurl"]) if "servingurl" in item.data.keys() else ("/file/download/%s" % item.data["dlkey"])

			#if "mimetype" in item.data.keys() and item.data["mimetype"].startswith("image/"):
			#	eval("window.top.document.execCommand(\"insertImage\", false, \""+dataUrl+"\")" )
			#else:
			#	eval("window.top.document.execCommand(\"createLink\", false, \""+dataUrl+"?download=1\")" )

		self.parent.update()

	def serialize(self, values):
		print("SERIALIZE", self.name, self.type)

		if self.lang:
			entryKey = "%s.%s" % (self.name, self.lang)
		else:
			entryKey = self.name

		if self.type in ["textarea", "input"]:
			val = self.widget["value"]

		elif self.type in ["dropdown"]:
			val = self.widget._children[self.widget["selectedIndex"]]["value"]

		elif self.type in ["image"]:
			val = self.image["src"]
			print("x"*30)
			print(self.image["src"])

		else:
			val = ""

		print(entryKey, val)

		values.update({entryKey: val})

	def unserialize(self, values):
		if self.lang:
			entryKey = "%s.%s" % (self.name, self.lang)
		else:
			entryKey = self.name

		if self.type in ["textarea", "input"]:
			self.widget["value"] = values.get(entryKey, "")
		elif self.type in ["dropdown"]:
			for c in self.widget._children:
				if c["value"] == values.get(entryKey, ""):
					c["selected"] = True
					break
		elif self.type in ["image"]:
			self.image["src"] = values.get(entryKey, "")


class ContentEditBoneEntry(html5.Li):
	def __init__(self, bone, template = None, values = None, *args, **kwargs):
		super(ContentEditBoneEntry, self).__init__(*args, **kwargs)
		self.bone = bone
		self.template = template
		self.values = values or {}
		self.language = None

		self.sinkEvent("onChange")

		self.templateSelector = html5.Select()
		self.appendChild(self.templateSelector)

		self.mask = html5.Div()
		self.mask["class"].append("mask")

		self.appendChild(self.mask)

		entries = []
		for name, dfn in self.bone.templates.items():
			if self.template is None:
				self.template = name

			opt = html5.Option()
			opt["value"] = name

			if self.template == name:
				opt["selected"] = True

			opt.appendChild(html5.TextNode(dfn.get("descr", name)))
			entries.append((name, dfn.get("descr", name), opt))

		for opt in sorted(entries, key=lambda x: x[1]):
			self.templateSelector.appendChild(opt[2])

		if bone.languages:
			buttonContainer = html5.Div()
			buttonContainer["class"] = "languagebuttons"
			self.appendChild(buttonContainer)

			for lang in bone.languages:
				if self.language is None:
					self.language = lang

				langBtn = html5.ext.Button(lang, callback=self.onLangBtnClicked)
				langBtn.lang = lang
				buttonContainer.appendChild(langBtn)

		self.renderMask(self.template)

		if bone.multiple:
			delBtn = html5.ext.Button(translate("Delete"), self.removeMe)
			delBtn["class"].append("icon delete tag")
			self.appendChild(delBtn)

			self.upBtn = html5.ext.Button(translate("Up"), self.moveUp)
			self.upBtn["class"].append("icon up tag")
			self.appendChild(self.upBtn)

			self.downBtn = html5.ext.Button(translate("Down"), self.moveDown)
			self.downBtn["class"].append("icon down tag")
			self.appendChild(self.downBtn)

		self.update()


	def removeMe(self, *args, **kwargs):
		self.parent().removeChild(self)

	def moveUp(self, *args, **kwargs):
		parent = self.parent()
		all = parent._children[:]

		for i in range(0, len(all)):
			if i > 0 and all[i] == self:
				all[i] = all[i-1]
				all[i-1] = self

		parent.removeAllChildren()
		for i in all:
			parent.appendChild(i)

		print("up")
		self.update()


	def moveDown(self, *args, **kwargs):
		parent = self.parent()
		all = parent._children[:]

		for i in range(0, len(all)):
			if i < len(all) - 1 and all[i] == self:
				all[i] = all[i+1]
				all[i+1] = self

		parent.removeAllChildren()
		for i in all:
			parent.appendChild(i)

		print("down")
		self.update()

	def onLangBtnClicked(self, sender):
		self.masks[self.language].hide()
		self.masks[sender.lang].show()
		self.language = sender.lang

	def renderMask(self, tpl):
		assert tpl in self.bone.templates.keys()
		tpl = self.bone.templates[tpl]["template"]

		self.mask.removeAllChildren()
		self.masks = {}

		for field in re.findall(r"{{\w+[^}]*}}", tpl):
			ret = parser.compile(field[2:-2])
			if ret is None:
				continue

			if self.bone.languages:
				for lang in self.bone.languages:
					wdg = ContentEditBoneWidget(self, lang=lang, **ret)
					wdg.unserialize(self.values)

					if not lang in self.masks.keys():
						self.masks[lang] = []
					self.masks[lang].append(wdg)

			else:
				wdg = ContentEditBoneWidget(self, **ret)
				wdg.unserialize(self.values)
				self.mask.appendChild(wdg)

		if self.masks:
			for lang in self.bone.languages or []:
				div = html5.Div()
				div["class"].append("lang_%s" % lang)
				if lang != self.language:
					div.hide()

				for c in self.masks[lang]:
					div.appendChild(c)

				self.masks[lang] = div
				self.mask.appendChild(div)


	def onChange(self, event):
		if event and utils.doesEventHitWidgetOrChildren(event, self.templateSelector):
			self.template = self.templateSelector._children[self.templateSelector["selectedIndex"]]["value"]
			self.renderMask(self.template)
		else:
			self.update()

	def update(self):
		if self.bone.multiple and len(self.bone.entries._children):
			if self == self.bone.entries._children[0]:
				self.upBtn.hide()
			else:
				self.upBtn.show()

			if self == self.bone.entries._children[-1]:
				self.downBtn.hide()
			else:
				self.downBtn.show()

		if self.bone.languages:
			for lang in self.bone.languages:
				for wdg in self.masks[lang]._children:
					wdg.serialize(self.values)
		else:
			for wdg in self.mask._children:
				wdg.serialize(self.values)


class ContentEditBone(html5.Div):

	def __init__(self, modulName, boneName, readOnly, templates,
	                multiple = False, languages = None, required = False,
	                    *args, **kwargs):
		super(ContentEditBone, self).__init__(*args, **kwargs)
		self.boneName = boneName
		self.readOnly = readOnly
		self.required = required
		self.templates = templates
		self.multiple = multiple
		self.languages = languages

		self.setParams()

		self.entries = html5.Ul()
		self.appendChild(self.entries)

		if self.multiple:
			addBtn = html5.ext.Button(translate("Add"), self.addEntry)
			addBtn["class"].append("icon add tag")
			self.appendChild(addBtn)

	def setParams(self):
		if self.readOnly:
			self["disabled"] = True

	def addEntry(self, *args, **kwargs):
		self.entries.appendChild(ContentEditBoneEntry(self))

	@staticmethod
	def fromSkelStructure( modulName, boneName, skelStructure ):
		readOnly = skelStructure[boneName].get("readonly", False)
		multiple = skelStructure[boneName].get("multiple", False)
		required = skelStructure[boneName].get("required", False)
		languages = skelStructure[boneName].get("languages")
		templates = skelStructure[boneName].get("templates", {})

		return ContentEditBone(modulName, boneName, readOnly, templates,
		                        multiple, languages, required)

	def unserialize(self, data, extendedErrorInformation=None):
		if data.get(self.boneName):
			all = data[self.boneName]

			print(all)

			if isinstance(all, dict):
				all = [all]

			for entry in all:
				self.entries.appendChild(ContentEditBoneEntry(self, entry["template"], entry["values"]))

		elif not self.multiple:
			self.addEntry()

	def serializeForPost(self):
		ret = {}

		for i, entry in enumerate(self.entries._children):
			if self.multiple:
				entryKey = "%s.%d" % (self.boneName, i)
			else:
				entryKey = self.boneName

			ret.update({entryKey: entry.template})

			for k, v in entry.values.items():
				ret.update({"%s.%s" % (entryKey, k): v})

		return ret

	def serializeForDocument(self):
		return self.serialize()

	def setExtendedErrorInformation(self, errorInfo ):
		pass


def CheckForContentBone(modulName, boneName, skelStucture, *args, **kwargs):
	return skelStucture[boneName]["type"] == "content"

#Register this Bone in the global queue
editBoneSelector.insert( 3, CheckForContentBone, ContentEditBone)
viewDelegateSelector.insert( 3, CheckForContentBone, ContentViewBoneDelegate)
extractorDelegateSelector.insert(3, CheckForContentBone, ContentBoneExtractor)
