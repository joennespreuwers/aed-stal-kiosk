import numpy as np
import sounddevice as sd

def sweep(
    start_freq: float,
    end_freq: float,
    duration: float,
    sample_rate: int
):
    t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
    k = np.log(end_freq / start_freq) / duration
    phase = (2 * np.pi * start_freq / k) * (np.exp(k * t) - 1)
    audio_data = np.sin(phase)
    audio_data = audio_data / np.max(np.abs(audio_data))

    print(f"Playing logarithmic sine sweep from {start_freq} Hz to {end_freq} Hz for {duration} seconds...")
    try:
        sd.play(audio_data, samplerate=sample_rate, blocking=True)
        print("Playback finished.")
    except Exception as e:
        print(f"Error during audio playback: {e}")
        print("Please ensure you have an audio output device configured and the 'sounddevice' library is correctly installed.")
        print("You might need to install PortAudio, which sounddevice depends on. See sounddevice documentation for details.")

if __name__ == "__main__":
    start_frequency_hz = 20.0
    end_frequency_hz = 20000.0
    sweep_duration_seconds = 3
    audio_sample_rate = 44100

    sweep(
        start_frequency_hz,
        end_frequency_hz,
        sweep_duration_seconds,
        audio_sample_rate
    )