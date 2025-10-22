#!/usr/bin/env python3
"""
Analyze images using Claude's vision API and insert descriptions into the script.

This is a STANDALONE script that runs independently (not during Claude Code conversation).
It processes all images and updates the script file with AI-generated descriptions.

Usage:
    python analyze_images.py <script_file> <image_directory>

Example:
    python analyze_images.py output/scripts/chapter_03.txt output/scripts/chapter_03_images/

Environment:
    Requires ANTHROPIC_API_KEY in config.yaml or environment variable
"""

import sys
import os
import re
import base64
from pathlib import Path
import yaml
from anthropic import Anthropic


def load_config():
    """Load configuration from config.yaml."""
    config_path = Path(__file__).parent.parent / "config.yaml"

    if not config_path.exists():
        print("Error: config.yaml not found.")
        print("Please copy config.yaml.template to config.yaml and add your API key.")
        sys.exit(1)

    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Check for API key
    api_key = config.get('api', {}).get('anthropic_api_key')
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        # Try environment variable
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            print("Error: ANTHROPIC_API_KEY not found in config.yaml or environment.")
            sys.exit(1)

    return config, api_key


def get_image_base64(image_path):
    """Read image file and encode as base64."""
    with open(image_path, 'rb') as f:
        return base64.standard_b64encode(f.read()).decode('utf-8')


def get_image_media_type(image_path):
    """Determine media type from file extension."""
    ext = Path(image_path).suffix.lower()
    media_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    return media_types.get(ext, 'image/jpeg')


def analyze_image_with_claude(client, image_path, config, context=""):
    """
    Analyze an image using Claude's vision API.

    Args:
        client: Anthropic client
        image_path: Path to image file
        config: Configuration dictionary
        context: Additional context about the image (e.g., figure label, page number)

    Returns:
        Description string
    """
    model = config.get('image_analysis', {}).get('model', 'claude-3-5-sonnet-20241022')
    max_tokens = config.get('image_analysis', {}).get('max_tokens', 500)
    style = config.get('image_analysis', {}).get('description_style', 'detailed')
    include_technical = config.get('image_analysis', {}).get('include_technical_details', True)

    # Build prompt based on configuration
    style_instructions = {
        'concise': 'Provide a brief, concise description in 1-2 sentences.',
        'detailed': 'Provide a detailed description suitable for an audiobook listener.',
        'very_detailed': 'Provide a very detailed, comprehensive description including all visible elements.'
    }

    style_prompt = style_instructions.get(style, style_instructions['detailed'])

    technical_prompt = ""
    if include_technical:
        technical_prompt = " Include relevant technical details, labels, and annotations visible in the image."

    prompt = f"""You are helping create an audiobook from a textbook. Describe this image/figure for someone who cannot see it.

{context}

{style_prompt}{technical_prompt}

Format your response as natural text suitable for audio narration. Do not use phrases like "this image shows" - just describe what's in the image directly.

For example:
- Good: "The diagram illustrates a double helix structure with base pairs connecting the two strands."
- Avoid: "This image shows a double helix structure..."
"""

    # Encode image
    image_data = get_image_base64(image_path)
    media_type = get_image_media_type(image_path)

    # Call Claude API
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )

    return message.content[0].text


def find_images_in_script(script_text):
    """
    Find all image placeholders in the script.

    Returns:
        List of tuples: (placeholder_text, image_number)
    """
    pattern = re.compile(r'\{\{IMAGE_PLACEHOLDER_(\d+)\}\}')
    matches = pattern.finditer(script_text)

    placeholders = []
    for match in matches:
        placeholder_text = match.group(0)
        image_number = int(match.group(1))
        placeholders.append((placeholder_text, image_number))

    return placeholders


