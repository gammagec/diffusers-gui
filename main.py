import argparse
from diffusers_gui import MainWindow, Namespace, AppContext
from diffusers_gui import Observable, Subscriber, map, Subject

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument(
		"--config",
		type=str,
		nargs="?",
		default="config/config.yaml",
		help="the config file to use"
	)

	opt = parser.parse_args()

	app_context = AppContext()
	app_context.config.load(opt.config)		
	main_window = MainWindow(app_context)
	app_context.sessions_model.load()
	main_window.start()		

	#clicks = Subject()
	#positions = clicks.pipe(
	#	map(lambda ev, index: ev['x']),
	#	map(lambda pos, index: pos + 1)
	#)
	#positions.subscribe(lambda val: print(f'position: {val}'))	
	#clicks.next({'x': 1})
	#clicks.next({'x': 2})

if __name__ == "__main__":
	main()