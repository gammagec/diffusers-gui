from types import SimpleNamespace

from . import Subscriber, Observer

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

		self.destination = ConsumerObserver(partial_observer)