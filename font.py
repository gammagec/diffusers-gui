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
    "--prompt",
    type=str,
    nargs="?",
    default='a pile of bones in the shape of <c>',
    help="prompt to use for each character"
)

parser.add_argument(
    "--size",
    type=int,
    nargs="?",
    default=450,
    help="the size of font"
)

parser.add_argument(
    "--strength",
    type=float,
    nargs="?",
    default=1,
    help="strength of init image"
)

parser.add_argument(
    "--seed",
    type=int,
    nargs="?",
    default=45,
    help="seed"
)

parser.add_argument(
    "--scale",
    type=float,
    nargs="?",
    default=12,
    help="guidance scale"
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

total_x = 10
total_y = int((122-65) / 10) + 1
grid = Image.new('RGB', (total_x * 100, total_y * 100))
x = 0
y = 0
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

        prompt = opt.prompt.replace('<c>', chr(c[0]))
        print(f'using prompt {prompt}')
        if opt.strength < 1.0:
            image = service.run_img2img(
                '', opt.seed, 50, 1,
                1, opt.prompt, 0.0, 512, 512, 3, 8, opt.scale, img,
                opt.strength, '', lambda: 0)
        else:
            image = service.run_txt2img(
                '', opt.seed, 50, 1,
                1, opt.prompt, 0.0, 512, 512, 3, 8, opt.scale,
                '')

        image.save(f'{opt.output}/{c[0]}.png')
        image = image.resize((100, 100))
        grid.paste(image, (x, y))
        x += 100
        if x > (total_x-1) * 100:
            x = 0
            y += 100
grid.save(f'{opt.output}/grid.png')
        