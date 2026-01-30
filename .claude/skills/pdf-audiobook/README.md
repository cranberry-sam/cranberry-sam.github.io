# PDF Audiobook Generator

**A Claude Code skill for converting textbook PDFs into audiobooks with AI-generated image descriptions.**

⚠️ **This skill is designed exclusively for Claude Code.** Claude analyzes images directly during your conversation - no separate API calls needed!

## Features

- **AI Image Descriptions**: Claude analyzes figures, diagrams, and images using vision capabilities
- **Smart Citations**: Summarizes bibliographies, references, and indices instead of reading them verbatim
- **Voice Selection**: Choose from 8 different voices (male/female, US/British accents)
- **Editable Scripts**: Review and edit the generated text before audio conversion
- **Flexible Processing**: Handle full documents, specific chapters, or custom page ranges
- **Free TTS**: Uses Piper for high-quality, local text-to-speech (no per-character fees)
- **Page/Figure References**: Includes page numbers and figure labels in audio descriptions

## Quick Start

1. **First time setup**:
   ```bash
   cd .claude/skills/pdf-audiobook
   pip3 install -r requirements.txt
   ```

2. **Install FFmpeg** (required for MP3 conversion):
   ```bash
   # macOS
   brew install ffmpeg

   # Linux
   sudo apt install ffmpeg
   ```

3. **Start a conversation with Claude Code**:
   - "Convert this PDF to an audiobook: /path/to/textbook.pdf"
   - "Create an audiobook from chapter 3 of my textbook"
   - "Process pages 10-25 of this PDF as audio"

## How It Works

### Claude Code Interactive Steps (Fast)
1. **Text Extraction**: Claude extracts text and identifies images from your PDF
2. **Image Analysis**: Claude analyzes images directly and generates descriptions
3. **Script Generation**: Claude creates an editable text script with image descriptions inserted
4. **Review**: You can review/edit the script before audio generation

### Audio Generation (Slow - Run Independently)
5. **Voice Selection**: Choose your preferred voice from 8 options
6. **Audio Generation**: Run the script to generate MP3 (takes time, completely free)

This hybrid approach means **zero API costs** and fast processing for everything except audio generation (which runs locally on your machine).

## Workflow

### Process Full Document
```bash
# 1. Extract and process (Claude guides you through this)
python3 scripts/process_chapter.py document.pdf --full output/scripts/full_doc.txt

# 2. Claude analyzes images and updates the script automatically

# 3. Generate audio (you run this, takes several hours)
python3 scripts/generate_audio_python.py output/scripts/full_doc.txt output/audio/audiobook.mp3
```

### Process Specific Chapter
```bash
# Requires PDF with table of contents
python3 scripts/process_chapter.py textbook.pdf 3 output/scripts/chapter_03.txt
```

### Process Page Range
```bash
# Process pages 10-25
python3 scripts/process_chapter.py document.pdf --pages 10-25 output/scripts/section.txt
```

## Voice Options

When generating audio, you'll be prompted to select a voice:

1. **en_US-ryan-high** - US male, clear and natural ⭐ (recommended)
2. **en_US-kathleen-low** - US female, warm
3. **en_US-amy-medium** - US female, clear
4. **en_US-lessac-medium** - US neutral/professional
5. **en_US-danny-low** - US male, expressive
6. **en_US-libritts-high** - US high quality (slower generation)
7. **en_GB-alan-medium** - British male
8. **en_GB-alba-medium** - British female

The default (`en_US-ryan-high`) was chosen based on user feedback that the original default was too bland.

You can also set a default voice in `config.yaml`.

## Output Structure

```
output/
├── scripts/
│   ├── chapter_01.txt         # Editable text scripts
│   ├── chapter_01_images/     # Extracted images
│   └── ...
└── audio/
    ├── chapter_01.mp3         # Final audio files
    └── ...
```

## Configuration

Edit `config.yaml` to customize:
- Default voice and speaking rate
- Text processing rules (what to summarize)
- Audio quality settings
- Output directories

See `config.yaml.template` for all options.

## Cost

- **Claude Analysis**: $0 (runs in Claude Code)
- **TTS Generation**: $0 (runs locally using Piper)
- **Total**: $0

## Troubleshooting

### Piper installation issues
If Piper doesn't install correctly:
```bash
pip3 install --upgrade piper-tts
```

See the [Piper documentation](https://github.com/rhasspy/piper) for platform-specific help.

### FFmpeg required
Audio generation requires FFmpeg for MP3 conversion:
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Audio generation is slow
This is normal! Generating 1 hour of audio can take 1-2 hours depending on your CPU. The voice model affects speed:
- Fastest: `danny-low`, `kathleen-low`
- Medium: `ryan-high`, `amy-medium`, `lessac-medium`
- Slowest: `libritts-high` (highest quality)

Run audio generation in the background or overnight.

### Python command issues
Always use `python3` on macOS/Linux:
```bash
python3 scripts/process_chapter.py ...  # ✅ Correct
python scripts/process_chapter.py ...   # ❌ May fail
```

## Requirements

All dependencies in `requirements.txt`:
- `PyMuPDF` - PDF text/image extraction
- `piper-tts` - Local text-to-speech engine
- `pyyaml` - Configuration
- `pillow` - Image processing
- `pydub` - Audio processing

System requirements:
- Python 3.8+
- FFmpeg

## Examples

See [EXAMPLES.md](EXAMPLES.md) for detailed usage examples.

## Advanced Usage

See [WORKFLOW.md](WORKFLOW.md) for step-by-step instructions and advanced options.

## Legal Notice

This tool is designed for creating accessible audiobooks from **legally obtained** textbooks for personal use. Ensure you have the right to use the source material.

## Tips for Best Results

1. **Start with one chapter** to get familiar with the workflow
2. **Review scripts carefully** before generating audio (especially image descriptions)
3. **Try different voices** to find what works best for your content
4. **Keep original PDFs** until you're satisfied with results
5. **Backup generated scripts** - they're valuable after Claude has analyzed the images

## Questions?

Just ask Claude Code! The skill is designed to help you through the entire process.

Example questions:
- "How do I process just chapter 5?"
- "Can I make the voice faster?"
- "How long will this take to generate?"
- "What voice sounds best for a medical textbook?"

---

**Created for Claude Code** | **Powered by Anthropic Claude & Piper TTS**
