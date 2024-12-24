import pyaudio
import webrtcvad
import wave, os
from ai.gpt.request import transcribe

class AudioVAD:
    def __init__(self, aggressiveness=3):
        self.vad = webrtcvad.Vad(aggressiveness)  # VAD aggressiveness (0-3)
        self.chunk_size = 320  # 20ms at 16kHz
        self.rate = 16000  # Sampling rate (16kHz)
        self.channels = 1  # Mono audio
        self.format = pyaudio.paInt16  # 16-bit audio format
        self.talking = False
        self.silence_time = 0
        self.audio_file_path = os.environ.get("SOURCE_AUDIO_PATH")

    def start(self):
        """Start the live voice activity detection."""
        p = pyaudio.PyAudio()

        # Open the PyAudio stream
        stream = p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        # Prepare WAV file for recording
        wf = wave.open(self.audio_file_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.format))
        wf.setframerate(self.rate)

        print("Listening for voice activity...")
        self.talking = True

        try:
            while self.talking:
                audio_data = stream.read(self.chunk_size, exception_on_overflow=False)

                # Write audio data to WAV file
                wf.writeframes(audio_data)

                # Pass audio data to WebRTC VAD
                is_speech = self.vad.is_speech(audio_data, self.rate)

                if is_speech:
                    print("Speech detected.")
                    self.silence_time = 0
                else:
                    print("Silence detected.")
                    self.silence_time += 0.02
                
                if self.silence_time > 1:
                    print("Stopping the function due to prolonged silence.")
                    self.talking = False

        except KeyboardInterrupt:
            print("Stopping live audio...")
        finally:
            # Cleanup
            wf.close()
            stream.stop_stream()
            stream.close()
            p.terminate()
            self.processAudio()

    def stop(self):
        """Stop the live detection."""
        self.talking = False

    def processAudio(self):
        """Send the recorded audio file to OpenAI Whisper for transcription."""
        try:
            text = transcribe(self.audio_file_path)
            print(text)
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None
