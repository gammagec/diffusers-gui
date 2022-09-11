class Subscription:

	def __init__(self, initial_teardown = None):		
		self.closed = False		
		self.teardowns = []
		if initial_teardown != None:
			self.teardowns.append(initial_teardown)

	def unsubscribe(self):
		if not self.closed:
			self.closed = True
		for teardown in self.teardowns:
			teardown()

	def add(self, teardown):
		self.teardowns.append(teardown)

	def remove(self, teardown):
		self.teardowns.remove(teardown)

	def EMPTY():
		empty = Subscription()
		empty.closed = True
		return empty

def is_subscription(val):
	return isinstance(val, Subscription) or (	
		hasattr(val, 'closed') and
		hasattr(val, 'remove') and
		hasattr(val, 'add') and
		hasattr(val, 'unsubscribe')
	)

EMPTY_SUBSCRIPTION = Subscription.EMPTY()
