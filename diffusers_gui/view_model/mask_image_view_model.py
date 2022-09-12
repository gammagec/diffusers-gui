from tkinter import filedialog

from . import ImageViewModel
from ..common import Subject, map 

class MaskMouseHandler:
	def __init__(self, model):
		self.model = model

	def down(self, x, y):
		self.model.paint_mask_at(x, y)		

	def drag(self, x, y):
		self.model.paint_mask_at(x, y)

class MaskImageViewModel(ImageViewModel):

	def __init__(self, model, title = ''):
		super().__init__(model, title)

		def on_open_mask_image(val):
			result = filedialog.askopenfilename(
				filetypes = [("PNG", "*.png"), ("Jpg", "*.jpg"), ("Jpeg", "*.jpeg")])
			if result != None and len(result) > 0:
				model.open_mask_image.next(result)
		self.load_mask_image_clicked = Subject(on_open_mask_image)

		self.reset_mask_image_clicked = Subject(lambda val: model.reset_mask_image())

		self.erase_clicked = Subject(lambda val: model.set_erase())
		self.restore_clicked = Subject(lambda val: model.set_restore())

		def clear_mask_image(val):
			model.clear_mask_image.next()
		self.clear_mask_image_clicked = Subject(clear_mask_image)

		self.clear_mask_image_enabled = model.image.pipe(map(lambda val, idx: val != None))	

		self.mouse_handler = MaskMouseHandler(model)