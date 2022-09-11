from ..common import tap, Subject

class ImagesViewModel:

	def __init__(self, model, app_context):
		self.model = model
		self.images = model.images.pipe(
			tap(lambda val: f'got {len(val)} images set'),
			name = 'images pipe'
		)
		self.image_selected = Subject(lambda val: self.model.set_image(val))	

