from wand.color import Color
from wand.image import Image

with Image(filename='stifResult.png') as img:
    img.resize(140, 92)
    img.background_color = Color('skyblue')
    img.virtual_pixel = 'background'
    args = (
        10,10,15,15,
        60,0,40,10,
        0,60,16,40
    )
    img.brightness_contrast(int(-20),int(33),'all_channels')
    img.save(filename='./brightnessexp.png')