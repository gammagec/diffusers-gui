from . import ImageView
from .widgets import Button

class ReferenceImageView(ImageView):

	def __init__(self, view_model):
		super().__init__(view_model)

	def create(self, parent):
		super().create(parent)
		buttons = super().get_buttons_view()

		buttons.add_child(Button("Load Ref Image", 
			lambda: self.view_model.load_ref_image_clicked.next()))