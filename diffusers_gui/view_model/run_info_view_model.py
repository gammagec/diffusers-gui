class RunInfoViewModel:
	def __init__(self, model, app_context):
		self.model = model
		model.update_run_model_subject.register(self, lambda _: self.update_run())

	def set_view(self, view):
		self.view = view

	def update_run(self):
		text = None
		model = self.model
		if(model.run != None):
			self.view.update_text(
				f'prompt: {model.prompt}\n'
				f'size: {model.width}x{model.height}\n'
				f'ddim_eta: {model.ddim_eta}, ddim_steps: {model.ddim_steps}\n'
				f'n_iter: {model.n_iter}, n_samples: {model.n_samples}\n'								
				f'device: {model.device}, fixed_code: {model.fixed_code}\n'
				f'from_file: {model.from_file}\n'
				f'f: {model.f}, half: {model.half}\n'
				f'init_img: {model.init_img}\n'
				f'n_rows: {model.n_rows}\n'
				f'outdir: {model.outdir}\n'
				f'plms: {model.plms}\n'
				f'precision: {model.precision}\n'
				f'scale: {model.scale}\n'
				f'seed: {model.seed}\n'
				f'session_name: {model.session_name}\n'
				f'skip_grid: {model.skip_grid}, skip_save: {model.skip_save}\n'
				f'small_batch: {model.small_batch}\n'
				f'strength: {model.strength}\n'
			)