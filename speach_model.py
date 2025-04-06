import io
import wave
import json
from vosk import Model, KaldiRecognizer
from pyAudioAnalysis import audioSegmentation as aS
from pydub import AudioSegment
from db_manager.config import settings


model_path = settings.MODEL
model = Model(model_path)



async def process_audio(audio_file):
    print("______________________________________________________-")
    dialog : str = ' '
    try:
        speaker_id = 0
        with wave.open(io.BytesIO(audio_file), "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000]:
                print("Unsupported audio format. Please use a mono WAV file with 8kHz or 16kHz sample rate.")
                exit(1)
            recognizer = KaldiRecognizer(model, wf.getframerate())
            while True:
                data = wf.readframes(4000)  
                if len(data) == 0:
                    break  
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    speaker_id += 1
                    text = json.loads(result)["text"]
                    print(f"Speaker{speaker_id}", text)
                    dialog = dialog + text + "\n"
            final_result = recognizer.FinalResult()
            dialog+=json.loads(final_result)["text"]
            return dialog
    except Exception as e:
        print(f"An error occurred: {e}")


import requests

# Установите ваш API-ключ
API_KEY = settings.HUGGING_ACCSES_TOKEN
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def summarize_text(text):
    try:
        # Отправляем запрос к модели BART
        payload = {
            "inputs": text,
            "parameters": {
                "max_length": 150,  # Максимальная длина резюме
                "min_length": 30,   # Минимальная длина резюме
                "do_sample": False  # Отключаем случайную выборку
            }
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        # Извлекаем резюме из ответа
        if isinstance(result, list) and len(result) > 0:
            summary = result[0].get("summary_text", "No summary generated")
            return summary
        else:
            return "Error: Unable to generate summary."
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Пример использования
text = """
Artificial intelligence (AI) is a wonderful field of technology that focuses on creating machines capable of performing tasks that typically require human intelligence. These tasks include learning, reasoning, problem-solving, perception, and language understanding. AI has applications in various industries, such as healthcare, finance, and transportation. One of the most exciting areas of AI is machine learning, where algorithms learn from data to make predictions or decisions without being explicitly programmed.
"""

summary = summarize_text(text)
print("Summary:", summary)

# Пример использования
text = """
Artificial intelligence is a field of computer science that deals with the creation of systems, 
capable of performing tasks that require human intelligence. These tasks include learning,
reasoning, problem solving, and language perception and understanding. AI is used in various industries
such as healthcare, finance, transportation, and education. One of the most interesting areas of AI 
is machine learning, where algorithms learn from data to make decisions
"""

summary = summarize_text(text)
print("Summary:", summary)