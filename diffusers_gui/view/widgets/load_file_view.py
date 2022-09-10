from tkinter import LEFT, StringVar
from tkinter import filedialog

from . import EntryView, ButtonView, ContainerView
from ..layout import RowLayout

class LoadFileView(ContainerView):
	name = 'load_file_view'

	def __init__(self, var, layout_options = None):
		super().__init__(layout_options = layout_options, layout_manager = RowLayout())
		self.val = StringVar()
		self.var = var
		var.trace_add('write', lambda a, b, c: self.val.set(self.var.get()))
	
	def create(self, parent):
		super().create(parent)
		
		entry = EntryView(var = self.val)
		self.add_child(entry)

		button = ButtonView(var = 'Load', handler = lambda: self.load())
		self.add_child(button)

		clear_button = ButtonView(var = 'Clear', handler = lambda: self.var.set(''))
		self.add_child(clear_button)

	def load(self):
		if self.val.get() == '':	
			self.var.set(value = filedialog.askopenfilename(
				filetypes = [("PNG", "*.png"), ("Jpg", "*.jpg"), ("Jpeg", "*.jpeg")]))
		else:
			self.var.set(self.val.get())

