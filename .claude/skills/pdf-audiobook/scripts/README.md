# PDF Audiobook Generator Scripts

This directory contains the Python scripts that power the PDF Audiobook Generator skill.

## Scripts Overview

### 1. extract_chapters.py
**Purpose**: Analyze a PDF and list all chapters with page ranges.

**Usage**:
```bash
python extract_chapters.py <pdf_path>
```

**Example**:
```bash
python extract_chapters.py ~/Documents/biology_textbook.pdf
```

**When to use**: First step when processing a new PDF. Shows you what chapters are available.

---

### 2. process_chapter.py
**Purpose**: Extract text and images from a specific chapter and create an initial script file.

**Usage**:
```bash
python process_chapter.py <pdf_path> <chapter_number> <output_script>
```

**Example**:
```bash
python process_chapter.py ~/Documents/biology_textbook.pdf 3 output/scripts/chapter_03.txt
```

**What it does**:
- Extracts all text from the chapter
- Identifies and saves all images
- Creates placeholders for image descriptions
- Identifies sections to summarize (citations, bibliography, etc.)
- Outputs a script file ready for image analysis

---

### 3. analyze_images.py (STANDALONE)
**Purpose**: Use Claude's vision API to analyze images and generate descriptions.

**Usage**:
```bash
python analyze_images.py <script_file> <image_directory>
```

**Example**:
```bash
python analyze_images.py output/scripts/chapter_03.txt output/scripts/chapter_03_images/
```

**Important**:
- This is a STANDALONE script - run it outside of Claude Code conversation
- Requires `ANTHROPIC_API_KEY` in config.yaml
- Takes several minutes depending on number of images
- Costs approximately $0.25-0.50 per image
- Updates the script file in place

**What it does**:
- Reads each image file
- Sends to Claude's vision API
- Generates natural language descriptions
- Includes figure labels and page numbers
- Replaces placeholders in the script with descriptions

---

### 4. generate_audio.py (STANDALONE)
**Purpose**: Convert the text script to MP3 audio using Piper TTS.

**Usage**:
```bash
python generate_audio.py <script_file> <output_audio>
```

**Example**:
```bash
python generate_audio.py output/scripts/chapter_03.txt output/audio/chapter_03.mp3
```

**Important**:
- This is a STANDALONE script - run it outside of Claude Code conversation
- Requires `piper-tts` and `ffmpeg` installed
- Takes 1-3 hours for a typical chapter
- Completely free (runs locally)
- Shows progress bar during generation

**What it does**:
- Cleans the script text (removes markers, etc.)
- Splits into sentences for processing
- Generates audio for each sentence using Piper
- Concatenates all audio into a single MP3 file
- Shows progress and estimated time remaining

---

## Typical Workflow

```bash
# Step 1: See what chapters are available (FAST - Claude can help)
python scripts/extract_chapters.py textbook.pdf

# Step 2: Process a specific chapter (FAST - Claude can help)
python scripts/process_chapter.py textbook.pdf 3 output/scripts/chapter_03.txt

# Step 3: Analyze images (SLOW - Run standalone, ~5-10 minutes)
python scripts/analyze_images.py output/scripts/chapter_03.txt output/scripts/chapter_03_images/

# Step 4: Review and edit the script
# (Use Claude Code or any text editor to review/edit output/scripts/chapter_03.txt)

# Step 5: Generate audio (SLOW - Run standalone, ~2-3 hours)
python scripts/generate_audio.py output/scripts/chapter_03.txt output/audio/chapter_03.mp3
```

## Installation

Before using these scripts, install dependencies:

```bash
cd .claude/skills/pdf-audiobook
pip install -r requirements.txt
```

Additionally, install system dependencies:

### Piper TTS
```bash
pip install piper-tts
```

Or follow instructions at: https://github.com/rhasspy/piper

### FFmpeg
**Ubuntu/Debian**:
```bash
sudo apt install ffmpeg
```

**macOS**:
```bash
brew install ffmpeg
```

**Windows**:
Download from: https://ffmpeg.org/download.html

## Configuration

Copy the template and add your API key:

```bash
cp config.yaml.template config.yaml
# Edit config.yaml and add your Anthropic API key
```

## Troubleshooting

### "Piper not found"
Make sure piper-tts is installed:
```bash
pip install piper-tts
piper --version
```

### "ffmpeg not found"
Install ffmpeg using your system package manager (see above).

### "API key not found"
Make sure config.yaml exists and has a valid `anthropic_api_key`.

### "Chapter not found"
Run `extract_chapters.py` first to see available chapters.

### "Image analysis failed"
Check that:
- Image files exist in the specified directory
- API key is valid and has credits
- Internet connection is working

## Cost Estimates

- **Image Analysis**: ~$0.25-0.50 per image (Claude API)
- **Audio Generation**: $0 (runs locally)

**Example**: A 30-page chapter with 8 images costs approximately $2-4 total.

## Performance Tips

1. **Batch Processing**: Process multiple chapters sequentially
2. **Overnight Runs**: Run audio generation overnight or during work
3. **Review Scripts**: Always review before generating audio to avoid re-processing
4. **Keep Originals**: Save original PDFs until you're satisfied with all chapters

## Need Help?

Ask Claude Code! The skill is designed to help you through the entire process.

Just say:
- "Help me process chapter 3"
- "I'm getting an error with image analysis"
- "How do I customize the voice settings?"
