# ez-video-chatbot-app
Sample app that uses videos of avatars or humans talking to create a GUI-based AI chatbot

[日本語のREADMEはこちら](README_JP.md)

![image](https://github.com/user-attachments/assets/4b137d30-c26a-4d00-a849-184e4f723893)

## Features
- By switching the videos played according to the conversation situation, this "pseudo" dialogue app can make it look like the avatar/human in the video is talking in real-time.
- Using free speech recognition libraries and free speech synthesis software, real-time conversations can be conducted.
- A high-performance GPU required for 3DCG engines is **not** necessary. While a discrete GPU like the GeForce RTX series would provide smoother operation, the app is designed to minimally function on PCs with only a CPU (with iGPU).

## Limitations
- Since Tkinter is used to rapidly redraw GUI component images to achieve video playback, the smoothness of playback varies depending on the CPU specifications.
- Local models are used for speech recognition and speech synthesis, so the response may be slower depending on the specifications of the PC running the app.
- The dialogue screen is fixed at 1920x1080. Depending on the screen scaling settings, the dialogue screen may be enlarged and overflow the display. In such cases, please change the OS display scaling setting to 100%.
- It does not support displays with less than Full HD resolution.

## Verified Environments (Laptop/Desktop)
- OS: Windows 11 24H2
- CPU: Intel Core i7-8650U, 11370H, AMD Ryzen 7 7840U, 5700X
- GPU: NVIDIA GeForce GTX 1050 Laptop GPU, RTX 3050Ti Laptop GPU, RTX 3090

### Video Playback Smoothness (Approx.)
- Intel Core i7-8650U (Laptop): Not good
- Intel Core i7-11370H (Laptop): OK
- AMD Ryzen 7 7840U (Laptop): Good
- AMD Ryzen 7 5700X (Desktop): Good

- Video playback operates smoothly on mid-range to high-end desktop CPUs such as Intel Core i7 (12th generation or later), Core 7, or equivalent Ryzen CPUs. Even with high-end CPUs, video playback may stutter on laptops.
- Using a PC with a discrete GPU will speed up speech recognition and synthesis processing. (To enable GPU support for speech recognition, you need to set up CUDA and install CUDA-compatible libraries.)

## Application Execution Steps

The following software installations are required:
- **ffmpeg**: For playing mp4 videos (Add the path where `ffmpeg.exe` is located to the environment variable `PATH`)
- **VOICEVOX**: For Japanese speech synthesis (If possible, specify the GPU for the synthesis engine in the settings)

If your PC supports CUDA, installing CUDA-compatible PyTorch from the official PyTorch website will improve performance.
[https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)

Install the necessary modules for running the application:
```sh
pip install -r requirements.txt
```

Execute the following command to launch the GUI screen:
```sh
python3 main.py
```

## Usage

After launching the screen, follow the instructions at the bottom of the screen and speak towards the audio input device. By default, it uses the OS's default input device (e.g., built-in PC microphone).
To fix the device you want to use, edit `tts.py`.

## Customization

### LLM Prompts
- `prompts/system_prompt.txt`: System prompt

### UI Settings
- `constants.py`: Specifies videos, chat background color, text color, and fixed values such as conversation end keywords.

