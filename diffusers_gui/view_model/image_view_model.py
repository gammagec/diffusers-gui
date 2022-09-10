from tkinter import StringVar

from ..common import ValueSubject, Map, Tap

class ImageViewModel:

	def __init__(self, model, app_context, title = ''):
		self.title = title
		self.photo_img = None
		self.model = model
		self.open_button_enabled = model.image.pipe(Map(lambda val: val != None))		
		self.copy_button_enabled = model.image.pipe(Map(lambda val: val != None))		
		self.use_button_enabled = model.image.pipe(Map(lambda val: val != None))		
		self.copy_seed_button_enabled = model.image.pipe(Map(lambda val: val != None))		
		self.image = model.image.pipe()

	def set_view(self, view):
		self.view = view

	def open_clicked(self):
		self.model.open()

	def use_image_clicked(self):
		self.model.use_image()

	def copy_clicked(self):
		self.model.copy()

	def copy_seed_clicked(self):
		self.model.copy_seed()