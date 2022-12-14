from tkinter import StringVar, DISABLED

from .widgets import Composite, Label, ScrolledText

class RunInfoView(Composite):
	name = 'run_info_view'

	def __init__(self, view_model):
		super().__init__()
		self.view_model = view_model
		view_model.set_view(self)
		self.text = StringVar()
		
	def create(self, parent):		
		super().create(parent)
		self.add_child(Label(var = "Selected Run"))
		text_view = ScrolledText(var = self.text)
		self.add_child(text_view)
		text_view.disable()
		text_view.bind_stringvar_to_scrolled_text()

	def update_text(self, text):				
		self.text.set(text)