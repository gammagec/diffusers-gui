from tkinter import Frame, X, END, simpledialog, messagebox, LEFT

from .widgets import Composite, Label, ListBox, Button
from .layout import pack_layout_options, RowLayout

class SessionsView(Composite):
	name = 'session_view'
	
	def __init__(self, view_model):
		super().__init__()
		self.view_model = view_model	
		view_model.set_view(self)			

	def create(self, parent):
		super().create(parent)
		
		self.add_child(Label(var = "Sessions"))
		
		self.sessions_list = ListBox(
			lambda evt: self.view_model.on_session_clicked(
				self.sessions_list.get_selected_value()),
			var = self.view_model.list_items,
			layout_options = pack_layout_options(fill = X))
		self.add_child(self.sessions_list)

		self.add_child((
			Composite(RowLayout())
			.add_child(Button(var = "+", 
				handler = lambda: self.view_model.on_new_session_clicked()))
			.add_child(Button(var = "-", 
				handler = lambda: self.view_model.on_delete_session_clicked()))
		))

	def get_new_session_name(self):
		return simpledialog.askstring("Input", "New session name?", parent = self.get_frame())

	def confirm_session_delete(self):
		return messagebox.askyesno(
				"Confirmation", 
				"There are runs in this session, are you sure you want to delete it?", 
				parent = self.frame)

	def select_last(self):
		self.sessions_list.select_last()		

	def clear_selection(self):
		self.sessions_list.clear_selection()