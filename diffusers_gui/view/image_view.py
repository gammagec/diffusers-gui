from tkinter import Frame, NW, LEFT, DISABLED, NORMAL

from .widgets import Button, Composite, Label, Canvas
from .layout import RowLayout

class ImageView(Composite):
	name = 'image_view'

	def __init__(self, view_model):
		super().__init__()		
		self.view_model = view_model					

	def create(self, parent):
		super().create(parent)
		view_model = self.view_model		

		self.buttons_view = (			
				Composite(RowLayout())
				.add_child(Button("Copy Image", 			
					lambda: self.view_model.copy_clicked.next(),
					enabled_value = view_model.copy_button_enabled))
			)

		self.add_child(Label(view_model.title))
		self.canvas = Canvas(self.view_model.image, 512, 512,
			view_model.mouse_handler)
		self.add_child(self.canvas)
		self.add_child(self.buttons_view)		

		super().create(parent)
								
	def get_buttons_view(self):
		return self.buttons_view

	def render_image(self, image):
		self.canvas.render(image)

	def clear_image(self):
		if self.is_created():
			self.canvas.clear()

			