#!/usr/bin/env python3
"""
Process a PDF file for audiobook conversion.

This script:
1. Extracts text from the specified pages/chapter
2. Identifies and extracts images
3. Creates placeholders for image descriptions (filled in by Claude Code)
4. Identifies sections that should be summarized (citations, indices, etc.)
5. Outputs a script file ready for audio generation

Usage:
    # Process specific chapter (requires TOC)
    python3 process_chapter.py <pdf_path> <chapter_number> <output_script>

    # Process entire document
    python3 process_chapter.py <pdf_path> --full <output_script>

    # Process custom page range
    python3 process_chapter.py <pdf_path> --pages <start-end> <output_script>

Examples:
    python3 process_chapter.py textbook.pdf 3 output/scripts/chapter_03.txt
    python3 process_chapter.py paper.pdf --full output/scripts/full_paper.txt
    python3 process_chapter.py book.pdf --pages 10-25 output/scripts/section.txt
"""

import sys
import fitz  # PyMuPDF
import re
from pathlib import Path
import yaml


def load_config():
    """Load configuration from config.yaml."""
    config_path = Path(__file__).parent.parent / "config.yaml"
    if not config_path.exists():
        print("Warning: config.yaml not found. Using defaults.")
        return {
            'text_processing': {
                'summarize_sections': ['bibliography', 'references', 'index', 'appendix'],
                'citation_length_threshold': 200,
                'table_handling': 'describe'
            }
        }

    with open(config_path) as f:
        return yaml.safe_load(f)


def get_chapter_pages(pdf_path, chapter_number):
    """
    Determine the page range for a specific chapter.

    Args:
        pdf_path: Path to PDF
        chapter_number: Chapter number (1-indexed)

    Returns:
        Tuple of (start_page, end_page) or None if not found
    """
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()

    if toc:
        # Use TOC to find chapter
        chapters = [entry for entry in toc if entry[0] == 1]

        if 0 < chapter_number <= len(chapters):
            start_page = chapters[chapter_number - 1][2]

            if chapter_number < len(chapters):
                end_page = chapters[chapter_number][2] - 1
            else:
                end_page = len(doc)

            doc.close()
            return (start_page - 1, end_page - 1)  # Convert to 0-indexed

    doc.close()
    return None


def extract_text_from_pages(pdf_path, start_page, end_page):
    """
    Extract text from a page range.

    Args:
        pdf_path: Path to PDF
        start_page: Starting page (0-indexed)
        end_page: Ending page (0-indexed)

    Returns:
        List of dictionaries with page number and text
    """
    doc = fitz.open(pdf_path)
    pages_text = []

    for page_num in range(start_page, end_page + 1):
        page = doc[page_num]
        text = page.get_text()

        pages_text.append({
            'page_number': page_num + 1,  # Convert to 1-indexed for display
            'text': text
        })

    doc.close()
    return pages_text


