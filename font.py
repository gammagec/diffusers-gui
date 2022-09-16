import argparse, re, os
from PIL import Image, ImageFont, ImageDraw
#from fontTools.ttLib import ttfont
from fontTools import ttLib
from itertools import chain
from fontTools.unicode import Unicode
from diffusers_gui import DiffusersService 

parser = argparse.ArgumentParser()

parser.add_argument(
    "--input",
    type=str,
    nargs="?",
    default="../fonts/Roboto-Regular.ttf",
    help="the font file to convert"
)

parser.add_argument(
    "--output",
    type=str,
    nargs="?",
    default="output/fonts",
    help="folder to output the converted font"
)

parser.add_argument(
    "--w",
    type=int,
    nargs="?",
    default=512,
    help="the width of font"
)

parser.add_argument(
    "--h",
    type=int,
    nargs="?",
    default=512,
    help="the height of font"
)

parser.add_argument(
    "--size",
    type=int,
    nargs="?",
    default=60,
    help="the size of font"
)

opt = parser.parse_args()

font_file = ttLib.TTFont(opt.input)
w = opt.w
h = opt.h

chars = chain.from_iterable(
    [y + (Unicode[y[0]], )
    for y in x.cmap.items()] for x in font_file['cmap'].tables)
chars = set(chars)
chars = sorted(chars, key=lambda c: int(c[0]))
font_file.close()
font = ImageFont.truetype(opt.input, opt.size) 

base = os.path.basename(opt.output)
dirs = os.path.splitext(base)[0]
if not os.path.exists(dirs):
    os.mkdir(dirs)

service = DiffusersService()

for c in chars:
    if re.match('.notdef|nonmarkingreturn|.null', c[1]):
        continue
    if (c[0] >= 65 and c[0] <= 122):
        print("got char " + chr(c[0]))
        img = Image.new('RGB', (w, h), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        (ws, hs) = font.getsize(chr(c[0]))
        wb = (w - ws) * 0.5
        hb = (h - hs) * 0.5
        draw.text((wb, hb), chr(c[0]), (0, 0, 0), font = font)
        draw = ImageDraw.Draw(img)
        img.save(f'{opt.output}/{c[0]}.png')

        service.run_img2img(
            out_dir, seed, ddim_steps, n_samples,
            n_iter, prompt, ddim_eta, H, W, C, f, scale, init_img,
            strength, session_name, after_run);
        