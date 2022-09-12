from tkinter import filedialog
from . import ImageViewModel
from ..common import Subject, map, tap

class ReferenceImageViewModel(ImageViewModel):

	def __init__(self, model, title = ''):
		super().__init__(model, title)
		def on_open_ref_image(val):
			result = filedialog.askopenfilename(
				filetypes = [("PNG", "*.png"), ("Jpg", "*.jpg"), ("Jpeg", "*.jpeg")])
			if result != None and len(result) > 0:
				model.open_ref_image.next(result)
		self.load_ref_image_clicked = Subject(on_open_ref_image)