def extract_context_for_image(script_text, placeholder):
    """
    Extract context around an image placeholder (figure label, page number, etc.).

    Args:
        script_text: Full script text
        placeholder: Placeholder text to search for

    Returns:
        Context string
    """
    # Find the placeholder and grab surrounding text
    placeholder_index = script_text.find(placeholder)
    if placeholder_index == -1:
        return ""

    # Get text around placeholder (500 chars before and after)
    start = max(0, placeholder_index - 500)
    end = min(len(script_text), placeholder_index + 500)
    context_text = script_text[start:end]

    # Extract figure label and page number if present
    figure_match = re.search(r'\[(Figure [\d.]+)[^\]]*on page (\d+)\]', context_text)

    if figure_match:
        figure_label = figure_match.group(1)
        page_number = figure_match.group(2)
        return f"This is {figure_label} on page {page_number} of the textbook."

    # Fallback
    page_match = re.search(r'\[PAGE (\d+)\]', context_text)
    if page_match:
        return f"This image appears on page {page_match.group(1)} of the textbook."

    return ""


def update_script_with_description(script_text, placeholder, description, context):
    """
    Replace image placeholder with the AI-generated description.

    Args:
        script_text: Full script text
        placeholder: Placeholder text to replace
        description: AI-generated description
        context: Context string (figure label, page number)

    Returns:
        Updated script text
    """
    # Build the replacement text
    replacement = f"\n[Image Description]\n"
    if context:
        replacement += f"{context} "
    replacement += f"{description}\n"

    # Replace the placeholder section
    # We want to replace from the placeholder to the end of the placeholder section
    pattern = re.compile(
        re.escape(placeholder) + r'.*?\(Image description will be inserted here by analyze_images\.py\)',
        re.DOTALL
    )

    updated_script = pattern.sub(replacement, script_text, count=1)
    return updated_script


def main():
    if len(sys.argv) < 3:
        print("Usage: python analyze_images.py <script_file> <image_directory>")
        print("Example: python analyze_images.py output/scripts/chapter_03.txt output/scripts/chapter_03_images/")
        sys.exit(1)

    script_file = sys.argv[1]
    image_dir = sys.argv[2]

    # Validate inputs
    script_path = Path(script_file)
    if not script_path.exists():
        print(f"Error: Script file not found: {script_file}")
        sys.exit(1)

    image_path = Path(image_dir)
    if not image_path.exists():
        print(f"Error: Image directory not found: {image_dir}")
        sys.exit(1)

    # Load config and API key
    config, api_key = load_config()
    client = Anthropic(api_key=api_key)

    print(f"Analyzing images for: {script_file}")
    print("=" * 60)

    # Load script
    with open(script_path, 'r', encoding='utf-8') as f:
        script_text = f.read()

    # Find all image placeholders
    placeholders = find_images_in_script(script_text)
    print(f"Found {len(placeholders)} images to analyze\n")

    if not placeholders:
        print("No image placeholders found in script.")
        print("This script may have already been processed, or there are no images.")
        sys.exit(0)

    # Process each image
    for i, (placeholder, image_num) in enumerate(placeholders, 1):
        print(f"Processing image {i}/{len(placeholders)} (image_{image_num:03d})...")

        # Find image file
        image_files = list(image_path.glob(f"image_{image_num:03d}.*"))
        if not image_files:
            print(f"  Warning: Image file not found for image_{image_num:03d}")
            continue

        image_file = image_files[0]

        # Extract context
        context = extract_context_for_image(script_text, placeholder)
        if context:
            print(f"  Context: {context}")

        # Analyze image
        try:
            description = analyze_image_with_claude(client, image_file, config, context)
            print(f"  Description generated ({len(description)} chars)")

            # Update script
            script_text = update_script_with_description(script_text, placeholder, description, context)

        except Exception as e:
            print(f"  Error analyzing image: {e}")
            continue

        print()

    # Save updated script
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_text)

    print("=" * 60)
    print(f"Script updated: {script_file}")
    print(f"\nAll {len(placeholders)} images have been analyzed and descriptions inserted.")
    print("\nNext step: Review the script and then generate audio:")
    print(f"python scripts/generate_audio.py {script_file} output/audio/<output_file>.mp3")


if __name__ == "__main__":
    main()
