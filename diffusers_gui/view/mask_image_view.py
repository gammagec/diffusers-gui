from . import ImageView
from .widgets import Button

class MaskImageView(ImageView):
	def __init__(self, view_model):
		super().__init__(view_model)

	def create(self, parent):		
		super().create(parent)
		buttons = super().get_buttons_view()

		buttons.add_child(Button("Load Mask Image", 
			lambda: self.view_model.load_mask_image_clicked.next()))

		buttons.add_child(Button("Clear",
			lambda: self.view_model.clear_mask_image_clicked.next(),
			enabled_value = self.view_model.clear_mask_image_enabled))		

		buttons.add_child(Button("Reset",
			lambda: self.view_model.reset_mask_image_clicked.next()))		

		buttons.add_child(Button("Erase",
			lambda: self.view_model.erase_clicked.next()))		

		buttons.add_child(Button("Restore",
			lambda: self.view_model.restore_clicked.next()))		