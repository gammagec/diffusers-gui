from tkinter import Listbox, SINGLE, END

from . import View

def create_list_box(parent, select_command, listvariable = None):
	listbox = Listbox(parent, selectmode = SINGLE, exportselection = 0, listvariable = listvariable)
	listbox.bind('<<ListboxSelect>>', select_command)

	def on_arrow_up(evt):
		index = listbox.curselection()[0] - 1
		if 0 <= index < evt.widget.size():
			listbox.selection_clear(0, END)
			listbox.select_set(index)
			select_command(evt)

	def on_arrow_down(evt):
		index = listbox.curselection()[0] + 1
		if 0 <= index < evt.widget.size():
			listbox.selection_clear(0, END)
			listbox.select_set(index)
			select_command(evt)

	listbox.bind('<Down>', on_arrow_down)
	listbox.bind('<Up>', on_arrow_up)
	return listbox

class ListBoxView(View):

	def __init__(self, on_select, var = None, layout_options = None):
		super().__init__(layout_options)
		self.var = var
		self.on_select = on_select

	def select_first(self):
		self.listbox.select_set(0)
		self.listbox.event_generate("<<ListboxSelect>>")

	def select_last(self):
		self.clear_selection()
		self.listbox.selection_set(END)
		self.listbox.event_generate('<<ListboxSelect>>')

	def create(self, parent):
		super().create()
		self.listbox = create_list_box(parent, self.on_select, self.var)

	def clear_selection(self):
		self.listbox.selection_clear(0, END)
		self.listbox.event_generate('<<ListboxSelect>>')
	
	def clear(self):
		if self.is_created():
			self.listbox.delete(0, END)

	def add(self, item):
		if self.is_created():
			self.listbox.insert(END, item)		

	def get_frame(self):
		return self.listbox

	def get_selected_value(self):
		return self.listbox.get(self.listbox.curselection())