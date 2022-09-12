import os
from PIL import Image, ImageTk
from io import BytesIO
import win32clipboard

from ..common import Subject
from ..common import BehaviorSubject

class ImageModel(object):
	name = 'image_model'

	def __init__(self, app_context):
		self.image = BehaviorSubject(None)		
		self.copy = Subject(lambda _: self.on_copy())
	
	def on_copy(self):
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

	def load_image(self, path):
		print(f'load image for {path}')
		if (path == None):
			self.image.next(None)
		else:			
			print(f'loading image {path}')
			self.image.next(self.get_processed_image(Image.open(path)))