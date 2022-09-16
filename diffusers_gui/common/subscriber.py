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
	
	def set_destination(self, destination):
		self.destination = destination

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
		self.destination.error(err)
		self.unsubscribe()

	def complete_(self):
		self.destination.complete()
		self.unsubscribe()

class ConsumerObserver(Observer):
	def __init__(self, observer):		
		self.observer = observer

	def next(self, val):
		if hasattr(self.observer, 'next'):
			self.observer.next(val)

	def error(self, err):
		pass

	def complete(self):
		pass

class SafeSubscriber(Subscriber):

	def __init__(self, observer_or_next, error = None, complete = None):
		super().__init__()

		partial_observer = None
		if callable(observer_or_next):
			partial_observer = SimpleNamespace(
				next = observer_or_next,
				error = error,
				complete = complete
			)
		else:
			partial_observer = observer_or_next

		#self.destination = ConsumerObserver(partial_observer)
		super().set_destination(ConsumerObserver(partial_observer))