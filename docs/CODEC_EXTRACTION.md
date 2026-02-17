# Codec Extraction - Implementation Updated

## Changes Made

### 1. **Updated FFmpeg Analyzer** (`src/utils/ffmpeg_analyzer.py`)

The codec extraction method has been completely rewritten to use a more reliable "dirty way" approach as you suggested:

**Old Method:**
- Used ffprobe with complex flags (`-select_streams`, `-show_entries`, `-of`)
- Sometimes failed silently or returned unexpected formats

**New Method:**
- Runs `ffprobe <filepath>` directly (simple approach)
- Parses the human-readable output using regex patterns
- More robust and reliable across different ffmpeg versions
- Easier to debug and understand

### 2. **Improved Codec Parsing**

The new parsing logic:
```python
# Parse output for video codec
# Looks for: "Stream #0:0: Video: h264 (profile), ..."
video_match = re.search(
    r'Stream\s+#\d+:\d+.*?Video:\s+([^\s,\[]+)',
    output
)

# Parse output for audio codec  
# Looks for: "Stream #0:1: Audio: aac, ..."
audio_match = re.search(
    r'Stream\s+#\d+:\d+.*?Audio:\s+([^\s,\[]+)',
    output
)
```

### 3. **Codec Name Cleaning**

Added `_clean_codec_name()` method to normalize codec names:
- Removes profile information: `h264 (High 4:4:4 Predictive)` → `h264`
- Handles codec name variations: `h.264` → `h264`, `ac-3` → `ac3`
- Standardizes output for compatibility checking

### 4. **Better Error Handling**

- Application now checks for FFmpeg availability at startup
- Clear warning messages if FFmpeg is not installed
- Helpful installation instructions for each platform

## Test Results

The test script (`test_codec_extraction.py`) demonstrates the functionality:

### Test Case 1: H.264 + AAC (Compatible) ✓
```
Input: H.264 video + AAC audio (MP4)
Output: Video: h264, Audio: aac
Result: Compatible with Samsung TV ✓
```

### Test Case 2: H.265 + Vorbis (Incompatible) ✗
```
Input: HEVC video + Vorbis audio (MKV)
Output: Video: hevc, Audio: vorbis
Result: Incompatible - Audio codec not supported ✗
Reason: Audio codec 'vorbis' not compatible
```

### Test Case 3: VP9 + Opus (Incompatible) ✗
```
Input: VP9 video + Opus audio (WebM)
Output: Video: vp9, Audio: opus
Result: Incompatible - Both codecs not supported ✗
Reason: Video codec 'vp9' not compatible; Audio codec 'opus' not compatible
```

## How It Works Now

1. **User clicks "Scan Folder"**
   - Application recursively finds all video files
   - Found files are displayed in the table

2. **Codec Analysis Starts** (if FFmpeg is installed)
   - For each video file, runs: `ffprobe <filepath>`
   - Parses output to extract video and audio codec names
   - Cleans up codec names for consistency

3. **Compatibility Check**
   - Compares codecs against Samsung TV compatible list:
     - **Video**: H.264 (AVC), H.265 (HEVC)
     - **Audio**: AAC, MP3, AC3, EAC3, FLAC, PCM

4. **Display Results**
   - Shows codec names in grid
   - Green ✓ for compatible files
   - Red ✗ for incompatible files with reason

5. **Context Menu for Conversion**
   - Right-click incompatible files
   - Convert to H.264 + AAC (MP4 container)
   - Custom output file location

## Supported Codec Detection

The application can now detect:

### Video Codecs
- H.264 / AVC
- H.265 / HEVC
- VP8, VP9
- AV1
- MPEG2
- Xvid/MPEG4

### Audio Codecs
- AAC
- MP3
- AC3 (Dolby Digital)
- EAC3 (Dolby Digital Plus)
- Vorbis
- Opus
- FLAC
- PCM
- And many more!

## Installation Requirements

To use the codec analysis features, install FFmpeg:

**Windows:**
```powershell
.\setup_ffmpeg.ps1
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

## Testing

Run the test script to verify codec extraction:
```bash
python test_codec_extraction.py
```

This will show:
- How codec names are cleaned/normalized
- Real ffprobe output parsing examples
- Compatibility checking logic
- Samsung TV compatibility results

## Next Steps

1. **Install FFmpeg** using one of the methods above
2. **Run the application**: `python -m src.main`
3. **Scan a folder** with video files
4. **View codec information** and compatibility status
5. **Convert files** as needed using the context menu

---

**The application is now ready to properly display video and audio codec information!**
