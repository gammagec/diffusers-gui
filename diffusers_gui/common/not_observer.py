from . import ValueSubject

class NotObserver(ValueSubject):
	def __init__(self, subject):		
		super().__init__(not subject.get_value())
		self.subject = subject

		subject.subscribe(lambda value: self.on_change())

	def on_change(self):
		self.set_value(not self.subject.get_value())