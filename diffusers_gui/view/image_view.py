from tkinter import Label, Frame, Button, NW, LEFT, DISABLED, NORMAL

from .widgets import ButtonView, ContainerView, LabelView, CanvasView
from .layout import RowLayout

class ImageView(ContainerView):
	name = 'image_view'

	def __init__(self, view_model):
		super().__init__()		
		self.view_model = view_model	
		view_model.set_view(self)					

	def create(self, parent):
		super().create(parent)
		view_model = self.view_model		

		self.buttons_view = (			
				ContainerView(RowLayout())
				.add_child(ButtonView("Open", 			
					lambda: self.view_model.open_clicked(),
					enabled_intvar = view_model.open_button_enabled))
				.add_child(ButtonView("Copy Image", 			
					lambda: self.view_model.copy_clicked(),
					enabled_intvar = view_model.copy_button_enabled))
			)

		self.add_child(LabelView(view_model.title))
		self.canvas = CanvasView(512, 512)
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

			