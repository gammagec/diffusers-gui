from tkinter import Frame, X, END

from .widgets import Composite, Label, ListBox, FIRST
from .layout import pack_layout_options

class RunsView(Composite):
	name = 'runs_view'

	def __init__(self, view_model):
		super().__init__()
		self.view_model = view_model	
		view_model.set_view(self)	

	def create(self, parent):
		super().create(parent)
		
		self.add_child(Label(var = "Runs"))
		
		self.runs_list = ListBox(
			lambda evt: self.view_model.on_run_select(
				self.runs_list.get_selected_value()), 
			auto_select = FIRST,
			layout_options = pack_layout_options(fill = X))	
		self.add_child(self.runs_list)

	def clear_list(self):
		self.runs_list.clear()

	def list_add_item(self, name):
		self.runs_list.add(name)

	def select_first_item(self):
		self.runs_list.select_first()		

	def get_selected_run(self):
		return self.runs_list.get_selected_value()