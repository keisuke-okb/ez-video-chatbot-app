from whisper_mic import WhisperMic

class STTModel:
    def __init__(self):
        self.model = WhisperMic(model="small")

    def listen(self):
        result = self.model.listen()
        result = result.replace(" ", "。").replace("「", "").replace("」", "")
        if not result.endswith(("。", "!", "?", "！", "？")):
            result += "。"
        return result