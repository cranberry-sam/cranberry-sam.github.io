# Usage Examples

This document shows real conversation examples and common scenarios.

## Example 1: First Time User

**You**: I want to convert my biology textbook to an audiobook so I can listen during my commute.

**Claude**: Great! I can help you create an audiobook from your PDF with AI-generated descriptions of any figures and images. First, let's get the PDF path. Where is your textbook located?

**You**: ~/Documents/biology_textbook.pdf

**Claude**: Perfect! Let me extract the chapter information...

```bash
python .claude/skills/pdf-audiobook/scripts/extract_chapters.py ~/Documents/biology_textbook.pdf
```

I found 15 chapters in your textbook:
1. Introduction to Biology (pages 1-28)
2. Chemical Basis of Life (pages 29-54)
3. Cell Structure and Function (pages 55-89)
4. Cellular Respiration (pages 90-121)
...

Which chapter would you like to start with?

**You**: Let's do chapter 3

**Claude**: Processing chapter 3: Cell Structure and Function...

```bash
python .claude/skills/pdf-audiobook/scripts/process_chapter.py ~/Documents/biology_textbook.pdf 3 output/scripts/chapter_03.txt
```

Done! I found 8 images in this chapter. To analyze them with AI:

```bash
python .claude/skills/pdf-audiobook/scripts/analyze_images.py \
  output/scripts/chapter_03.txt \
  output/scripts/chapter_03_images/
```

This will take about 5-10 minutes and cost approximately $2. Run this and let me know when it's done!

**You**: [Runs the command, waits] It's done!

**Claude**: Great! Let me show you the generated script... [reads file]

The script looks good. I've generated descriptions for all 8 figures including:
- Figure 3.1 (page 57): Prokaryotic vs Eukaryotic cells
- Figure 3.2 (page 61): Cell membrane structure
- Figure 3.3 (page 68): Mitochondria cross-section
...

Would you like to review or edit anything before generating the audio?

**You**: Looks good!

**Claude**: Perfect! To generate the audio:

```bash
python .claude/skills/pdf-audiobook/scripts/generate_audio.py \
  output/scripts/chapter_03.txt \
  output/audio/chapter_03.mp3
```

This will take about 2-3 hours. Run it in the background and you'll have your audiobook!

---

## Example 2: Editing Before Audio Generation

**You**: I reviewed the script and the description for Figure 3.5 is too technical. Can you simplify it?

**Claude**: Of course! Let me read the current description for Figure 3.5...

[reads output/scripts/chapter_03.txt]

Current description:
"Figure 3.5 on page 72 depicts the electron transport chain with complexes I through IV embedded in the inner mitochondrial membrane, showing the movement of electrons through the cytochrome pathway and the pumping of protons into the intermembrane space."

How would you like me to simplify it?

**You**: Just say it shows how the cell creates energy using the mitochondria.

**Claude**: [edits the file]

Updated! New description:
"Figure 3.5 on page 72 shows how the cell creates energy using the mitochondria."

Ready to generate audio now?

---

## Example 3: Batch Processing Multiple Chapters

**You**: Can I process all chapters at once?

**Claude**: Absolutely! Since you're already familiar with the workflow, you can run a batch process. Here's a script that will process chapters 1-15:

```bash
#!/bin/bash
# Save this as process_all_chapters.sh

for i in {1..15}; do
  chapter_num=$(printf "%02d" $i)
  echo "Processing chapter $i..."

  # Extract and process chapter
  python scripts/process_chapter.py ~/Documents/biology_textbook.pdf $i output/scripts/chapter_${chapter_num}.txt

  # Analyze images
  python scripts/analyze_images.py \
    output/scripts/chapter_${chapter_num}.txt \
    output/scripts/chapter_${chapter_num}_images/

  # Generate audio
  python scripts/generate_audio.py \
    output/scripts/chapter_${chapter_num}.txt \
    output/audio/chapter_${chapter_num}.mp3

  echo "Chapter $i complete!"
done

echo "All chapters processed!"
```

**Note**: This will take many hours and cost approximately $15-30 total for all 15 chapters. You might want to review the scripts for each chapter before generating audio. Let me know if you want a version that pauses for review.

---

## Example 4: Customizing Voice Settings

**You**: The voice sounds too slow. Can I speed it up?

**Claude**: Yes! Let me check your current config...

[reads .claude/skills/pdf-audiobook/config.yaml]

Current speaking rate is 1.0 (normal speed). Let's increase it to 1.25 (25% faster):

[edits config.yaml]

```yaml
tts:
  speaking_rate: 1.25  # Changed from 1.0
  voice_model: "en_US-lessac-medium"
  audio_quality: "high"
```

Now regenerate the audio for any chapter:

```bash
python scripts/generate_audio.py \
  output/scripts/chapter_03.txt \
  output/audio/chapter_03.mp3
```

The new audio will use the faster rate. Want to adjust it more?

---

## Example 5: Handling Errors

**You**: The image analysis crashed halfway through. What should I do?

**Claude**: No problem! The script saves progress. Let me check what was completed...

[reads output/scripts/chapter_03.txt and checks progress]

It looks like 5 out of 8 images were analyzed successfully. The script will automatically skip those and only process the remaining 3. Just re-run the command:

```bash
python .claude/skills/pdf-audiobook/scripts/analyze_images.py \
  output/scripts/chapter_03.txt \
  output/scripts/chapter_03_images/
```

It will only process images 6, 7, and 8 - should take about 2 minutes.

---

## Example 6: Starting the Next Chapter

**You**: Chapter 3 is done! Let's do chapter 4.

**Claude**: Great! Since we already have your textbook loaded, I'll process chapter 4 right away:

```bash
python scripts/process_chapter.py ~/Documents/biology_textbook.pdf 4 output/scripts/chapter_04.txt
```

Chapter 4: Cellular Respiration (pages 90-121) extracted!

Found 6 images. Ready to analyze:

```bash
python scripts/analyze_images.py \
  output/scripts/chapter_04.txt \
  output/scripts/chapter_04_images/
```

---

## Example 7: Just Want to See Chapter List

**You**: What chapters are in my textbook again?

**Claude**: Let me extract the chapter list:

```bash
python scripts/extract_chapters.py ~/Documents/biology_textbook.pdf
```

Here's what I found:
1. Introduction to Biology (pages 1-28)
2. Chemical Basis of Life (pages 29-54)
3. Cell Structure and Function (pages 55-89)
4. Cellular Respiration (pages 90-121)
5. Photosynthesis (pages 122-156)
...

Which one would you like to work on?

---

## Example 8: Processing a Different PDF

**You**: I have another textbook I want to convert. It's a chemistry book.

**Claude**: Perfect! What's the path to your chemistry textbook?

**You**: ~/Documents/chemistry.pdf

**Claude**: Got it! Let me extract the chapters...

```bash
python scripts/extract_chapters.py ~/Documents/chemistry.pdf
```

[Workflow continues as normal...]

---

## Quick Reference Commands

Once you're familiar with the skill, here are the key commands:

```bash
# 1. See chapters
python scripts/extract_chapters.py <pdf_path>

# 2. Process a chapter
python scripts/process_chapter.py <pdf_path> <chapter_number> output/scripts/chapter_XX.txt

# 3. Analyze images (standalone)
python scripts/analyze_images.py output/scripts/chapter_XX.txt output/scripts/chapter_XX_images/

# 4. Generate audio (standalone)
python scripts/generate_audio.py output/scripts/chapter_XX.txt output/audio/chapter_XX.mp3
```

You can run these yourself or ask me to help at any step!
