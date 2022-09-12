import argparse
from diffusers_gui import MainWindow, Namespace, AppContext
from diffusers_gui import Observable, Subscriber, map, Subject
from diffusers_gui import RealEsrganService
from PIL import Image

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

	#real_esrgan_service = RealEsrganService()
	#print('doing esrgan')

	#img = Image.open("data/esrgan/lena_blurred.png")
	#(h, w) = img.size
	#print(f'doing esrgan on an {w} by {h} image')
	#out = real_esrgan_service.process(img)

	#h *= 4
	#w *= 4
	#print(f'new size {w} {h}')
	#out.save("data/esrgan/lena_out.png")

if __name__ == "__main__":
	main()