import tkinter as tk
import threading
import imageio
import os
from PIL import Image, ImageTk
from time import perf_counter, sleep

import tools
import chat
import tts
from stt import STTModel
from generate_bubble import create_chat_bubble
from concat_image import create_vertical_image
from constants import Constants

global finished
finished = False

class EZVideoChatBotApp:
    def __init__(self, root):
        self.root = root
        self.stt_model = STTModel()
        self.starting_video = Constants.STARTING_VIDEO
        self.waiting_video = Constants.WAITING_VIDEO
        self.speaking_video = Constants.SPEAKING_VIDEO
        self.overlay_image_path = Constants.CONCAT_CHAT_IMAGE
        self.c_user_bg = Constants.C_USER_BG
        self.c_user_text = Constants.C_USER_TEXT
        self.c_assistant_bg = Constants.C_ASSISTANT_BG
        self.c_assistant_text = Constants.C_ASSISTANT_TEXT
        self.init_message = Constants.INIT_MESSAGE
        self.system_prompt = Constants.SYSTEM_PROMPT
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]

        self.videoplayer = tk.Label(self.root)
        self.videoplayer.pack(expand=True, fill="both")

        self.play_video(self.waiting_video)

        self.labelframe_0 = tk.LabelFrame(root, bg='pink',
            text='labelframe_0', labelanchor='n', container=True)
        self.labelframe_0.place(x=0, y=0, width=1920, height=1080)
        self.sub = tk.Toplevel(root, bg='red', use=self.labelframe_0.winfo_id()) 

        self.overlay_image = ImageTk.PhotoImage(file=self.overlay_image_path)
        self.overlay_label = tk.Label(self.sub, image=self.overlay_image, bg='green')
        self.overlay_label.place(x=0, y=0, width=1920, height=1080)

        self.label = tk.Label(root, text="起動中", font=("メイリオ", 28), bg=self.c_user_bg, fg=self.c_user_text)
        self.label.place(x=30, y=30, width=600, height=80)

        self.root.update()

        self.sub.wm_attributes('-transparentcolor', 'green')
        self.sub.wm_attributes('-alpha', 1.0)
        self.root.wm_deiconify() 

        self.thread = threading.Thread(target=self.load_video, args=(self.waiting_video, self.videoplayer, 30))
        self.thread.daemon = True
        self.thread.start()

        self.main_thread = threading.Thread(target=self.main_chat)
        self.main_thread.daemon = True
        self.main_thread.start()

    def start_chat(self):
        self.messages.append(
            {"role": "assistant", "content": self.init_message}
        )

        assistant_respose_segments = tools.split_text(self.init_message)
        gen_thread = threading.Thread(target=tts.generate_voice, args=(assistant_respose_segments,))
        gen_thread.daemon = True
        gen_thread.start()

        for i, seg in enumerate(assistant_respose_segments):
            if len(assistant_respose_segments) == 1:
                mode = "single"
            elif i == 0:
                mode = "start"
            elif i == len(assistant_respose_segments) - 1:
                mode = "end"
            else:
                mode = "middle"
            create_chat_bubble(seg, role="assistant", mode=mode)

            self.change_label("assistant", Constants.GENERATING_VOICE_TEXT)
            while True:
                if os.path.exists(f"./audio/{i}.wav"):
                    break

            if i == 0:
                self.play_video(self.starting_video)
                sleep(2.5)
            
            self.change_label("assistant", Constants.ASSISTANT_SPEAKING_TEXT)
            self.update_chat_display()
            self.play_video(self.speaking_video)
            tts.play_sound(f"./audio/{i}.wav")
            self.play_video(self.waiting_video)

    def main_chat(self):
        tools.delete_files_in_folder("./chats")
        tools.delete_files_in_folder("./audio")
        self.update_chat_display()
        self.start_chat()

        while True:
            try:
                tools.delete_files_in_folder("./audio")
                self.change_label("user", Constants.LISTENING_TEXT)
                user_input = self.stt_model.listen()

                self.change_label("assistant", Constants.GENERATING_CHAT_TEXT)
                self.messages.append(
                    {"role": "user", "content": user_input}
                )
                user_input_segments = tools.split_text(user_input)
                for i, seg in enumerate(user_input_segments):
                    if len(user_input_segments) == 1:
                        mode = "single"
                    elif i == 0:
                        mode = "start"
                    elif i == len(user_input_segments) - 1:
                        mode = "end"
                    else:
                        mode = "middle"
                    create_chat_bubble(seg, role="user", mode=mode)
                
                self.update_chat_display()
                assistant_respose, reset = chat.run_completion(self.messages)
                self.messages.append(
                    {"role": "assistant", "content": assistant_respose}
                )

                # Customize image display
                if "クリーンマスター" in assistant_respose:
                    overlay_image = "./images/cleanmaster.png"
                elif "エアロブック" in assistant_respose:
                    overlay_image = "./images/aerobook.png"
                else:
                    overlay_image = None

                assistant_respose_segments = tools.split_text(assistant_respose)
                gen_thread = threading.Thread(target=tts.generate_voice, args=(assistant_respose_segments,))
                gen_thread.daemon = True
                gen_thread.start()

                for i, seg in enumerate(assistant_respose_segments):
                    if i == 0:
                        mode = "start"
                    elif i == len(assistant_respose_segments) - 1:
                        mode = "end"
                    else:
                        mode = "middle"
                    create_chat_bubble(seg, role="assistant", mode=mode)

                    self.change_label("assistant", Constants.GENERATING_VOICE_TEXT)
                    while True:
                        if os.path.exists(f"./audio/{i}.wav"):
                            break

                    self.change_label("assistant", Constants.ASSISTANT_SPEAKING_TEXT)
                    self.update_chat_display(overlay_image=overlay_image)
                    self.play_video(self.speaking_video)
                    tts.play_sound(f"./audio/{i}.wav")
                    self.play_video(self.waiting_video)

                if reset:
                    tools.delete_files_in_folder("./chats")
                    tools.delete_files_in_folder("./audio")
                    self.messages = [
                        {"role": "system", "content": self.system_prompt}
                    ]
                    self.update_chat_display()
                    self.start_chat()
            
            except Exception as e:
                print(e)


    def update_chat_display(self, overlay_image=None):
        create_vertical_image("./chats", overlay_image=overlay_image)
        new_image = Image.open(Constants.CONCAT_CHAT_IMAGE)
        new_photo = ImageTk.PhotoImage(new_image)
        self.overlay_label.config(image=new_photo)
        self.overlay_label.image = new_photo

    def change_label(self, mode="assistant", text=""):
        if mode == "assistant":
            self.label.config(text=text, bg=self.c_assistant_bg, fg=self.c_assistant_text)
        else:
            self.label.config(text=text, bg=self.c_user_bg, fg=self.c_user_text)

    def load_video(self, path, label, hz):
        global finished
        frame_data = imageio.get_reader(path)
        if hz > 0:
            frame_duration = float(1 / hz)
        else:
            frame_duration = float(0)

        while not finished:
            before = perf_counter()
            for image in frame_data.iter_data():
                if not finished:
                    frame_image = ImageTk.PhotoImage(Image.fromarray(image).resize((1920,1080)))
                    label.config(image=frame_image)
                    label.image = frame_image
                    diff = frame_duration + before
                    after = perf_counter()
                    diff = diff - after 
                    if diff > 0:
                        sleep(diff)
                    before = perf_counter()
                
                else:
                    finished = True
                    break
        finished = False

    def play_video(self, video_path):
        self.stop_video()
        self.thread = threading.Thread(target=self.load_video, args=(video_path, self.videoplayer, 30))
        self.thread.daemon = True
        self.thread.start()

    def stop_video(self):
        global finished
        finished = True


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1920x1080') 
    root.configure(bg='blue')
    root.resizable(False, False)
    root.title("EZ Avatar Chatbot")

    app = EZVideoChatBotApp(root)
    root.mainloop()
