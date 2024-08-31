import requests

from pydub import AudioSegment
from pydub.playback import play

from constants import Constants

def play_sound(sound_path):
    audio = AudioSegment.from_wav(sound_path)
    play(audio)

def generate_voice(texts):
    for i, text in enumerate(texts):
        url = Constants.VOICEVOX_HOST + "/audio_query"
        params = {
            'text': text,
            'speaker': Constants.VOICEVOX_SPEAKER_ID
        }
        response = requests.post(url, params=params)
        query = response.text
        # query = query.replace('"pitchScale":0.0', '"pitchScale":0.02') # Customize parameters
        print(query)
        query = query.encode('utf-8')

        url = Constants.VOICEVOX_HOST + "/synthesis"
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            'speaker': Constants.VOICEVOX_SPEAKER_ID
        }
        
        response = requests.post(url, headers=headers, params=params, data=query)
        
        if response.status_code == 200:
            with open(f'./audio/{i}.wav', 'wb') as file:
                file.write(response.content)
            print("Command executed successfully.")
        else:
            print(f"Error executing command: {response.status_code}")

# generate_voice("こんにちは。")