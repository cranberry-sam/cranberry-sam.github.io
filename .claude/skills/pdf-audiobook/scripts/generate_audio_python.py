#!/usr/bin/env python3
"""
Generate audio from a text script using Piper TTS Python API.

Usage:
    python generate_audio_python.py <script_file> <output_audio>
"""

import sys
import re
from pathlib import Path
import yaml
import wave
import subprocess
from piper import PiperVoice


def load_config():
    """Load configuration from config.yaml."""
    config_path = Path(__file__).parent.parent / "config.yaml"

    if not config_path.exists():
        print("Warning: config.yaml not found. Using defaults.")
        return {
            'tts': {
                'speaking_rate': 1.0,
                'voice_model': 'en_US-lessac-medium',
                'audio_quality': 'high',
                'output_format': 'mp3'
            }
        }

    with open(config_path) as f:
        return yaml.safe_load(f)


def clean_text_for_tts(text):
    """Clean and prepare text for text-to-speech."""
    # Remove page markers
    text = re.sub(r'\[PAGE \d+\]', '', text)

    # Remove any remaining image placeholders
    text = re.sub(r'\{\{IMAGE_PLACEHOLDER_\d+\}\}', '', text)

    # Remove placeholder text
    text = re.sub(r'\(Image description will be inserted here.*?\)', '', text)

    # Clean up image description markers
    text = re.sub(r'\[Image \d+ on page \d+\]', '', text)
    text = re.sub(r'\[Figure .* on page \d+\]', '', text)

    # Normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)

    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    return text.strip()


def download_voice_model(model_name):
    """Download a Piper voice model if not already present."""
    import urllib.request
    import json

    # Piper voices are hosted on Hugging Face
    base_url = "https://huggingface.co/rhasspy/piper-voices/resolve/main"

    # Map model names to paths
    model_paths = {
        'en_US-lessac-medium': 'en/en_US/lessac/medium/en_US-lessac-medium',
        'en_GB-alan-medium': 'en/en_GB/alan/medium/en_GB-alan-medium',
        'en_US-libritts-high': 'en/en_US/libritts/high/en_US-libritts-high',
    }

    if model_name not in model_paths:
        print(f"Warning: Unknown model {model_name}, using default")
        model_name = 'en_US-lessac-medium'

    model_path = model_paths[model_name]

    # Create models directory
    models_dir = Path.home() / '.local' / 'share' / 'piper' / 'voices'
    models_dir.mkdir(parents=True, exist_ok=True)

    onnx_file = models_dir / f"{model_name}.onnx"
    json_file = models_dir / f"{model_name}.onnx.json"

    # Download if not present
    if not onnx_file.exists():
        print(f"Downloading voice model {model_name}...")
        print("This may take a few minutes on first run...")

        onnx_url = f"{base_url}/{model_path}.onnx"
        json_url = f"{base_url}/{model_path}.onnx.json"

        try:
            print(f"  Downloading {onnx_file.name}...")
            urllib.request.urlretrieve(onnx_url, onnx_file)
            print(f"  Downloading {json_file.name}...")
            urllib.request.urlretrieve(json_url, json_file)
            print("  Download complete!")
        except Exception as e:
            print(f"Error downloading model: {e}")
            return None

    return str(onnx_file)


def select_voice():
    """Prompt user to select a voice model."""
    voices = {
        '1': ('en_US-ryan-high', 'US English, male, clear and natural (recommended)'),
        '2': ('en_US-kathleen-low', 'US English, female, warm'),
        '3': ('en_US-amy-medium', 'US English, female, clear'),
        '4': ('en_US-lessac-medium', 'US English, neutral/professional'),
        '5': ('en_US-danny-low', 'US English, male, expressive'),
        '6': ('en_US-libritts-high', 'US English, high quality (slower generation)'),
        '7': ('en_GB-alan-medium', 'British English, male'),
        '8': ('en_GB-alba-medium', 'British English, female'),
    }

    print("\nAvailable voices:")
    for key, (model, desc) in voices.items():
        print(f"  {key}. {desc}")

    while True:
        choice = input("\nSelect voice (1-8, or press Enter for default): ").strip()

        if not choice:
            # Default to ryan-high (recommended)
            return 'en_US-ryan-high'

        if choice in voices:
            return voices[choice][0]

        print("Invalid choice. Please enter a number 1-8.")


