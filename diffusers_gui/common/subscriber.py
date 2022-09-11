from types import SimpleNamespace
from . import Subscription, Observer, is_subscription

def noop(*args):
	pass

EMPTY_OBSERVER = SimpleNamespace(
	closed = True,
	next = noop,
	error = noop,
	complete = noop,
)

class Subscriber(Subscription, Observer):

	def __init__(self, destination = None):	
		super().__init__()	
		self.stopped = False
		if destination != None:
			self.destination = destination
			if is_subscription(destination):
				destination.add(self)
		else:
			self.destination = EMPTY_OBSERVER

	def next(self, val):
		if not self.stopped:
			self.next_(val)

	def error(self, err):
		if not self.stopped:
			self.stopped = True
			self.error_(err)

	def complete(self):
		if not self.stopped:
			self.stopped = True
			self.complete_()

	def unsubscribe(self):
		if not self.closed:
			self.stopped = True
			super().unsubscribe()
			self.destination = None

	def next_(self, val):
		self.destination.next(val)

	def error_(self, err):
		self.destination.error(val)
		self.unsubscribe()

	def complete_(self):
		self.destination.complete()
		self.unsubscribe()