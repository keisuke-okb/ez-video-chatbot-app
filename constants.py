class Constants:
    OPENAI_API_KEY = "YOUR_API_KEY"

    INIT_MESSAGE = "ご来店ありがとうございます。本日はどのような商品をお探しでしょうか。"
    SYSTEM_PROMPT = open("./prompt/system_prompt.txt", "r", encoding="utf-8").read()
    RESET_MESSAGE = "会話をリセットします。ご利用ありがとうございました。"
    RESET_KEYWORDS_USER = ["リセット", "会話終了", "終わって", "終わり", ]
    RESET_KEYWORDS_ASSISTANT = ["こちらこそありがとう", "またのご来店"]

    CONCAT_CHAT_IMAGE = "./images/concat.png"

    STARTING_VIDEO = "./videos/bowing.mp4"
    WAITING_VIDEO = "./videos/waiting.mp4"
    SPEAKING_VIDEO = "./videos/speaking.mp4"

    LISTENING_TEXT = "お話しください"
    ASSISTANT_SPEAKING_TEXT = "アシスタントが発話中です"
    GENERATING_CHAT_TEXT = "回答を考えています..."
    GENERATING_VOICE_TEXT = "音声合成を待機しています..."

    VOICEVOX_SPEAKER_ID = 0
    VOICEVOX_HOST = "http://localhost:50021"

    C_USER_BG = "#CEE1FF"
    C_USER_TEXT = "#004480"
    C_ASSISTANT_BG = "#452EA4"
    C_ASSISTANT_TEXT = "#ffffff"
