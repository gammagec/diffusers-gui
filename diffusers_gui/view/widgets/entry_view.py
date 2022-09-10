from tkinter import Entry, StringVar

from . import View

from ...common import bind_enabled_to_intvar

class EntryView(View):

	def __init__(self, var, layout_options = None, enabled_intvar = None):
		super().__init__(layout_options)
		self.var = var
		self.enabled_intvar = enabled_intvar		

	def create(self, parent):
		super().create()		
		self.entry = Entry(parent, textvariable = self.var)		

		if self.enabled_intvar != None:
			bind_enabled_to_intvar(self.entry, self.enabled_intvar)

	def get_frame(self):
		return self.entry
