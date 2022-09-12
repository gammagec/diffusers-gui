from . import ImageView
from .widgets import Button

class InputImageView(ImageView):
	def __init__(self, view_model):
		super().__init__(view_model)


	def create(self, parent):		
		super().create(parent)
		buttons = super().get_buttons_view()

		use_image = Button("Load Init Image", 
			lambda: self.view_model.load_init_image_clicked.next())			
		buttons.add_child(use_image)

		copy_seed = Button("Clear",
			lambda: self.view_model.clear_init_image_clicked.next(),
			enabled_value = self.view_model.clear_init_image_enabled)				
		buttons.add_child(copy_seed)		