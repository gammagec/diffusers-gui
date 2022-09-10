class Subject(object):
	def __init__(self):
		self.subscribers = dict()

	def register(self, who, callback = None):
		self.subscribers[who] = callback

	def unregister(self, who):
		del self.subscribers[who]

	def dispatch(self):		
		for subscriber, callback in self.subscribers.items():
			sub_name = subscriber.name if hasattr(subscriber, 'name') else 'unknown'
			name = self.name if hasattr(self, 'name') else 'unknown'
			print(f'{name} dispatching to {sub_name}')
			callback()	