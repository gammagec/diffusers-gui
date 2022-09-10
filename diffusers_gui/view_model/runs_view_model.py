class RunsViewModel:

	def __init__(self, model, app_context):
		self.model = model
		model.update_runs_subject.register(self, lambda:self.update_runs())

	def set_view(self, view):
		self.view = view

	def on_run_select(self, run):
		self.model.on_run_select(run)

	def update_runs(self):
		self.view.clear_list()
		for name in self.model.runs:
			self.view.list_add_item(name)
		if (len(self.model.runs) > 0):
			self.view.select_first_item()			
		else:
			self.model.on_run_select(None)		