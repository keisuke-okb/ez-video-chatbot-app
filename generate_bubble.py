import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

import tools
from constants import Constants

def create_chat_bubble(text, role="user", mode="single", width=480, font_path='C:/Windows/Fonts/meiryob.ttc', font_size=32):
    padding = 30
    y_text_offset = -8
    assistant_user_margin = 80
    border_radius = font_size * 1.3
    c_user_bg = (*tools.hex_to_rgb(Constants.C_USER_BG), 255)
    c_user_text = (*tools.hex_to_rgb(Constants.C_USER_TEXT), 255)
    c_assistant_bg = (*tools.hex_to_rgb(Constants.C_ASSISTANT_BG), 255)
    c_assistant_text = (*tools.hex_to_rgb(Constants.C_ASSISTANT_TEXT), 255)
    font = ImageFont.truetype(font_path, font_size)
    wrapped_text = textwrap.fill(text, width=width // font_size)

    dummy_img = Image.new('RGBA', (width, 1), (255, 255, 255, 0))
    draw = ImageDraw.Draw(dummy_img)
    text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    img_height = text_height + padding * 2

    width_all = width + padding * 2 + assistant_user_margin

    img = Image.new('RGBA', (width_all, img_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    if role == "user":
        if mode == "single":
            draw.rounded_rectangle([(width_all - text_width - padding * 2, 0), (width_all, img_height)], radius=border_radius, fill=c_user_bg)
        
        elif mode == "start":
            draw.rounded_rectangle([(width_all - text_width - padding * 2, 0), (width_all, img_height)], radius=border_radius, fill=c_user_bg)
            draw.rounded_rectangle([(width_all - border_radius, border_radius), (width_all, img_height)], radius=0, fill=c_user_bg)

        elif mode == "middle":
            draw.rounded_rectangle([(width_all - text_width - padding * 2, 0), (width_all, img_height)], radius=border_radius, fill=c_user_bg)
            draw.rounded_rectangle([(width_all - border_radius, 0), (width_all, img_height)], radius=0, fill=c_user_bg)

        elif mode == "end":
            draw.rounded_rectangle([(width_all - text_width - padding * 2, 0), (width_all, img_height)], radius=border_radius, fill=c_user_bg)
            draw.rounded_rectangle([(width_all - border_radius, 0), (width_all, border_radius)], radius=0, fill=c_user_bg)

        draw.text((width_all - text_width - padding, padding + y_text_offset), wrapped_text, font=font, fill=c_user_text)
    
    else:
        if mode == "single":
            draw.rounded_rectangle([(0, 0), (text_width + padding * 2, img_height)], radius=border_radius, fill=c_assistant_bg)
        
        elif mode == "start":
            draw.rounded_rectangle([(0, 0), (text_width + padding * 2, img_height)], radius=border_radius, fill=c_assistant_bg)
            draw.rounded_rectangle([(0, border_radius), (border_radius * 2, img_height)], radius=0, fill=c_assistant_bg)

        elif mode == "middle":
            draw.rounded_rectangle([(0, 0), (text_width + padding * 2, img_height)], radius=border_radius, fill=c_assistant_bg)
            draw.rounded_rectangle([(0, 0), (border_radius * 2, img_height)], radius=0, fill=c_assistant_bg)

        elif mode == "end":
            draw.rounded_rectangle([(0, 0), (text_width + padding * 2, img_height)], radius=border_radius, fill=c_assistant_bg)
            draw.rounded_rectangle([(0, 0), (border_radius * 2, border_radius)], radius=0, fill=c_assistant_bg)

        draw.text((padding, padding + y_text_offset), wrapped_text, font=font, fill=c_assistant_text)
    

    chat_files = [f for f in os.listdir("chats") if f.endswith('.png')]
    numbers = [int(f.split('_')[0]) for f in chat_files]
    if numbers:
        num = max(numbers) + 1
    else:
        num = 0
    
    if role == "user":
        img.save(f'./chats/{num:04d}_U.png', 'PNG')
    elif role == "assistant":
        img.save(f'./chats/{num:04d}_A.png', 'PNG')
