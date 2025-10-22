---
name: PDF Audiobook Generator
description: Convert textbook PDFs to audiobooks with AI-generated image descriptions and smart text processing. Use when converting PDFs to audio, creating audiobooks from textbooks, or processing academic PDFs with images. Handles figures, citations, and indices intelligently.
---

# PDF Audiobook Generator

Converts textbook PDFs into chapter-by-chapter audiobooks with intelligent processing:

- **AI Image Descriptions**: Automatically describes figures, diagrams, and images using Claude's vision capabilities
- **Smart Citations**: Summarizes bibliographies, references, and indices instead of reading them verbatim
- **Editable Scripts**: Review and edit the generated text before audio conversion
- **Chapter-by-Chapter**: Process books incrementally to avoid errors and manage costs
- **Free TTS**: Uses Piper for high-quality, local text-to-speech (no per-character fees)
- **Page/Figure References**: Includes page numbers and figure labels in audio descriptions

## Quick Start

1. **First time setup**:
   ```bash
   cd .claude/skills/pdf-audiobook
   pip install -r requirements.txt
   ```

2. **Configure your API key**:
   Create a `config.yaml` file with your Anthropic API key (see config.yaml.template)

3. **Start a conversation**:
   - "Convert chapter 3 of my textbook to audio"
   - "Process textbook.pdf chapter by chapter"
   - "Help me create an audiobook from this PDF"

## How It Works

### Interactive Steps (Fast - Claude assists)
1. **Chapter Selection**: I'll extract the table of contents and help you choose chapters
2. **Text Processing**: I'll process the chapter, identify images, and structure the content
3. **Script Review**: You can review and edit the generated script before audio generation

### Standalone Steps (Slow - Run independently)
4. **Image Analysis**: Run the standalone script to analyze images (takes minutes, ~$1-3 per chapter)
5. **Audio Generation**: Run the standalone script to generate MP3 (takes hours, completely free)

This hybrid approach means **zero token costs during long operations** while still giving you AI assistance where it's valuable.

## Workflow

See [WORKFLOW.md](WORKFLOW.md) for detailed step-by-step instructions.

## Examples

See [EXAMPLES.md](EXAMPLES.md) for usage examples and common scenarios.

## Cost Estimate

- **Claude API** (image analysis): ~$0.50-3 per chapter depending on image count
- **TTS Generation**: $0 (runs locally using Piper)
- **Estimated total for 500-page textbook**: $5-15

## Requirements

All dependencies listed in `requirements.txt`:
- `PyMuPDF` (fitz) - PDF text/image extraction
- `anthropic` - Claude API for image descriptions
- `piper-tts` - Local text-to-speech engine
- `pyyaml` - Configuration file handling
- `pillow` - Image processing

## Output Structure

```
output/
├── scripts/
│   ├── chapter_01.txt    # Editable text scripts
│   ├── chapter_02.txt
│   └── ...
└── audio/
    ├── chapter_01.mp3    # Final audio files
    ├── chapter_02.mp3
    └── ...
```

## Troubleshooting

**Piper installation issues**: Piper can be tricky to install. If you have issues, see the [Piper documentation](https://github.com/rhasspy/piper) or ask me for help.

**API key errors**: Make sure `config.yaml` exists with a valid `ANTHROPIC_API_KEY`.

**Audio generation is slow**: This is normal! Generating 1 hour of audio can take 1-2 hours depending on your CPU. Run it in the background or overnight.

## Next Steps

After I help you set up and generate your first chapter, you'll be able to:
- Batch process multiple chapters with a simple command
- Customize voice settings and speaking rate
- Adjust how citations and figures are handled
