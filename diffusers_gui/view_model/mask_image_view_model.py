from tkinter import filedialog

from . import ImageViewModel
from ..common import Subject, map 

class MaskImageViewModel(ImageViewModel):

	def __init__(self, model, title = ''):
		super().__init__(model, title)

		def on_open_mask_image(val):
			result = filedialog.askopenfilename(
				filetypes = [("PNG", "*.png"), ("Jpg", "*.jpg"), ("Jpeg", "*.jpeg")])
			if result != None and len(result) > 0:
				model.open_mask_image.next(result)
		self.load_mask_image_clicked = Subject(on_open_mask_image)

		def clear_mask_image(val):
			model.clear_mask_image.next()
		self.clear_mask_image_clicked = Subject(clear_mask_image)

		self.clear_mask_image_enabled = model.image.pipe(map(lambda val, idx: val != None))		