class ImagesViewModel:

	def __init__(self, model, app_context):
		self.model = model
		model.update_images_subject.register(self, lambda: self.update_images())

	def set_view(self, view):
		self.view = view

	def update_images(self):
		print('updating images')
		self.view.clear_image_list()

		for name in self.model.images:
			self.view.add_image(name)
		if (len(self.model.images) > 0):
			self.view.select_first()			
		else:
			self.model.set_image(None)		

	def on_image_selected(self, image):
		self.model.set_image(image)

