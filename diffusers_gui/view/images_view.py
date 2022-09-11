from tkinter import Frame, END, X

from .widgets import ListBox, Composite, Label, FIRST
from .layout import pack_layout_options

class ImagesView(Composite):
	name = 'images_view'

	def __init__(self, view_model, layout_options = None):
		super().__init__(layout_options = layout_options)
		self.view_model = view_model

	def select_first(self):
		self.images_list.select_first()

	def create(self, parent):
		super().create(parent)

		self.add_child(Label(var = "Images"))
		
		self.images_list = ListBox(lambda evt: self.on_image_select(evt), 
			var = self.view_model.images,
			auto_select = FIRST,
			layout_options = pack_layout_options(fill = X))		
		self.add_child(self.images_list)					

	def on_image_select(self, evt):
		self.view_model.image_selected.next(self.images_list.get_selected_value())		