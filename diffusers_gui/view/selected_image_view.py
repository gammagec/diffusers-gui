from tkinter import Label, Frame, Canvas, NW, LEFT, DISABLED

from . import ImageView, ButtonView

from ..common import bind_enabled_to_intvar

class SelectedImageView(ImageView):
	name = 'selected_image_view'

	def __init__(self, view_model):
		super().__init__(view_model)
		self.view_model = view_model

	def create(self, parent):		
		super().create(parent)
		buttons = super().get_buttons_view()

		use_image = ButtonView("Use Image", lambda: self.view_model.use_image_clicked(),
			enabled_intvar = self.view_model.use_button_enabled)			
		buttons.add_child(use_image)

		copy_seed = ButtonView("Copy Seed", lambda: self.view_model.copy_seed_clicked(),
			enabled_intvar = self.view_model.copy_seed_button_enabled)				
		buttons.add_child(copy_seed)		