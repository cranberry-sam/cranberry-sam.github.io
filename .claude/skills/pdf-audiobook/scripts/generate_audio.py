#!/usr/bin/env python3
"""
Generate audio from a text script using Piper TTS.

This is a STANDALONE script that runs independently (not during Claude Code conversation).
It processes the entire text script and generates an MP3 audiobook file.

Usage:
    python generate_audio.py <script_file> <output_audio>

Example:
    python generate_audio.py output/scripts/chapter_03.txt output/audio/chapter_03.mp3

Requirements:
    - piper-tts must be installed
    - A Piper voice model must be downloaded
"""

import sys
import subprocess
import re
from pathlib import Path
import yaml
import tempfile
import os


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


def check_piper_installed():
    """Check if Piper is installed and accessible."""
    try:
        result = subprocess.run(['piper', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def clean_text_for_tts(text):
    """
    Clean and prepare text for text-to-speech.

    Removes:
    - Page markers
    - Image placeholders that weren't replaced
    - Excessive whitespace
    - Special formatting that doesn't translate well to audio

    Args:
        text: Raw script text

    Returns:
        Cleaned text suitable for TTS
    """
    # Remove page markers
    text = re.sub(r'\[PAGE \d+\]', '', text)

    # Remove any remaining image placeholders (shouldn't exist if analyze_images was run)
    text = re.sub(r'\{\{IMAGE_PLACEHOLDER_\d+\}\}', '', text)

    # Remove placeholder text
    text = re.sub(r'\(Image description will be inserted here.*?\)', '', text)

    # Clean up image description markers (keep the content, remove the marker)
    text = re.sub(r'\[Image Description\]', '', text)

    # Normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 consecutive newlines
    text = re.sub(r' {2,}', ' ', text)  # Remove multiple spaces

    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    return text.strip()


def split_into_sentences(text):
    """
    Split text into sentences for processing.

    This helps with:
    - Progress tracking
    - Error recovery
    - Memory management

    Args:
        text: Cleaned text

    Returns:
        List of sentences
    """
    # Simple sentence splitting (can be improved with nltk if needed)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def generate_audio_with_piper(text, output_file, config, progress_callback=None):
    """
    Generate audio using Piper TTS.

    Args:
        text: Text to convert to speech
        output_file: Path to output audio file
        config: Configuration dictionary
        progress_callback: Optional function to call with progress updates

    Returns:
        True if successful, False otherwise
    """
    voice_model = config.get('tts', {}).get('voice_model', 'en_US-lessac-medium')
    speaking_rate = config.get('tts', {}).get('speaking_rate', 1.0)

    # Clean text
    cleaned_text = clean_text_for_tts(text)

    # Split into sentences for progress tracking
    sentences = split_into_sentences(cleaned_text)
    total_sentences = len(sentences)

    print(f"Processing {total_sentences} sentences...")

    # Create temporary directory for intermediate audio files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        audio_files = []

        # Process each sentence
        for i, sentence in enumerate(sentences, 1):
            if progress_callback:
                progress_callback(i, total_sentences)

            # Skip empty sentences
            if not sentence.strip():
                continue

            # Generate audio for this sentence
            sentence_audio = temp_path / f"sentence_{i:05d}.wav"

            try:
                # Run Piper
                process = subprocess.Popen(
                    ['piper', '--model', voice_model, '--output_file', str(sentence_audio)],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                stdout, stderr = process.communicate(input=sentence)

                if process.returncode != 0:
                    print(f"\nWarning: Error processing sentence {i}: {stderr}")
                    continue

                audio_files.append(sentence_audio)

            except Exception as e:
                print(f"\nWarning: Error processing sentence {i}: {e}")
                continue

        # Concatenate all audio files
        print("\nConcatenating audio files...")

        # Create a file list for ffmpeg
        file_list_path = temp_path / "file_list.txt"
        with open(file_list_path, 'w') as f:
            for audio_file in audio_files:
                f.write(f"file '{audio_file}'\n")

        # Use ffmpeg to concatenate and convert to MP3
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            subprocess.run([
                'ffmpeg', '-f', 'concat', '-safe', '0',
                '-i', str(file_list_path),
                '-c:a', 'libmp3lame', '-b:a', '128k',
                str(output_path)
            ], check=True, capture_output=True)

            return True

        except subprocess.CalledProcessError as e:
            print(f"\nError: Failed to concatenate audio files: {e}")
            print("Make sure ffmpeg is installed.")
            return False

        except FileNotFoundError:
            print("\nError: ffmpeg not found.")
            print("Please install ffmpeg to generate MP3 files.")
            return False


def estimate_duration(text):
    """
    Estimate audio duration based on text length.

    Average speaking rate: ~150 words per minute

    Args:
        text: Text to estimate

    Returns:
        Estimated duration in minutes
    """
    word_count = len(text.split())
    duration_minutes = word_count / 150
    return duration_minutes


def progress_callback(current, total):
    """Display progress bar."""
    percentage = (current / total) * 100
    bar_length = 40
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    print(f'\rProgress: |{bar}| {percentage:.1f}% ({current}/{total} sentences)', end='', flush=True)


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_audio.py <script_file> <output_audio>")
        print("Example: python generate_audio.py output/scripts/chapter_03.txt output/audio/chapter_03.mp3")
        sys.exit(1)

    script_file = sys.argv[1]
    output_audio = sys.argv[2]

    # Validate script file
    script_path = Path(script_file)
    if not script_path.exists():
        print(f"Error: Script file not found: {script_file}")
        sys.exit(1)

    # Check Piper installation
    if not check_piper_installed():
        print("Error: Piper TTS is not installed or not in PATH.")
        print("\nTo install Piper:")
        print("  pip install piper-tts")
        print("\nSee: https://github.com/rhasspy/piper")
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
    print(f"Estimated processing time: {estimated_minutes * 1.5:.1f} minutes")
    print()

    # Check for remaining image placeholders
    remaining_placeholders = len(re.findall(r'\{\{IMAGE_PLACEHOLDER_\d+\}\}', script_text))
    if remaining_placeholders > 0:
        print(f"Warning: Found {remaining_placeholders} image placeholders that haven't been analyzed.")
        print("Run analyze_images.py first for better results.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            sys.exit(0)

    # Generate audio
    print("\nGenerating audio...")
    success = generate_audio_with_piper(script_text, output_audio, config, progress_callback)

    if success:
        output_size = Path(output_audio).stat().st_size / (1024 * 1024)  # MB
        print("\n" + "=" * 60)
        print(f"Success! Audio file created: {output_audio}")
        print(f"File size: {output_size:.1f} MB")
        print("\nYour audiobook chapter is ready!")
    else:
        print("\nFailed to generate audio.")
        sys.exit(1)


if __name__ == "__main__":
    main()
