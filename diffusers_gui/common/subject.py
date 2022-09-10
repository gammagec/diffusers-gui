class Subject(object):
	def __init__(self, name = 'Unknown Subject'):
		self.name = name
		self.subscribers = dict()

	def register(self, who, callback = None):
		self.subscribers[who] = callback

	def unregister(self, who):
		del self.subscribers[who]

	def dispatch(self, val = None):
		for subscriber, callback in self.subscribers.items():
			sub_name =  subscriber.name if hasattr(subscriber, 'name') else 'unknown'			
			print(f'{self.name} dispatching to {sub_name} with value {val}')
			callback(val)

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
		self.register(self, process)		
		return new_sub