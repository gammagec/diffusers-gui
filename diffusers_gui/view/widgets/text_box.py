from tkinter import Entry, StringVar

from . import View

from ...common import bind_enabled_to_intvar

class TextBox(View):

	def __init__(self, var, layout_options = None, enabled_intvar = None):
		super().__init__(layout_options)		
		self.enabled_intvar = enabled_intvar		
		self.string_var = StringVar()
		self.string_var.set(var.get_value())
		var.subscribe(lambda val: self.string_var.set(val))
		self.string_var.trace('w', lambda a, b, c: var.set_value(self.string_var.get()))

	def create(self, parent):
		super().create()		
		self.entry = Entry(parent, textvariable = self.string_var)		

		if self.enabled_intvar != None:
			bind_enabled_to_intvar(self.entry, self.enabled_intvar)

	def get_frame(self):
		return self.entry
