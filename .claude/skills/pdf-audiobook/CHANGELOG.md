# Changelog

## 2026-01-29 - Major Refactor: Claude Code-First

### Summary
Refactored the entire skill to be Claude Code-first, eliminating redundant scripts and API costs.

### Key Changes

#### 1. Unified Document Processing ✅
- **Updated `process_chapter.py`** to handle three modes:
  - `python3 process_chapter.py book.pdf 3 output.txt` - Process chapter 3
  - `python3 process_chapter.py book.pdf --full output.txt` - Process entire document
  - `python3 process_chapter.py book.pdf --pages 10-25 output.txt` - Process page range
- **Removed `process_full_document.py`** (functionality merged into `process_chapter.py`)

#### 2. Interactive Voice Selection ✅
- **Updated `generate_audio_python.py`** to prompt for voice selection
- Added 8 voice options with descriptions
- Changed default from `en_US-lessac-medium` to `en_US-ryan-high` (based on user feedback)
- Voice selection happens at audio generation time

#### 3. Python3 Best Practices ✅
- All documentation updated to use `python3` instead of `python`
- All scripts already have `#!/usr/bin/env python3` shebangs
- Consistent command examples throughout

#### 4. Claude Code-First Workflow ✅
- **Removed `analyze_images.py`** - Claude analyzes images directly in conversation
- **Removed API key requirement** from `config.yaml` and templates
- Updated all documentation to emphasize Claude Code integration
- Cost changed from "$10-20 per book" to "$0"
- Workflow simplified: extract → Claude analyzes → generate audio

#### 5. Documentation Updates ✅
- **README.md**: Complete rewrite emphasizing Claude Code-only usage
- **SKILL.md**: Updated to reflect zero-cost, Claude-integrated workflow
- **config.yaml.template**: Removed API key section, updated defaults
- **config.yaml**: Removed API key, changed default voice to ryan-high
- Added ⚠️ warnings that skill is Claude Code-only

#### 6. Removed Obsolete Files ✅
- `analyze_images.py` - No longer needed (Claude does this)
- `generate_audio.py` - Replaced by `generate_audio_python.py`
- `process_full_document.py` - Merged into `process_chapter.py`

### Remaining Scripts

1. **extract_chapters.py** - Helper to view PDF structure (optional)
2. **process_chapter.py** - Main extraction script (supports --full and --pages)
3. **generate_audio_python.py** - Audio generation with voice selection

### User-Facing Changes

**Before:**
1. Run extract script
2. Run analyze_images.py (costs $2-4, takes 5-10 min, requires API key)
3. Run generate_audio.py (free, takes hours)

**After:**
1. Claude extracts and analyzes images automatically (free, seconds)
2. Run generate_audio_python.py with voice selection (free, takes hours)

### Configuration Changes

**Before:**
```yaml
api:
  anthropic_api_key: "YOUR_API_KEY_HERE"
tts:
  voice_model: "en_US-lessac-medium"
```

**After:**
```yaml
# No API key needed!
tts:
  voice_model: "en_US-ryan-high"  # Better default voice
```

### Benefits

- **Zero API costs** - Everything runs in Claude Code or locally
- **Simpler workflow** - No standalone image analysis step
- **Better voices** - Interactive selection + better default
- **More flexible** - Can process full documents, chapters, or page ranges
- **Consistent commands** - All use `python3`
- **Clearer documentation** - Emphasizes Claude Code integration

### Breaking Changes

- Users with existing `config.yaml` files should update to remove `api:` section
- Command examples changed from `python` to `python3`
- `analyze_images.py` removed - use Claude Code workflow instead

### Migration Guide

If you have existing setups:

1. Update `config.yaml` to remove the `api:` section
2. Change default voice to `en_US-ryan-high` (optional but recommended)
3. Use `python3` instead of `python` in all commands
4. Delete `analyze_images.py`, `generate_audio.py`, `process_full_document.py` if present
5. For full documents, use `--full` flag instead of separate script