def extract_images_from_pages(pdf_path, start_page, end_page, output_dir):
    """
    Extract images from a page range.

    Args:
        pdf_path: Path to PDF
        start_page: Starting page (0-indexed)
        end_page: Ending page (0-indexed)
        output_dir: Directory to save images

    Returns:
        List of image metadata dictionaries
    """
    doc = fitz.open(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    images = []
    image_counter = 1

    for page_num in range(start_page, end_page + 1):
        page = doc[page_num]
        image_list = page.get_images()

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            # Save image
            image_filename = f"image_{image_counter:03d}.{image_ext}"
            image_path = output_dir / image_filename

            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

            images.append({
                'image_number': image_counter,
                'page_number': page_num + 1,
                'filename': image_filename,
                'path': str(image_path),
                'figure_label': None  # Will try to detect later
            })

            image_counter += 1

    doc.close()
    return images


def detect_figure_labels(pages_text, images):
    """
    Try to detect figure labels like "Figure 3.1" in the text.

    Args:
        pages_text: List of page text dictionaries
        images: List of image metadata dictionaries

    Returns:
        Updated images list with figure labels
    """
    figure_pattern = re.compile(r'Figure\s+(\d+\.?\d*)', re.IGNORECASE)

    for img in images:
        page_num = img['page_number']

        # Find the corresponding page text
        for page_data in pages_text:
            if page_data['page_number'] == page_num:
                text = page_data['text']

                # Look for figure labels
                matches = figure_pattern.findall(text)
                if matches:
                    # Assign the first match to this image
                    # (This is a simple heuristic; could be improved)
                    img['figure_label'] = f"Figure {matches[0]}"
                break

    return images


def is_summary_section(text, config):
    """
    Determine if a section should be summarized instead of read verbatim.

    Args:
        text: Text to check
        config: Configuration dictionary

    Returns:
        Boolean indicating if this should be summarized
    """
    summary_keywords = config.get('text_processing', {}).get('summarize_sections', [])

    text_lower = text.lower()

    for keyword in summary_keywords:
        if keyword in text_lower:
            return True

    return False


def create_script(pages_text, images, config):
    """
    Create the audiobook script with text and image placeholders.

    Args:
        pages_text: List of page text dictionaries
        images: List of image metadata dictionaries
        config: Configuration dictionary

    Returns:
        Script text as a string
    """
    script_lines = []

    for page_data in pages_text:
        page_num = page_data['page_number']
        text = page_data['text']

        # Add page marker (useful for debugging)
        script_lines.append(f"\n[PAGE {page_num}]\n")

        # Check for images on this page
        page_images = [img for img in images if img['page_number'] == page_num]

        # Add image placeholders
        for img in page_images:
            figure_ref = img['figure_label'] if img['figure_label'] else f"Image {img['image_number']}"
            script_lines.append(f"\n{{{{IMAGE_PLACEHOLDER_{img['image_number']:03d}}}}}")
            script_lines.append(f"[{figure_ref} on page {page_num}]")
            script_lines.append("(Image description will be inserted here by analyze_images.py)\n")

        # Check if this is a summary section
        if is_summary_section(text, config):
            script_lines.append("\n[SUMMARY SECTION - This section contains references/citations]")
            script_lines.append("This section contains bibliographic references and citations.")
            script_lines.append("Please refer to page {page_num} in your textbook for detailed citations.\n")
        else:
            # Add the actual text
            script_lines.append(text)

    return "\n".join(script_lines)


def parse_page_range(range_str):
    """Parse page range string like '10-25' into (start, end) tuple (0-indexed)."""
    try:
        start, end = range_str.split('-')
        return (int(start) - 1, int(end) - 1)  # Convert to 0-indexed
    except:
        print(f"Error: Invalid page range '{range_str}'. Use format: START-END (e.g., 1-52)")
        sys.exit(1)


def main():
    if len(sys.argv) < 4:
        print("Usage:")
        print("  python3 process_chapter.py <pdf_path> <chapter_number> <output_script>")
        print("  python3 process_chapter.py <pdf_path> --full <output_script>")
        print("  python3 process_chapter.py <pdf_path> --pages <start-end> <output_script>")
        print("\nExamples:")
        print("  python3 process_chapter.py textbook.pdf 3 output/scripts/chapter_03.txt")
        print("  python3 process_chapter.py paper.pdf --full output/scripts/full_paper.txt")
        print("  python3 process_chapter.py book.pdf --pages 10-25 output/scripts/section.txt")
        sys.exit(1)

    pdf_path = sys.argv[1]
    mode_arg = sys.argv[2]
    output_script = sys.argv[3]

    # Validate file exists
    if not Path(pdf_path).exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    # Load config
    config = load_config()

    # Determine page range based on mode
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()

    if mode_arg == '--full':
        # Process entire document
        start_page = 0
        end_page = total_pages - 1
        print(f"Processing entire document from: {pdf_path}")
        print("=" * 60)
        print(f"Total pages: {total_pages}")

    elif mode_arg == '--pages':
        # Process custom page range
        if len(sys.argv) < 5:
            print("Error: --pages requires a range argument (e.g., --pages 10-25)")
            sys.exit(1)
        page_range_str = sys.argv[3]
        output_script = sys.argv[4]
        start_page, end_page = parse_page_range(page_range_str)

        # Validate range
        if start_page < 0 or end_page >= total_pages or start_page > end_page:
            print(f"Error: Invalid page range {start_page+1}-{end_page+1} (document has {total_pages} pages)")
            sys.exit(1)

        print(f"Processing pages {start_page + 1} to {end_page + 1} from: {pdf_path}")
        print("=" * 60)

    else:
        # Process specific chapter (original behavior)
        try:
            chapter_number = int(mode_arg)
        except ValueError:
            print(f"Error: Invalid argument '{mode_arg}'. Expected chapter number, --full, or --pages")
            sys.exit(1)

        print(f"Processing Chapter {chapter_number} from: {pdf_path}")
        print("=" * 60)

        # Get chapter page range
        page_range = get_chapter_pages(pdf_path, chapter_number)
        if not page_range:
            print(f"Error: Could not find chapter {chapter_number}")
            print("This PDF may not have a table of contents.")
            print("Try using --full to process the entire document, or --pages START-END for a specific range.")
            sys.exit(1)

        start_page, end_page = page_range
        print(f"Chapter {chapter_number}: pages {start_page + 1} to {end_page + 1}")

    # Extract text
    print("\nExtracting text...")
    pages_text = extract_text_from_pages(pdf_path, start_page, end_page)
    print(f"Extracted text from {len(pages_text)} pages")

    # Extract images
    print("\nExtracting images...")
    output_path = Path(output_script)
    image_dir = output_path.parent / f"{output_path.stem}_images"
    images = extract_images_from_pages(pdf_path, start_page, end_page, image_dir)
    print(f"Extracted {len(images)} images to: {image_dir}")

    # Detect figure labels
    if images:
        print("\nDetecting figure labels...")
        images = detect_figure_labels(pages_text, images)
        for img in images:
            label = img['figure_label'] or f"Image {img['image_number']}"
            print(f"  - {label} (page {img['page_number']})")

    # Create script
    print("\nCreating script...")
    script = create_script(pages_text, images, config)

    # Save script
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_script, 'w', encoding='utf-8') as f:
        f.write(script)

    print(f"\nScript saved to: {output_script}")
    print("=" * 60)

    if images:
        print(f"\nNext step: Claude Code will analyze {len(images)} images and insert descriptions.")
        print("(This happens automatically in the Claude Code workflow)")
    else:
        print("\nNo images found in this section.")

    print(f"\nAfter image analysis, generate audio with:")
    print(f"python3 scripts/generate_audio_python.py {output_script} output/audio/audiobook.mp3")


if __name__ == "__main__":
    main()
