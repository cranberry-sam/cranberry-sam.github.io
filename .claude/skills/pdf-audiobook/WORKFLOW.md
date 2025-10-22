# Detailed Workflow

This document provides a complete step-by-step guide for converting a textbook PDF to an audiobook.

## Prerequisites

1. **Install dependencies**:
   ```bash
   cd .claude/skills/pdf-audiobook
   pip install -r requirements.txt
   ```

2. **Configure API key**:
   ```bash
   cp config.yaml.template config.yaml
   # Edit config.yaml and add your Anthropic API key
   ```

3. **Verify Piper installation**:
   ```bash
   piper --version
   ```

## Complete Workflow

### Step 1: Extract Chapter List (Interactive - Fast)

**You ask**: "Help me process chapters from textbook.pdf"

**I will**:
- Run `extract_chapters.py` to scan the PDF
- Display a list of chapters with page ranges
- Ask which chapter you'd like to process

**Script runs**:
```bash
python scripts/extract_chapters.py /path/to/textbook.pdf
```

**Output example**:
```
Found 12 chapters:
1. Introduction to Biology (pages 1-24)
2. Cell Structure (pages 25-56)
3. DNA and RNA (pages 57-89)
...
```

### Step 2: Process Chapter Text (Interactive - Fast)

**You select**: "Let's do chapter 3"

**I will**:
- Run `process_chapter.py` to extract text and locate images
- Identify sections to summarize (citations, indices, etc.)
- Create an initial script with placeholders for image descriptions

**Script runs**:
```bash
python scripts/process_chapter.py /path/to/textbook.pdf 3 output/scripts/chapter_03.txt
```

**Output**:
- Creates `output/scripts/chapter_03.txt` with text
- Creates `output/scripts/chapter_03_images/` with extracted images
- Lists how many images need descriptions

### Step 3: Analyze Images (Standalone - Minutes)

**I will tell you**:
```
Found 7 images in chapter 3. To analyze them with AI:

python .claude/skills/pdf-audiobook/scripts/analyze_images.py \
  output/scripts/chapter_03.txt \
  output/scripts/chapter_03_images/

This will take about 5-10 minutes and cost approximately $1.50.
Run this command and let me know when it's done!
```

**You run**: The command in your terminal (Claude is not consuming tokens during this)

**Script does**:
- Sends each image to Claude's vision API
- Generates detailed descriptions
- Identifies figure numbers and page references
- Updates the script file with descriptions

**You notify me**: "Image analysis is done"

### Step 4: Review and Edit Script (Interactive - Fast)

**I will**:
- Show you the generated script
- Highlight image descriptions and summarized sections
- Help you make any edits

**You can**:
- Read through the script
- Ask me to make changes: "Make figure 3.2 description more concise"
- Edit the file directly if you prefer

**Example script content**:
```
Chapter 3: DNA and RNA

In this chapter, we'll explore the fundamental molecules of heredity...

[On page 58, see Figure 3.1] This image shows the double helix structure
of DNA, with the sugar-phosphate backbone on the outside and base pairs
on the inside. The complementary base pairing is clearly visible, with
adenine bonding to thymine and guanine bonding to cytosine.

The text continues discussing the chemical structure...
```

### Step 5: Generate Audio (Standalone - Hours)

**I will tell you**:
```
Script looks good! To generate the audio:

python .claude/skills/pdf-audiobook/scripts/generate_audio.py \
  output/scripts/chapter_03.txt \
  output/audio/chapter_03.mp3

This will take approximately 2-3 hours for a typical chapter.
Run it in the background or overnight. It's completely free!
```

**You run**: The command (Claude is not consuming tokens during this)

**Script does**:
- Loads the text script
- Processes it sentence by sentence using Piper TTS
- Generates high-quality audio
- Outputs to MP3 format

**Progress tracking**:
The script will show progress:
```
Processing chapter 3...
Progress: 15% (Page 60 of 89)
Estimated time remaining: 1h 45m
```

### Step 6: Verify and Listen (Interactive - Fast)

**You notify me**: "Chapter 3 audio is ready"

**I will**:
- Check that the file was created successfully
- Show you the file details (size, duration)
- Help you troubleshoot if there were any issues

**You can**:
- Listen to the MP3
- Ask me to regenerate with different voice settings
- Process the next chapter

## Batch Processing

Once you're comfortable with the workflow, you can batch process:

```bash
# Process all chapters 1-12
for i in {1..12}; do
  python scripts/process_chapter.py textbook.pdf $i output/scripts/chapter_$(printf "%02d" $i).txt
  python scripts/analyze_images.py output/scripts/chapter_$(printf "%02d" $i).txt output/scripts/chapter_$(printf "%02d" $i)_images/
  python scripts/generate_audio.py output/scripts/chapter_$(printf "%02d" $i).txt output/audio/chapter_$(printf "%02d" $i).mp3
done
```

**Note**: This is completely autonomous - no Claude token costs!

## Customization Options

### Voice Settings

Edit `config.yaml` to customize:
- Voice model (different languages/accents)
- Speaking rate
- Volume
- Audio quality

### Text Processing Rules

You can configure what gets summarized:
- Bibliography sections
- Indices
- Long tables
- Footnotes
- Code listings

Ask me to help customize these settings based on your textbook's structure.

## Error Recovery

### If image analysis fails mid-way
The script saves progress. Re-running will skip already-analyzed images.

### If audio generation crashes
The script can resume from the last completed sentence.

### If you're not happy with the result
Just edit the script file and regenerate audio for that chapter.

## Tips for Best Results

1. **Start with one chapter**: Get familiar with the workflow before batch processing
2. **Review the first script carefully**: This helps you understand what to expect
3. **Customize voice settings early**: It's easier to get it right before processing 12 chapters
4. **Keep original PDFs**: Don't delete them until you're happy with all chapters
5. **Backup scripts**: The text scripts are valuable - they're edited and curated

## Next Chapter

Once chapter 3 is complete, just say:
- "Let's do chapter 4 next"
- "Process the next chapter"

I'll remember your preferences and make it even faster!
