from tkinter import scrolledtext, WORD, DISABLED

from . import View

from ..common import bind_scrolledtext_to_stringvar, bind_stringvar_to_scrolled_text

class ScrolledTextView(View):

	def __init__(self, var, layout_options = None):
		super().__init__(layout_options)
		self.var = var
		self.disabled = False
		self.bind_from_var = False

	def get_frame(self):
		return self.scrolledtext

	def disable(self):
		self.disabled = True
		if self.is_created():
			self.scrolledtext.configure(state = DISABLED)		

	def bind_stringvar_to_scrolled_text(self):
		self.bind_from_var = True		

	def create(self, parent):
		super().create()
		self.scrolledtext = scrolledtext.ScrolledText(
			parent, wrap = WORD, width = 40, height = 5, font = ("Times New Roman", 10))				
		bind_scrolledtext_to_stringvar(self.scrolledtext, self.var)				
		if self.disabled:
			self.scrolledtext.configure(state = DISABLED)
		if self.bind_from_var:
			bind_stringvar_to_scrolled_text(self.scrolledtext, self.var)