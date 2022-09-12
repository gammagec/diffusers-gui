from tkinter import filedialog

from . import ImageViewModel
from ..common import Subject, map 

class InputImageViewModel(ImageViewModel):

	def __init__(self, model, title = ''):
		super().__init__(model, title)

		def on_open_init_image(val):
			result = filedialog.askopenfilename(
				filetypes = [("PNG", "*.png"), ("Jpg", "*.jpg"), ("Jpeg", "*.jpeg")])
			if result != None and len(result) > 0:
				model.open_init_image.next(result)
		self.load_init_image_clicked = Subject(on_open_init_image)

		def clear_init_image(val):
			model.clear_init_image.next()
		self.clear_init_image_clicked = Subject(clear_init_image)

		self.clear_init_image_enabled = model.image.pipe(map(lambda val, idx: val != None))		