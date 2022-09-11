from . import Subject

class ValueSubject(Subject):
	def __init__(self, initial_value, name = 'Unknown ValueSubject'):				
		self.value = initial_value
		super().__init__(name = name)		

	def set_value(self, value):
		self.value = value
		self.next(value)

	def get_value(self):
		return self.value

	def on_new_subscribe(self, callback):
		callback(self.value)