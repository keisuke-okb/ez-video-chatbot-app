import re
import os
import glob

def split_text(text):
    pattern = r'(?<=[。！？!?])'
    sentences = re.split(pattern, text)
    sentences = [sentence for sentence in sentences if sentence]
    return sentences

def delete_files_in_folder(folder_path):
    files = glob.glob(os.path.join(folder_path, '*'))
    for file in files:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))