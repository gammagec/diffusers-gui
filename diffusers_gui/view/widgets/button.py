from tkinter import Button as TkButton, StringVar

from . import View

from ...common import bind_enabled_to_intvar, bind_enabled_to_value_observer

class Button(View):
	name = 'button'
		
	def __init__(self, var, handler, layout_options = None, enabled_value = None):

		super().__init__(layout_options)
		self.var = var
		self.enabled_value	= enabled_value
		self.handler = handler

	def create(self, parent):
		super().create()
		if isinstance(self.var, StringVar):
			self.button = TkButton(parent, textvariable = self.var, command = self.handler)
		else:
			self.button = TkButton(parent, text = self.var, command = self.handler)
		
		if self.enabled_value != None:
			bind_enabled_to_value_observer(self.button, self.enabled_value, self.button)

	def get_frame(self):
		return self.button
