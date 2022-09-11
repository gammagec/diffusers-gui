from types import SimpleNamespace

from . import create_operator_subscriber, operate

def tap(observerOrNext, error = None, complete = None):
	tap_observer = SimpleNamespace(
		subscribe = lambda *arg: None,
		unsubscribe = lambda *arg: None,
		finalize = lambda *arg: None,
		next = observerOrNext,
		error = error,
		complete = complete
	)

	def do_operate(src, subscriber):
		def on_next(val):
			tap_observer.next(val)
			subscriber.next(val)
		def on_complete():
			tap_observer.complete()
			subscriber.complete()
		def on_error(err):
			tap_observer.err(err)
			subscriber.err(err)
		def on_finalize():
			tap_observer.unsubscribe()
			tap_observer.finalize()
		src.subscribe(
			create_operator_subscriber(subscriber, on_next, on_complete, on_error, on_finalize))
	return operate(do_operate)