from tkinter import LEFT, StringVar
from tkinter import filedialog

from . import TextBox, Button, Composite
from ..layout import RowLayout
from ...common import BehaviorSubject

class LoadFileView(Composite):
	name = 'load_file_view'

	def __init__(self, var, layout_options = None):
		super().__init__(layout_options = layout_options, layout_manager = RowLayout())
		self.val = BehaviorSubject('')
		self.var = var
		var.subscribe(lambda val: self.val.next(val))
	
	def create(self, parent):
		super().create(parent)
		
		entry = TextBox(var = self.val)
		self.add_child(entry)

		button = Button(var = 'Load', handler = lambda: self.load())
		self.add_child(button)

		clear_button = Button(var = 'Clear', handler = lambda: self.var.next(''))
		self.add_child(clear_button)

	def load(self):
		if self.val.get_value() == '':	
			self.var.next(value = filedialog.askopenfilename(
				filetypes = [("PNG", "*.png"), ("Jpg", "*.jpg"), ("Jpeg", "*.jpeg")]))
		else:
			self.var.next(self.val.get_value())

