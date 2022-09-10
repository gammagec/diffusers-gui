from tkinter import Label as TkLabel, StringVar

from . import View

class Label(View):

	def __init__(self, var, layout_options = None):
		super().__init__(layout_options)
		self.var = var

	def create(self, parent):
		super().create()
		if isinstance(self.var, StringVar):
			self.label = TkLabel(parent, textvariable = self.var)
		else:
			self.label = TkLabel(parent, text = self.var)

	def get_frame(self):
		return self.label