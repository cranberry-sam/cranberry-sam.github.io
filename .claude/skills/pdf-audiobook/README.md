# PDF Audiobook Generator - Claude Code Skill

A Claude Code Skill that converts textbook PDFs into high-quality audiobooks with AI-generated image descriptions.

## Overview

This skill helps you create audiobooks from legally obtained textbooks by:

- **Extracting text** chapter-by-chapter from PDFs
- **Analyzing images** with Claude's vision AI to generate natural language descriptions
- **Handling special content** like citations, bibliographies, and indices intelligently
- **Generating audio** using free, local text-to-speech (Piper TTS)
- **Including context** like page numbers and figure labels in descriptions

## Features

### Intelligent Image Handling
- AI-generated descriptions of figures, diagrams, and images
- Automatic detection of figure labels (e.g., "Figure 3.2")
- Page number references in audio
- Customizable description styles (concise, detailed, very detailed)

### Smart Text Processing
- Auto-summarizes citations, bibliographies, and indices
- Handles tables appropriately
- Removes content that doesn't translate well to audio

### Cost-Effective
- Free local TTS (Piper) - no per-character fees
- Minimal AI costs (~$2-4 per chapter for image analysis)
- Typical 500-page textbook: $10-20 total

### Hybrid Workflow
- **Fast operations** run interactively with Claude's help
- **Slow operations** run standalone (no token costs during processing)
- Review and edit scripts before generating audio

## Quick Start

### 1. Install Dependencies

```bash
cd .claude/skills/pdf-audiobook
pip install -r requirements.txt
```

Install system dependencies:
- **Piper TTS**: `pip install piper-tts`
- **FFmpeg**: Install via your system package manager

### 2. Configure API Key

```bash
cp config.yaml.template config.yaml
# Edit config.yaml and add your Anthropic API key
```

### 3. Start Using the Skill

Just chat with Claude Code:

```
You: I want to convert my biology textbook to an audiobook

Claude: Great! I can help with that. What's the path to your PDF?

You: ~/Documents/bio_textbook.pdf

Claude: [Extracts chapters and guides you through the process]
```

## How It Works

### The Hybrid Approach

**Interactive Steps (Claude assists)**:
1. Extract chapter list from PDF (seconds)
2. Process chapter text and images (seconds)
3. Review and edit generated scripts (your pace)

**Standalone Steps (run independently)**:
4. Analyze images with AI (5-10 minutes per chapter)
5. Generate MP3 audio (2-3 hours per chapter)

This design ensures **zero token costs** during long operations while still providing AI assistance where it's valuable.

## Typical Workflow

### First Chapter

```
You: Convert chapter 3 of my textbook to audio

Claude: [Runs extraction and processing - fast]
        Found 7 images in chapter 3.

        To analyze them with AI:

        python .claude/skills/pdf-audiobook/scripts/analyze_images.py \
          output/scripts/chapter_03.txt \
          output/scripts/chapter_03_images/

        Run this and let me know when it's done!

[You run the command, wait 5 minutes]

You: Image analysis is done

Claude: [Shows you the script preview]
        Here's the generated script. Want to review or edit anything?

You: Looks good!

Claude: To generate audio:

        python .claude/skills/pdf-audiobook/scripts/generate_audio.py \
          output/scripts/chapter_03.txt \
          output/audio/chapter_03.mp3

        This will take about 2 hours. Run it in the background!

[You run it overnight]

You: Chapter 3 is ready! Let's do chapter 4.

Claude: [Process continues...]
```

### Batch Processing

Once you're comfortable, batch process multiple chapters:

```bash
for i in {1..12}; do
  python scripts/process_chapter.py textbook.pdf $i output/scripts/chapter_$(printf "%02d" $i).txt
  python scripts/analyze_images.py output/scripts/chapter_$(printf "%02d" $i).txt output/scripts/chapter_$(printf "%02d" $i)_images/
  python scripts/generate_audio.py output/scripts/chapter_$(printf "%02d" $i).txt output/audio/chapter_$(printf "%02d" $i).mp3
done
```

