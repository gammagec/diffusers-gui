from ..common import Subject, BehaviorSubject

class SelectionModel:
	name = 'selection_model'

	def __init__(self, app_context):
		self.selected_session = BehaviorSubject(None)
		self.selected_run = None
		self.selected_image = None
		self.run_selected = Subject()
		self.image_selected = Subject()

	def set_selected_run(self, run):
		print(f'run set {run}')
		self.selected_run = run
		self.run_selected.next()	

	def set_selected_session(self, session):
		print(f'session set {session}')		
		self.selected_session.next(session)

	def set_selected_image(self, image):
		print(f'image set {image}')
		self.selected_image = image
		self.image_selected.next(image)