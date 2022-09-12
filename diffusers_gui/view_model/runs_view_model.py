class RunsViewModel:

	def __init__(self, model):
		self.model = model
		model.update_runs_subject.subscribe(lambda _: self.update_runs())
		model.select_recent_subject.subscribe(lambda _: self.select_recent())

	def set_view(self, view):
		self.view = view

	def select_recent(self):
		self.view.select_first_item()

	def on_run_select(self, run):
		self.model.on_run_select(run)

	def update_runs(self):
		self.view.clear_list()
		for name in self.model.runs:
			self.view.list_add_item(name)