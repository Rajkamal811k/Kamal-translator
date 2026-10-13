import os
import tempfile
import numpy as np
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import pyttsx3
from translate import Translator

# ── Setup ──────────────────────────────────────────────────────────────
translator = Translator(from_lang="en", to_lang="ta")
recognizer = sr.Recognizer()

# Initialize text-to-speech engine
engine = pyttsx3.init()
# Slow down the speech rate a bit for Tamil
engine.setProperty('rate', 130)


def record_audio(duration=5, sample_rate=16000):
    """Record audio from microphone using sounddevice."""
    print("🎤 Listening... (speak now)")
    audio_data = sd.rec(int(duration * sample_rate),
                        samplerate=sample_rate,
                        channels=1,
                        dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("✅ Recording complete!")
    return audio_data, sample_rate


def speech_to_text(audio_data, sample_rate):
    """Convert recorded audio to text using Google Speech Recognition."""
    # Save to a temporary WAV file
    temp_file = os.path.join(tempfile.gettempdir(), "voice_input.wav")
    sf.write(temp_file, audio_data, sample_rate)

    # Use SpeechRecognition to process the WAV file
    with sr.AudioFile(temp_file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en-US")
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"❌ Speech recognition service error: {e}")
        return None
    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)


def speak_text(text):
    """Speak the given text using pyttsx3."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"⚠️  Voice output error: {e}")


def main():
    print("\n╔══════════════════════════════════════════╗")
    print("║   🌐 English to Tamil Voice Translator   ║")
    print("╚══════════════════════════════════════════╝")
    print()
    print("Commands:")
    print("  [v] - Voice input (speak in English)")
    print("  [t] - Type input (type in English)")
    print("  [exit] - Quit the translator")
    print()

    while True:
        mode = input("Choose mode [v/t/exit]: ").strip().lower()

        if mode == "exit":
            print("\n👋 Translator closed! Goodbye!")
            break

        english_text = None

        if mode == "v":
            # Voice input mode
            try:
                audio_data, sample_rate = record_audio(duration=5)
                english_text = speech_to_text(audio_data, sample_rate)

                if english_text:
                    print(f"🗣️  You said: \"{english_text}\"")
                else:
                    print("❌ Could not understand the audio. Please try again.")
                    continue
            except Exception as e:
                print(f"❌ Microphone error: {e}")
                print("   Make sure your microphone is connected and try again.")
                continue

        elif mode == "t":
            # Text input mode
            english_text = input("\nEnter English text: ").strip()
            if not english_text:
                print("⚠️  Please enter some text.")
                continue

        else:
            print("⚠️  Invalid option. Please choose 'v', 't', or 'exit'.")
            continue

        # Translate
        try:
            result = translator.translate(english_text)
            print(f"\n📝 English:  {english_text}")
            print(f"🔤 Tamil:    {result}")

            # Speak the translated text
            print("🔊 Speaking translation...")
            speak_text(result)
            print()

        except Exception as e:
            print(f"❌ Translation failed: {e}\n")


if __name__ == "__main__":
    main()