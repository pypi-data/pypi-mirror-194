import json
from PIL import Image, ImageDraw
import smartcrop
from pixelate import pixelate
from multiskin import model
import traceback
from pathlib import Path    

# possible sizes
# 22 x 17 (20 kb max size) = 64x32
# 44 x 34 (40 kb max size) = 128x64
# 88 x 68 (60 kb max size) = 256x128
# 176 x 136 (80 kb max size) = 512x256
# 352 x 272 (100 kb max size) = 1024x512 save file size (has to be 2:1 ratio on w/h)

# bottom is 321x30
# left side is 514*31 (257 + 16?)
# front and back are both 321

def smart_crop_image(filepath: str):
    print("Step 2: Smart crop image...")
    # crop output
    img_to_crop = Image.open(filepath).convert("RGB")
    sc = smartcrop.SmartCrop()
    # scale has to be 0.35 at most (1 / ((512*512) / (352*272)))
    # could either smart crop to correct size, or smart crop to a more cape-focused size (a portrait img) and then resize NEAREST
    result = sc.crop(img_to_crop, 512, 396, prescale=False, min_scale=0.8, max_scale=0.8)

    box = (
        result['top_crop']['x'],
        result['top_crop']['y'],
        result['top_crop']['width'] + result['top_crop']['x'],
        result['top_crop']['height'] + result['top_crop']['y']
    )

    # cropped_image.thumbnail((200, 200), Image.ANTIALIAS)
    cropped_image = img_to_crop.crop(box)
    # cropped_image.save(f"{files[0][:-4]}.png", 'PNG', quality=90)

    crop_filepath = f"{Path(filepath).stem}_cropped.png"
    cropped_image.save(crop_filepath, 'PNG', quality=90)
    print("Step 2: Smart crop image, finished.")
    return crop_filepath

def pixelate_image(filepath, output_path):
    # pixelate output
    pixelate(filepath, output_path, 4)
    # Image.open(filepath).save(output_path)
    print("Step 3: Pixelate cropped image, finished.")

def format_as_cape(pixelated_filepath):
    # pixelating it changes its size, so call resize afterwards
    smaller_image_size = (374, 289) # (352 + 22, 272 + 17)
    image = Image.open(pixelated_filepath).resize(smaller_image_size, Image.Resampling.NEAREST)
    
    # move bottom box to right place
    bottom_box_pos = (16, 272, 176, 287) # left, upper [273 = (514/2) height of left side box over 2, + 16 vertical offset of left side], right [352//2 width of bottom box over 2 + 16], down [height of bottom box + offset = 273+15]
    bottom_box = image.crop(bottom_box_pos)
    image.paste(bottom_box, (176, 0)) # 160 = 352/2 - 16

    strip_box_size = (1024, 200)
    strip_box = Image.new("RGBA", strip_box_size, (255, 255, 255, 0))
    image.paste(strip_box, (0, 272))
    
    # move right side to right place - put back face in a variable, move right side then paste back side offsetted
    right_box_pos = (336, 15, 352, 272)
    right_box = image.crop(right_box_pos)
    back_box_pos = (176, 15, 336, 272)
    back_box = image.crop(back_box_pos)
    image.paste(right_box, (176, 15)) # 160 = 352/2 - 16
    image.paste(back_box, (192, 15)) # 160 = 352/2 - 16

    # crop image to size, removes excess from slightly larger smart crop (needed for the bottom of the cape)
    cropped_img = image.crop((0, 0, 352, 272))
    # cropped_img.save("files/3_cape_before_canvassing.png")

    # paste into canvas
    canvas = Image.new('RGBA', (1024, 512), color=(255, 255, 255, 0))
    canvas.paste(cropped_img, (0, 0))
    # create empty cape corner boxes
    rect_size = (16, 15) # (31, 30)
    corner_box_1_pos = (0, 0)
    corner_box_2_pos = (336, 0)
    rect = Image.new("RGBA", rect_size, (255, 255, 255, 0))
    canvas.paste(rect, corner_box_1_pos)
    canvas.paste(rect, corner_box_2_pos)
    
    final_filepath = f"{Path(pixelated_filepath).stem}_final.png"
    canvas.save(final_filepath)

    # canvas.resize((64, 32), Image.Resampling.NEAREST).save(final_filename)
    print("Step 3: Format as cape, finished.")
    return final_filepath


def post_process_cape(cape_filepath: str):
    cropped_img_filepath = smart_crop_image(cape_filepath)
    final_filepath = f"{Path(cape_filepath).stem}_pixelated.png"
    pixelate_image(cropped_img_filepath, final_filepath) 
    processed_cape_filepath = format_as_cape(final_filepath)
    return processed_cape_filepath