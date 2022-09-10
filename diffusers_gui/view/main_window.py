import tkinter as tk
from tkinter import Tk, Frame, LEFT, X

from .layout import RowLayout, pack_layout_options

from .widgets import View, ContainerView

# Views
from . import (
	SessionsView, RunsView, RunInfoView, ImagesView, 
	ImageView, ParamsView, SelectedImageView
)

# View Models
from ..view_model import (
	ParamsViewModel, SessionsViewModel, ImageViewModel, ImagesViewModel, 
	RunInfoViewModel, RunsViewModel
)

class MainWindow:
	name = 'main_window'
	
	def __init__(self, app_context):
		self.root = tk.Tk()
		self.root.title('Stable Diffusion GUI')
		self.root.geometry("1650x1200")
		
		main_view = ContainerView(RowLayout())

		main_view.add_child(ContainerView(layout_options = pack_layout_options(fill = X))			
			.add_child(SessionsView(
				SessionsViewModel(app_context.sessions_model, app_context)))
			.add_child(RunsView(RunsViewModel(app_context.runs_model, app_context)))
			.add_child(RunInfoView(RunInfoViewModel(app_context.run_model, app_context)))
			.add_child(ImagesView(ImagesViewModel(app_context.images_model, app_context), 
				layout_options = pack_layout_options(fill = X)))
		)

		main_view.add_child(ContainerView()		
			.add_child(ImageView(ImageViewModel(app_context.input_image_model, app_context, 'Input Image')))
			.add_child(SelectedImageView(ImageViewModel(
				app_context.image_model, app_context, 'Selected Image')))
		)

		main_view.add_child(ContainerView()
			.add_child(ImageView(ImageViewModel(app_context.mask_image_model, app_context, 'Mask Image')))
		)
		
		main_view.add_child(ParamsView(ParamsViewModel(app_context.params_model, app_context)))

		main_view.create(self.root)
		main_view.layout()

		main_view.pack()

	def start(self):
		self.root.mainloop()