import os
from PIL import Image
from io import BytesIO
import win32clipboard

from . import ImageModel

from ..common import Subject
from ..common import BehaviorSubject

class SelectedImageModel(ImageModel):
	name = 'selected image_model'

	def __init__(self, app_context):
		super().__init__(app_context)
		self.selection_model = app_context.selection_model
		self.images_model = app_context.images_model

		self.selection_model.image_selected.subscribe(lambda val: self.load_selected_image(val))

		self.open = Subject(lambda _: self.on_open())
		self.copy_seed = Subject()
		self.use_image = Subject(lambda _: self.on_use_image())
		self.input_image_model = app_context.input_image_model

	def on_open(self):
		path = self.get_image_path(self.selection_model.image_selected.get_value())
		if (path != None):						
			print(f'opening image {path}')
			os.startfile(path)

	def load_selected_image(self, path):
		print(f'loading selected image {path}')
		self.load_image(self.get_image_path(path))

	def get_image_path(self, val):
		if not val:
			return None
		path = os.path.join(self.images_model.images_path, val)
		return path

	def get_processed_image(self, image):
		return image

	def on_use_image(self):
		self.input_image_model.image.next(self.image.get_value())