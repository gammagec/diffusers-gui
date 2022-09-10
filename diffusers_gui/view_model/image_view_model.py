from PIL import ImageTk
from tkinter import IntVar, StringVar

from ..common import ValueSubject

class ImageViewModel:

	def __init__(self, model, app_context, title = ''):
		self.title = title
		self.photo_img = None
		self.model = model
		self.open_button_enabled = ValueSubject(False)
		self.copy_button_enabled = ValueSubject(False)
		self.use_button_enabled = ValueSubject(False)
		self.copy_seed_button_enabled = ValueSubject(False)
		model.image_loaded.register(self, lambda loaded: self.on_image_loaded(loaded))

	def set_view(self, view):
		self.view = view

	def on_image_loaded(self, loaded):
		if (loaded):
			print('rendering image')
			self.photo_img = ImageTk.PhotoImage(self.model.image)
			self.view.render_image(self.photo_img)	
			self.open_button_enabled.set_value(True)		
			self.copy_button_enabled.set_value(True)
			self.use_button_enabled.set_value(True)		
			self.copy_seed_button_enabled.set_value(True)
			print('image rendered')
		else:
			self.view.clear_image()
			self.open_button_enabled.set_value(False)		
			self.copy_button_enabled.set_value(False)
			self.use_button_enabled.set_value(False)		
			self.copy_seed_button_enabled.set_value(False)

	def open_clicked(self):
		self.model.open()

	def use_image_clicked(self):
		self.model.use_image()

	def copy_clicked(self):
		self.model.copy()

	def copy_seed_clicked(self):
		self.model.copy_seed()