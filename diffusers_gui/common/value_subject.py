from . import Subject, Map, Tap

class ValueSubject(Subject):
	def __init__(self, initial_value, name = 'Unknown ValueSubject'):		
		super().__init__(name = name)
		self.value = initial_value

	def set_value(self, value):
		self.value = value
		self.dispatch(value)

	def get_value(self):
		return self.value	

	def pipe(self, *ops, name = None):
		new_sub = Subject(name = name)
		def process(val):
			new_val = val
			for op in ops:
				if isinstance(op, Map):
					new_val = op.map(new_val)
				if isinstance(op, Tap):
					op.tap(new_val)
			print(f'setting value after pipe {new_val}')
			new_sub.dispatch(new_val)
		self.register(new_sub, process)		
		return new_sub