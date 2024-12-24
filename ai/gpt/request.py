from ai.gpt.config import client, model

def chat(messages: list[dict]):
    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )
    
    return completion.choices[0].message


def transcribe(audio_file: str):
    audio_file = open(audio_file, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

    return transcription.text