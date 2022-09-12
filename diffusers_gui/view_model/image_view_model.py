from tkinter import StringVar

from ..common import Subject, map, tap

class ImageViewModel:

	def __init__(self, model, title = ''):
		self.title = title
		self.model = model
		self.copy_button_enabled = model.image.pipe(map(lambda val, idx: val != None))		
		self.use_button_enabled = model.image.pipe(map(lambda val, idx: val != None))		
		self.copy_seed_button_enabled = model.image.pipe(map(lambda val, idx: val != None))		
		self.image = model.image.pipe()

		self.copy_clicked = Subject(lambda _: self.model.copy.next())
		self.use_image_clicked = Subject(lambda _: self.model.use_image.next())
		self.copy_seed_clicked = Subject(lambda _: self.model.copy_seed.next())

		self.mouse_handler = None
