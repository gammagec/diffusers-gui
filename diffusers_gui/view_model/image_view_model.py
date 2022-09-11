from tkinter import StringVar

from ..common import Subject, map_op, tap

class ImageViewModel:

	def __init__(self, model, app_context, title = ''):
		self.title = title
		self.photo_img = None
		self.model = model
		self.open_button_enabled = model.image.pipe(
			map_op(lambda val, index: val != None),
			tap(lambda val: print(f'open button got enabled value {val}'))
		)		
		self.copy_button_enabled = model.image.pipe(map_op(lambda val, idx: val != None))		
		self.use_button_enabled = model.image.pipe(map_op(lambda val, idx: val != None))		
		self.copy_seed_button_enabled = model.image.pipe(map_op(lambda val, idx: val != None))		
		self.image = model.image.pipe()

		self.open_clicked = Subject(lambda _: self.model.open.next())
		self.copy_clicked = Subject(lambda _: self.model.copy.next())
		self.use_image_clicked = Subject(lambda _: self.model.use_image.next())
		self.copy_seed_clicked = Subject(lambda _: self.model.copy_seed.next())