def generate_audio_with_piper(text, output_file, config, voice_override=None):
    """Generate audio using Piper TTS Python API."""

    voice_model_name = voice_override or config.get('tts', {}).get('voice_model', 'en_US-ryan-high')

    # Download/locate voice model
    voice_model_path = download_voice_model(voice_model_name)
    if not voice_model_path:
        return False

    print(f"Using voice model: {voice_model_name}")

    # Clean text
    cleaned_text = clean_text_for_tts(text)

    # Load voice
    print("Loading voice model...")
    voice = PiperVoice.load(voice_model_path)

    # Create temporary WAV file
    temp_wav = Path(output_file).parent / "temp_audio.wav"
    temp_wav.parent.mkdir(parents=True, exist_ok=True)

    print("Synthesizing speech...")

    # Generate audio chunks
    audio_chunks = []
    total_chars = len(cleaned_text)
    chars_processed = 0

    # Process in paragraphs for better progress tracking
    paragraphs = [p.strip() for p in cleaned_text.split('\n\n') if p.strip()]

    for i, paragraph in enumerate(paragraphs, 1):
        print(f"\rProgress: {i}/{len(paragraphs)} paragraphs ({(i/len(paragraphs)*100):.1f}%)", end='', flush=True)

        # Synthesize this paragraph
        for audio_chunk in voice.synthesize(paragraph):
            audio_chunks.append(audio_chunk)

    print()  # New line after progress

    # Combine all audio chunks and save to WAV
    print("Writing audio file...")
    with wave.open(str(temp_wav), 'wb') as wav_file:
        wav_file.setframerate(voice.config.sample_rate)
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setnchannels(1)  # Mono

        for chunk in audio_chunks:
            wav_file.writeframes(chunk)

    # Convert to MP3 using ffmpeg
    print("Converting to MP3...")
    output_path = Path(output_file)

    try:
        subprocess.run([
            'ffmpeg', '-y', '-i', str(temp_wav),
            '-c:a', 'libmp3lame', '-b:a', '128k',
            str(output_path)
        ], check=True, capture_output=True)

        # Clean up temp file
        temp_wav.unlink()

        return True

    except subprocess.CalledProcessError as e:
        print(f"\nError: Failed to convert to MP3: {e}")
        return False


def estimate_duration(text):
    """Estimate audio duration based on text length (150 words per minute)."""
    word_count = len(text.split())
    duration_minutes = word_count / 150
    return duration_minutes


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_audio_python.py <script_file> <output_audio>")
        sys.exit(1)

    script_file = sys.argv[1]
    output_audio = sys.argv[2]

    # Validate script file
    script_path = Path(script_file)
    if not script_path.exists():
        print(f"Error: Script file not found: {script_file}")
        sys.exit(1)

    # Load config
    config = load_config()

    print(f"Generating audio for: {script_file}")
    print(f"Output: {output_audio}")
    print("=" * 60)

    # Load script
    with open(script_path, 'r', encoding='utf-8') as f:
        script_text = f.read()

    # Estimate duration
    estimated_minutes = estimate_duration(script_text)
    print(f"Estimated audio duration: {estimated_minutes:.1f} minutes")
    print()

    # Select voice
    selected_voice = select_voice()
    print(f"\nUsing voice: {selected_voice}")
    print()

    # Generate audio
    success = generate_audio_with_piper(script_text, output_audio, config, voice_override=selected_voice)

    if success:
        output_size = Path(output_audio).stat().st_size / (1024 * 1024)  # MB
        print("\n" + "=" * 60)
        print(f"Success! Audio file created: {output_audio}")
        print(f"File size: {output_size:.1f} MB")
        print(f"Estimated duration: {estimated_minutes:.1f} minutes")
    else:
        print("\nFailed to generate audio.")
        sys.exit(1)


if __name__ == "__main__":
    main()
