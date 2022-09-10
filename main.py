import argparse
from diffusers_gui import MainWindow, Namespace, AppContext

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
	app_context.sessions_model.load()
	main_window = MainWindow(app_context)
	main_window.start()	

if __name__ == "__main__":
	main()