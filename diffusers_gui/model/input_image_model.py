from PIL import ImageTk

from .image_model import ImageModel

from ..common.subject import Subject

class InputImageModel(ImageModel):
	name = 'input_image_model'

	def __init__(self, app_context):
		super().__init__(app_context)		
		self.open_init_image = Subject(lambda val: self.load_image(val))
		self.clear_init_image = Subject(lambda val: self.load_image(None))