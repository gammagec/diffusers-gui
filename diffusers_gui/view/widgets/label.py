from tkinter import Label as TkLabel, StringVar

from . import View
from ...common import Subject

class Label(View):

	def __init__(self, var, layout_options = None):
		super().__init__(layout_options)
		
		self.string_var = StringVar()
		if isinstance(var, Subject):
			var.subscribe(lambda val: self.string_var.set(val))
		else:
			self.string_var.set(var)		

	def create(self, parent):
		super().create()		
		self.label = TkLabel(parent, textvariable = self.string_var)

	def get_frame(self):
		return self.label