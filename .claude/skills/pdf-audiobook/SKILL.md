---
name: PDF Audiobook Generator
description: Convert textbook PDFs to audiobooks with AI-generated image descriptions and smart text processing. Use when converting PDFs to audio, creating audiobooks from textbooks, or processing academic PDFs with images. Handles figures, citations, and indices intelligently.
---

# PDF Audiobook Generator

**A Claude Code skill that converts textbooks and PDFs into audiobooks with intelligent image analysis.**

⚠️ **Claude Code Only**: This skill is designed exclusively for use within Claude Code. I analyze images directly during our conversation - no separate API calls needed!

## Features

- **AI Image Descriptions**: I analyze figures, diagrams, and images using my vision capabilities
- **Smart Citations**: Automatically summarizes bibliographies, references, and indices
- **Voice Selection**: Choose from 8 voices when generating audio
- **Flexible Processing**: Full documents, specific chapters, or custom page ranges
- **Editable Scripts**: Review and edit before audio generation
- **Free TTS**: Local text-to-speech using Piper (no per-character fees)
- **Page/Figure References**: Includes context like page numbers and figure labels

## Quick Start

1. **First time setup**:
   ```bash
   cd .claude/skills/pdf-audiobook
   pip3 install -r requirements.txt
   ```

2. **Install FFmpeg** (required):
   ```bash
   brew install ffmpeg  # macOS
   sudo apt install ffmpeg  # Linux
   ```

3. **Start a conversation**:
   - "Convert this PDF to an audiobook: /path/to/file.pdf"
   - "Create an audiobook from chapter 3"
   - "Process pages 10-25 as audio"

## How It Works

### Interactive Steps (Fast - I assist)
1. **Extraction**: I extract text and identify images from your PDF
2. **Image Analysis**: I analyze images directly and generate descriptions
3. **Script Creation**: I create an editable text script with descriptions inserted
4. **Review**: You can review/edit the script

### Standalone Step (Slow - Run independently)
5. **Audio Generation**: You run a script to generate MP3 (takes hours, free)

This approach means **zero API costs** - everything runs in our conversation or locally on your machine.

## Processing Options

### Full Document
```bash
python3 scripts/process_chapter.py document.pdf --full output/scripts/full.txt
```

### Specific Chapter
```bash
# Requires PDF with table of contents
python3 scripts/process_chapter.py textbook.pdf 3 output/scripts/chapter_03.txt
```

### Page Range
```bash
python3 scripts/process_chapter.py document.pdf --pages 10-25 output/scripts/section.txt
```

## Voice Options

When generating audio, you'll choose from 8 voices:

1. **en_US-ryan-high** - Clear, natural male voice ⭐ (recommended)
2. **en_US-kathleen-low** - Warm female voice
3. **en_US-amy-medium** - Clear female voice
4. **en_US-lessac-medium** - Neutral/professional
5. **en_US-danny-low** - Expressive male voice
6. **en_US-libritts-high** - Highest quality (slower)
7. **en_GB-alan-medium** - British male
8. **en_GB-alba-medium** - British female

The default was chosen based on feedback that the original was too bland.

## Cost

- **Image Analysis**: $0 (I do this in Claude Code)
- **Audio Generation**: $0 (runs locally)
- **Total**: $0

## Output Structure

```
output/
├── scripts/
│   ├── full_doc.txt           # Editable text script
│   ├── full_doc_images/       # Extracted images
│   └── ...
└── audio/
    ├── audiobook.mp3          # Final audio file
    └── ...
```

## Requirements

Dependencies (in `requirements.txt`):
- `PyMuPDF` - PDF extraction
- `piper-tts` - Text-to-speech
- `pyyaml` - Configuration
- `pillow` - Image processing
- `pydub` - Audio processing

System requirements:
- Python 3.8+
- FFmpeg

## Troubleshooting

**Piper installation**: If `pip3 install -r requirements.txt` fails, try `pip3 install --upgrade piper-tts`

**FFmpeg missing**: Install via your package manager (brew/apt)

**Audio is slow**: Normal! 1 hour of audio takes 1-2 hours to generate. Run overnight.

**Python command errors**: Use `python3` not `python` on macOS/Linux

## Tips

1. Start with one chapter to learn the workflow
2. Review scripts carefully before audio generation
3. Try different voices to find what works best
4. Keep original PDFs until satisfied with results
5. Backup generated scripts - they're valuable after image analysis

## Next Steps

After your first conversion, you can:
- Batch process multiple chapters
- Customize voice settings in `config.yaml`
- Adjust text processing rules (what to summarize)

See [WORKFLOW.md](WORKFLOW.md) and [EXAMPLES.md](EXAMPLES.md) for more details.

---

**Powered by Claude Code & Piper TTS**
