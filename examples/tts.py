from transformers import pipeline

# Load the text-to-speech pipeline
tts = pipeline("text-to-speech", model="coqui/XTTS-v2")

# Input text to be converted to speech
text = "Hello, this is a demonstration of the Coqui XTTS-v2 model."

# Generate speech audio
speech = tts(text)

# Save the audio to a file
with open("output_audio.wav", "wb") as f:
    f.write(speech["audio"])
print("Audio saved to output_audio.wav")
