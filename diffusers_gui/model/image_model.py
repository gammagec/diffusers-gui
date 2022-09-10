import os
from PIL import Image, ImageTk
from io import BytesIO
import win32clipboard

from ..common.subject import Subject
from ..common.value_subject import ValueSubject

class ImageModel(object):
	name = 'image_model'

	def __init__(self, app_context):
		self.selection_model = app_context.selection_model
		self.images_model = app_context.images_model
		self.image = ValueSubject(None)
		self.copy_seed_value = Subject()
		self.use_image_value = Subject()		

		self.selection_model.image_selected.register(self, lambda _: self.load_image())

	def open(self):
		path = self.get_image_path()
		if (path != None):						
			print(f'opening image {path}')
			os.startfile(path)

	def get_image_path(self):
		img_name = self.selection_model.selected_image
		if not img_name:
			return None
		path = os.path.join(self.images_model.images_path, img_name)
		return path

	def copy_seed(self):		
		self.copy_seed_value.dispatch()

	def use_image(self):
		self.use_image_value.dispatch()
	
	def copy(self):
		path = self.get_image_path()		
		if (path != None):						
			print(f'copying image {path}')
			image = self.image.get_value().copy()
			output = BytesIO()
			image.convert("RGB").save(output, "BMP")
			data = output.getvalue()[14:]
			output.close()
			win32clipboard.OpenClipboard()
			win32clipboard.EmptyClipboard()
			win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
			win32clipboard.CloseClipboard()

	def get_processed_image(self, image):
		return image

	def load_image(self):
		path = self.get_image_path()
		print(f'load image for {path}')
		if (path == None):
			self.image.set_value(None)
		else:			
			print(f'loading image {path}')
			self.image.set_value(self.get_processed_image(Image.open(path)))