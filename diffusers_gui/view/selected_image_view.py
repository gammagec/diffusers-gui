from tkinter import Frame, Canvas, NW, LEFT, DISABLED


from .widgets import Button
from . import ImageView

from ..common import bind_enabled_to_intvar

class SelectedImageView(ImageView):
	name = 'selected_image_view'

	def __init__(self, view_model):
		super().__init__(view_model)
		self.view_model = view_model

	def create(self, parent):		
		super().create(parent)
		buttons = super().get_buttons_view()

		buttons.add_child(Button("Open", 			
					lambda: self.view_model.open_clicked.next(),
					enabled_value = self.view_model.open_button_enabled))

		buttons.add_child(Button("Use Image", lambda: self.view_model.use_image_clicked.next(),
			enabled_value = self.view_model.use_button_enabled))

		buttons.add_child(Button("Copy Seed", lambda: self.view_model.copy_seed_clicked.next(),
			enabled_value = self.view_model.copy_seed_button_enabled))		
