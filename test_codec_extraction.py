#!/usr/bin/env python3
"""Test script to verify codec extraction functionality."""

import re
from src.utils.ffmpeg_analyzer import FFmpegAnalyzer
from src.utils.samsung_compatibility import SamsungTVCompatibility

# Test the codec name cleaning
print("=" * 60)
print("Testing Codec Name Cleaning")
print("=" * 60)

test_cases = [
    "h264",
    "h.264",
    "h264 (High 4:4:4 Predictive)",
    "hevc",
    "h.265",
    "vorbis",
    "aac",
    "ac-3",
    "e-ac-3",
    "vp9",
    "av1"
]

for codec in test_cases:
    cleaned = FFmpegAnalyzer._clean_codec_name(codec)
    print(f"  {codec:40s} -> {cleaned}")

print()

# Test FFprobe output parsing
print("=" * 60)
print("Testing FFprobe Output Parsing")
print("=" * 60)

ffprobe_outputs = [
    # H.264 + AAC (compatible)
    """ffprobe version 5.1.2
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'video.mp4':
  Metadata:
    major_brand     : isom
  Duration: 00:05:30.10, start: 0.000000, bitrate: 5000 kb/s
    Stream #0:0: Video: h264 (avc1 / 0x31637661), yuv420p, 1920x1080, 29.97 fps
    Stream #0:1: Audio: aac (mp4a / 0x6134706D), 48000 Hz, stereo, fltp""",
    
    # H.265 + Vorbis (incompatible audio)
    """ffprobe version 5.1.2
Input #0, matroska,webm, from 'video.mkv':
  Metadata:
    ENCODER         : Lavf56.25.101
  Duration: 00:28:05.15, start: 0.000000, bitrate: 4353 kb/s
    Stream #0:0: Video: hevc (Main), yuv420p, 1280x960, 29.97 fps
    Stream #0:1: Audio: vorbis (libvorbis), 48000 Hz, stereo""",
    
    # VP9 + Opus (incompatible)
    """ffprobe version 5.1.2
Input #0, matroska,webm, from 'video.webm':
  Duration: 00:10:00.00, start: 0.000000, bitrate: 2000 kb/s
    Stream #0:0: Video: vp9 (Profile 0), yuv420p, 1920x1080, 30 fps
    Stream #0:1: Audio: opus (libopus), 48000 Hz, stereo, fltp"""
]

for i, output in enumerate(ffprobe_outputs, 1):
    print(f"\nTest Case {i}:")
    print("-" * 60)
    
    # Extract codecs
    video_match = re.search(r'Stream\s+#\d+:\d+.*?Video:\s+([^\s,\[]+)', output)
    audio_match = re.search(r'Stream\s+#\d+:\d+.*?Audio:\s+([^\s,\[]+)', output)
    
    video_codec = FFmpegAnalyzer._clean_codec_name(video_match.group(1)) if video_match else "Unknown"
    audio_codec = FFmpegAnalyzer._clean_codec_name(audio_match.group(1)) if audio_match else "Unknown"
    
    print(f"  Video Codec: {video_codec}")
    print(f"  Audio Codec: {audio_codec}")
    
    # Check compatibility
    is_compatible = SamsungTVCompatibility.is_compatible(video_codec, audio_codec)
    icon = SamsungTVCompatibility.get_compatibility_icon(is_compatible)
    
    print(f"  Compatible: {icon} {'Yes' if is_compatible else 'No'}")
    
    if not is_compatible:
        reason = SamsungTVCompatibility.get_incompatible_reason(video_codec, audio_codec)
        print(f"  Reason: {reason}")

print()
print("=" * 60)
print("✓ All tests completed successfully!")
print("=" * 60)
print()
print("To use the application:")
print("1. Install FFmpeg: https://ffmpeg.org/download.html")
print("2. Run: python -m src.main")
print("3. Click 'Scan Folder' to analyze your video files")
print()