## Documentation

- **[SKILL.md](SKILL.md)**: Main skill definition and overview
- **[WORKFLOW.md](WORKFLOW.md)**: Detailed step-by-step guide
- **[EXAMPLES.md](EXAMPLES.md)**: Real conversation examples
- **[scripts/README.md](scripts/README.md)**: Technical documentation for each script

## Configuration

Edit `config.yaml` to customize:

### Voice Settings
- Speaking rate (0.5 to 2.0, default: 1.0)
- Voice model (different accents/languages)
- Audio quality (low, medium, high)

### Text Processing
- Which sections to summarize
- How to handle tables
- Citation length thresholds

### Image Analysis
- Description style (concise, detailed, very_detailed)
- Technical detail level
- Claude model to use

## Cost Breakdown

### Per Chapter (typical 30-page chapter)
- Image analysis (8 images): ~$2-4
- Audio generation: $0 (free, local)
- **Total**: ~$2-4 per chapter

### Full Textbook (500 pages, 15 chapters, 100 images)
- Image analysis: ~$25-50
- Audio generation: $0
- **Total**: ~$25-50 for entire book

Compare to commercial audiobook production: $2000-5000+ per book!

## Output

```
output/
├── scripts/
│   ├── chapter_01.txt      # Editable text scripts
│   ├── chapter_02.txt
│   ├── chapter_03.txt
│   └── ...
├── audio/
│   ├── chapter_01.mp3      # Final audiobook files
│   ├── chapter_02.mp3
│   ├── chapter_03.mp3
│   └── ...
└── images/
    ├── chapter_01_images/  # Extracted images
    ├── chapter_02_images/
    └── ...
```

## Requirements

### Python Packages
- PyMuPDF (fitz) - PDF processing
- anthropic - Claude API
- piper-tts - Text-to-speech
- Pillow - Image processing
- PyYAML - Configuration

### System Tools
- Python 3.8+
- FFmpeg (for audio processing)
- Internet connection (for image analysis only)

## Troubleshooting

### Piper Installation Issues
Piper can be tricky to install. If you have problems:
1. Try: `pip install piper-tts`
2. Check: https://github.com/rhasspy/piper
3. Ask Claude for help!

### API Key Errors
Make sure `config.yaml` exists with a valid `ANTHROPIC_API_KEY`.

### Audio Generation is Slow
This is normal! High-quality TTS takes time. Run overnight or during work.

### Chapter Not Found
Run `extract_chapters.py` first to see available chapters.

## Tips for Best Results

1. **Start with one chapter** to get familiar with the workflow
2. **Review scripts carefully** before generating audio
3. **Customize voice settings** early on
4. **Keep original PDFs** until you're satisfied with results
5. **Backup generated scripts** - they're valuable after editing

## Limitations

- Works best with standard textbook PDFs (not scanned images)
- Image descriptions are AI-generated (may need human review)
- Audio generation takes time (1-3 hours per chapter)
- Requires internet connection for image analysis

## Legal Notice

This tool is designed for creating accessible audiobooks from **legally obtained** textbooks for personal use. Ensure you have the right to use the source material.

## Contributing

This is a Claude Code Skill. To modify:
1. Edit files in `.claude/skills/pdf-audiobook/`
2. Test with Claude Code
3. Share improvements with the community!

## License

This skill is open source and free to use. The underlying technologies (Piper, PyMuPDF, Claude API) have their own licenses.

## Questions?

Just ask Claude Code! The skill is designed to help you through the entire process.

Example questions:
- "How do I process chapter 5?"
- "The image analysis failed, what do I do?"
- "Can I speed up the voice?"
- "How much will it cost to process my entire book?"

---

**Created for Claude Code** | **Powered by Anthropic Claude & Piper TTS**
