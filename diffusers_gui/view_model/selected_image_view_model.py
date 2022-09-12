from . import ImageViewModel
from ..common import Subject, map, tap

class SelectedImageViewModel(ImageViewModel):

	def __init__(self, model, title = ''):
		super().__init__(model, title)

		self.open_button_enabled = model.image.pipe(
			map(lambda val, index: val != None),
			tap(lambda val: print(f'open button got enabled value {val}'))
		)		
		self.open_clicked = Subject(lambda _: self.model.open.next())