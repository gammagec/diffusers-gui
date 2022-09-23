import os
from PIL import Image, ImageTk
from io import BytesIO
import win32clipboard
from resizeimage import resizeimage
from tkinter import filedialog

from ..common import Subject
from ..common import BehaviorSubject

class ImageModel(object):
	name = 'image_model'

	def __init__(self, app_context):
		self.image = BehaviorSubject(None)		
		self.copy = Subject(lambda _: self.on_copy())
		self.enhance = Subject(lambda _: self.on_enhance())
		self.real_esrgan_service = app_context.real_esrgan_service
	
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

	def on_enhance(self):
		out = self.real_esrgan_service.process(self.image.get_value())
		result = filedialog.asksaveasfilename(
			filetypes = [("PNG", "*.png"), ("Jpg", "*.jpg"), ("Jpeg", "*.jpeg")])
		out.save(result)

	def get_processed_image(self, image):
		return image

	def load_image(self, path):
		print(f'load image for {path}')
		if (path == None):
			self.image.next(None)
		else:			
			print(f'loading image {path}')
			img = Image.open(path)
			(w, h) = img.size
			#if (w != 512 and h != 512):
			#	if (w > h):
			#		new_width = 512
			#		new_height = int((new_width / w) * h)
			#	else:
			#		new_height = 512
			#		new_width = int((new_height / h) * w)
			#	img = img.resize((new_width, new_height))
			#	img = resizeimage.resize_contain(img, [512, 512])
			self.image.next(self.get_processed_image(img))