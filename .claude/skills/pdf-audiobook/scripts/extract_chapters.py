#!/usr/bin/env python3
"""
Extract chapter information from a PDF file.

This script analyzes a PDF's table of contents and structure to identify chapters
and their page ranges.

Usage:
    python extract_chapters.py <pdf_path>

Example:
    python extract_chapters.py ~/Documents/textbook.pdf
"""

import sys
import fitz  # PyMuPDF
import re
from pathlib import Path


def extract_toc_from_metadata(pdf_path):
    """
    Extract table of contents from PDF metadata.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        List of tuples: (level, title, page_number)
    """
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()
    doc.close()
    return toc


def extract_chapters_from_toc(toc):
    """
    Parse the TOC to identify chapters.

    Args:
        toc: List of TOC entries from PyMuPDF

    Returns:
        List of chapter dictionaries with title and page ranges
    """
    chapters = []

    # Filter to top-level entries (usually chapters)
    top_level_entries = [entry for entry in toc if entry[0] == 1]

    for i, entry in enumerate(top_level_entries):
        level, title, start_page = entry

        # Determine end page
        if i < len(top_level_entries) - 1:
            end_page = top_level_entries[i + 1][2] - 1
        else:
            # Last chapter - we'll update this with total pages later
            end_page = None

        chapters.append({
            'number': i + 1,
            'title': title.strip(),
            'start_page': start_page,
            'end_page': end_page
        })

    return chapters


def extract_chapters_heuristic(pdf_path):
    """
    Fallback method: Use heuristics to find chapters if TOC is not available.

    Looks for patterns like "Chapter 1", "CHAPTER 1", etc. in large/bold text.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        List of chapter dictionaries
    """
    doc = fitz.open(pdf_path)
    chapters = []
    chapter_pattern = re.compile(r'chapter\s+(\d+)', re.IGNORECASE)

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()

        # Look for chapter headers
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines of each page
            match = chapter_pattern.search(line)
            if match:
                chapter_num = int(match.group(1))
                # Extract chapter title (usually the rest of the line)
                title = line.strip()

                chapters.append({
                    'number': chapter_num,
                    'title': title,
                    'start_page': page_num + 1,  # PyMuPDF is 0-indexed
                    'end_page': None  # Will be filled in later
                })
                break

    # Fill in end pages
    for i in range(len(chapters) - 1):
        chapters[i]['end_page'] = chapters[i + 1]['start_page'] - 1

    doc.close()
    return chapters


def get_total_pages(pdf_path):
    """Get total number of pages in the PDF."""
    doc = fitz.open(pdf_path)
    total = len(doc)
    doc.close()
    return total


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_chapters.py <pdf_path>")
        print("Example: python extract_chapters.py ~/Documents/textbook.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]

    # Validate file exists
    if not Path(pdf_path).exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    print(f"Analyzing PDF: {pdf_path}")
    print("=" * 60)

    # Get total pages
    total_pages = get_total_pages(pdf_path)
    print(f"Total pages: {total_pages}\n")

    # Try to extract TOC from metadata first
    toc = extract_toc_from_metadata(pdf_path)

    if toc:
        print("Found table of contents in PDF metadata.\n")
        chapters = extract_chapters_from_toc(toc)

        # Update last chapter's end page
        if chapters:
            chapters[-1]['end_page'] = total_pages
    else:
        print("No TOC found in metadata. Using heuristic search...\n")
        chapters = extract_chapters_heuristic(pdf_path)

        if chapters:
            chapters[-1]['end_page'] = total_pages
        else:
            print("Could not automatically detect chapters.")
            print("You may need to manually specify chapter page ranges.")
            sys.exit(1)

    # Display results
    if chapters:
        print(f"Found {len(chapters)} chapters:\n")
        for chapter in chapters:
            page_range = f"pages {chapter['start_page']}-{chapter['end_page']}"
            page_count = chapter['end_page'] - chapter['start_page'] + 1
            print(f"{chapter['number']:2d}. {chapter['title']}")
            print(f"    {page_range} ({page_count} pages)")
            print()
    else:
        print("No chapters found.")

    print("=" * 60)
    print(f"\nTo process a specific chapter, use:")
    print(f"python scripts/process_chapter.py {pdf_path} <chapter_number> <output_file>")


if __name__ == "__main__":
    main()
