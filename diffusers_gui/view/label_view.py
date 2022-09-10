from tkinter import Label, StringVar

from . import View

class LabelView(View):

	def __init__(self, var, layout_options = None):
		super().__init__(layout_options)
		self.var = var

	def create(self, parent):
		super().create()
		if isinstance(self.var, StringVar):
			self.label = Label(parent, textvariable = self.var)
		else:
			self.label = Label(parent, text = self.var)

	def get_frame(self):
		return self.label