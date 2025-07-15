from PIL import Image
import sys

try:
    if len(sys.argv[1]) > 1:
        item = sys.argv[1]
except:
    raise ValueError("Please provide a valid item name as an argument.")


img = Image.open(item)
bg = Image.new("RGBA", img.size, (255, 255, 255, 0))
# img = Image.alpha_composite(bg, img)
bg.paste(img, (0, 0), img)
bg = bg.convert("RGB")
bg.save(item[:-4] + "_whitened.png", "PNG")
