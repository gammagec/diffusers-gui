from functools import reduce

from . import Subscribable, Subscriber, is_subscription, SafeSubscriber

class Observable(Subscribable):

	def __init__(self, subscribe = None):
		self.subscribe_ = subscribe
		self.source = None
		self.operator = None

	def subscribe(self, observerOrNext, error = None, complete = None):
		subscriber = observerOrNext if is_subscriber(observerOrNext) else SafeSubscriber(
			observerOrNext)#, error, complete)
		if self.operator == None:
			subscriber.add(self.subscribe_(subscriber))
		else:
			self.operator(subscriber, self.source)	

	def pipe(self, *ops, name = 'Unknown Pipe'):
		return pipe_from_array(ops)(self)		

	def lift(self, operator):
		observable = Observable()
		observable.source = self
		observable.operator = operator
		return observable

def pipe_from_array(ops):
	if len(ops) == 0:
		return lambda ob: ob

	if len(ops) == 1:
		return ops[0]

	return lambda input: reduce(lambda prev, fn: fn(prev), ops, input)

def is_observer(val):
	return val and hasattr(val, 'next') and hasattr(val, 'error') and hasattr(val, 'complete')

def is_subscriber(val):
	#return (val and isinstance(val, Subscriber)) or (is_observer(val) and is_subscription(val))
	return val and isinstance(val, Subscriber) or (is_observer(val) and is_subscription(val))
