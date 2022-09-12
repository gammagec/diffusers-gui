from . import Subject

class BehaviorSubject(Subject):
	def __init__(self, value, name = 'Unknown ValueSubject'):				
		self.value = value
		super().__init__(name = name)		

	def next(self, value):
		self.value = value
		super().next(value)

	def get_value(self):
		return self.value

	def subscribe_(self, subscriber):
		subscription = super().subscribe_(subscriber)
		if not subscription.is_closed():
			subscriber.next(self.value)
		return subscription