from . import Subject

class ValueSubject(Subject):
	def __init__(self, initial_value):		
		super().__init__()
		self.value = initial_value

	def set_value(self, value):
		self.value = value
		self.dispatch()

	def get_value(self):
		return self.value

	def dispatch(self):
		for subscriber, callback in self.subscribers.items():
			sub_name =  subscriber.name if hasattr(subscriber, 'name') else 'unknown'
			name = self.name if hasattr(self, 'name') else 'unknown'
			print(f'{name} dispatching to {sub_name} with value {self.value}')
			callback(self.value)	