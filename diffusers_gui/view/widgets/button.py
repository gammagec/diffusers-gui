from tkinter import Button as TkButton, StringVar, NORMAL, DISABLED

from . import View

from ...common import bind_enabled_to_intvar, bind_enabled_to_value_observer

class Button(View):
	name = 'button'
		
	def __init__(self, var, handler, layout_options = None, enabled_value = None):
		print(f'Button {var} __init__')
		super().__init__(layout_options)
		self.var = var
		self.enabled_value	= enabled_value
		self.handler = handler
		self.enabled = True
		if self.enabled_value != None:
			self.enabled_value.subscribe(lambda enabled: self.set_enabled(enabled))

	def set_enabled(self, enabled):
		print(f'set_enabled {self.var} to {enabled}')
		self.enabled = enabled	
		self.update_enabled_state()	

	def update_enabled_state(self):
		if self.is_created():									
			print(f'updating button {self.var} enabled {self.enabled}')
			self.button.configure(state = NORMAL if self.enabled else DISABLED)			

	def create(self, parent):
		print(f'Button {self.var} create')
		super().create()
		if isinstance(self.var, StringVar):
			self.button = TkButton(parent, textvariable = self.var, command = self.handler)
		else:
			self.button = TkButton(parent, text = self.var, command = self.handler)
		
		self.update_enabled_state()

	def get_frame(self):
		return self.button
