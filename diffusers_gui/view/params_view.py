from tkinter import WORD, LEFT, Frame, Entry, Label, scrolledtext, Checkbutton
from tkinter import LEFT, Button, END, DISABLED, NORMAL, W, E

from ..common import (
	bind_enabled_to_value_observer, bind_scrolledtext_to_stringvar,
	bind_enabled_to_intvar
)

from . import (
	ContainerView, LoadFileView, LabelView, EntryView, ButtonView, 
	ScrolledTextView, grid_layout_options, GridLayout
)

class ParamsView(ContainerView):
	name = 'params_view'

	def __init__(self, view_model):
		super().__init__(GridLayout())
		self.view_model = view_model

	def create(self, parent):
		super().create(parent)
		row = 0		
		self.add_child(LabelView(var = "Params",
			layout_options = grid_layout_options(row = row, column = 0)))
		row += 1
		
		self.add_child(LabelView(var = "Prompt:", 
			layout_options = grid_layout_options(row = row, column = 0, columnspan = 3, sticky = W)))			
		row += 1

		self.add_child(ScrolledTextView(self.view_model.prompt,
			layout_options = grid_layout_options(row = row, column = 0, columnspan = 3)))		
		row += 1

		self.add_child(LabelView(var = 'Image Prompt:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		

		self.add_child(LoadFileView(self.view_model.image_prompt,
			layout_options = grid_layout_options(row = row, column = 1, columnspan = 2, sticky = W)))		
		row += 1
		
		self.add_child(LabelView(var = 'Strength:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))			
		self.add_child(EntryView(var = self.view_model.strength,
			layout_options = grid_layout_options(row = row, column = 1)))		
		row += 1

		self.add_child(LabelView(var = "Seed:",
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(EntryView(var = self.view_model.seed,
			layout_options = grid_layout_options(row = row, column = 1)))					
		row += 1

		self.add_child(LabelView(var = 'DDIM Steps:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(EntryView(var = self.view_model.ddim_steps,
			layout_options = grid_layout_options(row = row, column = 1)))		
		row += 1

		self.add_child(LabelView(var = '# Samples:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(EntryView(var = self.view_model.n_samples,
			layout_options = grid_layout_options(row = row, column = 1)))		
		row += 1

		self.add_child(LabelView(var = '# Iterations:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(EntryView(var = self.view_model.n_iter,
			layout_options = grid_layout_options(row = row, column = 1)))		
		row += 1

		self.add_child(LabelView(var = 'Width:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(EntryView(var = self.view_model.width,
			layout_options = grid_layout_options(row = row, column = 1)))						
		row += 1

		self.add_child(LabelView(var = 'Height:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))
		self.add_child(EntryView(var = self.view_model.height,
			layout_options = grid_layout_options(row = row, column = 1)))						
		row += 1

		self.add_child(LabelView(var = 'Channels:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(EntryView(var = self.view_model.channels,
			layout_options = grid_layout_options(row = row, column = 1)))		
		row += 1

		self.add_child(LabelView(var = 'Downsampling:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(EntryView(var = self.view_model.downsampling,
			layout_options = grid_layout_options(row = row, column = 1)))		
		row += 1

		self.add_child(LabelView(var = 'Scale:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(EntryView(var = self.view_model.scale,
			layout_options = grid_layout_options(row = row, column = 1)))		
		row += 1	

		self.add_child(LabelView(var = 'Mask:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		

		self.add_child(LoadFileView(var = self.view_model.mask,
			layout_options = grid_layout_options(row = row, column = 1, columnspan = 2, sticky = W)))		

		row += 1

		self.add_child(ButtonView(var = 'Run', 
			handler = lambda: self.view_model.run_clicked(),
			enabled_value_observer = self.view_model.run_enabled,
			layout_options = grid_layout_options(row = row, column = 0)))

		self.add_child(ButtonView(var = 'Run Random Seed', 
			handler = lambda: self.view_model.run_random_clicked(),
			enabled_value_observer = self.view_model.run_enabled,
			layout_options = grid_layout_options(row = row, column = 1)))

		
	
