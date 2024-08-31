from PIL import Image
import os

from constants import Constants

def create_vertical_image(folder_path, padding=8, padding_role=24, overlay_image=None):
    files = os.listdir(folder_path)
    png_files = sorted([f for f in files if f.endswith('.png')], key=lambda x: int(x.split('_')[0]), reverse=True)

    images = [os.path.join(folder_path, f) for f in png_files]
    new_image = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))

    y = 700
    current_role = None
    for image in images:
        img = Image.open(image)
        h = img.height
        role = os.path.basename(image).split(".")[0].split("_")[1]
        if current_role is not None:
            if role != current_role:
                p = padding_role
            else:
                p = padding
        else:
            p = padding

        y -= h + p
        new_image.paste(img, (1250, y))
        print(f"y:{y}, h:{h}")
        current_role = role
        if y + h < 0:
            break
    
    if overlay_image is not None:
        overlay_img = Image.open(overlay_image).convert("RGBA").resize((600, 600))
        new_image.paste(overlay_img, (100, 200), overlay_img)
    
    new_image.save(Constants.CONCAT_CHAT_IMAGE)

# create_vertical_image("./chats")