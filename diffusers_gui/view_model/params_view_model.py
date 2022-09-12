from tkinter import StringVar

from ..common import (
	EqualsObserver, NotObserver, AndObserver, bind_var_to_value_observer,
	BehaviorSubject, Subject
)

class ParamsViewModel(object):

	def __init__(self, model, app_context):
		self.model = model

		self.seed = BehaviorSubject(model.seed.get_value())
		self.ddim_steps = BehaviorSubject('')
		self.n_samples = BehaviorSubject('')
		self.n_iter = BehaviorSubject('')
		self.width = BehaviorSubject('')
		self.height = BehaviorSubject('')
		self.channels = BehaviorSubject('')
		self.downsampling = BehaviorSubject('')
		self.scale = BehaviorSubject('')				
		self.strength = BehaviorSubject('')
		self.prompt = StringVar()

		self.load_init_image_clicked = Subject(lambda val: self.on_load_init_image())
		self.load_mask_image_clicked = Subject(lambda val: self.on_load_mask_image())
		self.run_clicked = Subject(lambda val: self.run())
		self.run_random_clicked = Subject(lambda val: self.run_random())

		self.run_enabled = NotObserver(
			EqualsObserver(app_context.selection_model.selected_session, None))

		model.seed.subscribe(lambda val: self.seed.next(val))				
		
		self.update_from_model()

#	def on_load_init_image(self):
#		result = filedialog.askopenfilename(
#				filetypes = [("PNG", "*.png"), ("Jpg", "*.jpg"), ("Jpeg", "*.jpeg")])
#		if result != None and len(result) > 0:
#			self.model.open_init_image(result)

#	def on_load_mask_image(self):
#		result = filedialog.askopenfilename(
#				filetypes = [("PNG", "*.png"), ("Jpg", "*.jpg"), ("Jpeg", "*.jpeg")])
#		if result != None and len(result) > 0:
#			self.model.open_mask_image(result)

	def run_random(self):
		self.set_random_seed()
		self.run()

	def run(self):			
		self.params_to_model()
		self.model.on_run()

	def set_random_seed(self):
		self.model.set_random_seed()
		self.seed.next(str(self.model.seed.get_value()))

	def params_to_model(self):
		self.model.seed.next(int(self.seed.get_value()))
		self.model.ddim_steps = int(self.ddim_steps.get_value())
		self.model.n_samples = int(self.n_samples.get_value())
		self.model.n_iter = int(self.n_iter.get_value())
		self.model.ddim_eta = 0
		self.model.prompt = self.prompt.get()
		self.model.width = int(self.width.get_value())
		self.model.height = int(self.height.get_value())
		self.model.channels = int(self.channels.get_value())
		self.model.downsampling = int(self.downsampling.get_value())
		self.model.scale = float(self.scale.get_value())				
		self.model.strength = float(self.strength.get_value())

	def update_from_model(self):
		self.seed.next(str(self.model.seed.get_value()))
		self.ddim_steps.next(str(self.model.ddim_steps))		
		self.n_samples.next(str(self.model.n_samples))
		self.n_iter.next(str(self.model.n_iter))
		self.width.next(str(self.model.width))
		self.height.next(str(self.model.height))		
		self.channels.next(str(self.model.channels))
		self.downsampling.next(str(self.model.downsampling))
		self.scale.next(str(self.model.scale))				
		self.strength.next(str(self.model.strength))					