from tkinter import Button, StringVar

from . import View

from ...common import bind_enabled_to_intvar, bind_enabled_to_value_observer

class ButtonView(View):

	def __init__(self, var, handler, layout_options = None, 
		enabled_intvar = None, enabled_value_observer = None):

		super().__init__(layout_options)
		self.var = var
		self.enabled_intvar = enabled_intvar	
		self.enabled_value_observer	= enabled_value_observer
		self.handler = handler

	def create(self, parent):
		super().create()
		if isinstance(self.var, StringVar):
			self.button = Button(parent, textvariable = self.var, command = self.handler)
		else:
			self.button = Button(parent, text = self.var, command = self.handler)

		if self.enabled_intvar != None:
			bind_enabled_to_intvar(self.button, self.enabled_intvar)
		if self.enabled_value_observer != None:
			bind_enabled_to_value_observer(self.button, self.enabled_value_observer, self.button)

	def get_frame(self):
		return self.button
