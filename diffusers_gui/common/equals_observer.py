from . import BehaviorSubject

class EqualsObserver(BehaviorSubject):
	def __init__(self, subject, expect):		
		super().__init__(subject.get_value() == expect)
		self.subject = subject
		self.expect = expect

		subject.subscribe(lambda value: self.on_change())

	def on_change(self):
		self.next(self.subject.get_value() == self.expect)