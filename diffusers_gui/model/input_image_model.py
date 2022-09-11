from PIL import ImageTk

from .image_model import ImageModel

from ..common.subject import Subject

class InputImageModel(ImageModel):
	name = 'input_image_model'

	def __init__(self, app_context):
		super().__init__(app_context)		
		self.params_model = app_context.params_model
		self.params_model.init_image.subscribe(lambda val: self.load_image())

	def get_image_path(self):
		return self.params_model.init_image.get_value()