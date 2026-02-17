"""FFmpeg analyzer for extracting codec information from video files."""

import subprocess
import json
import re
import logging
import shutil
import sys
import os
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class FFmpegAnalyzer:
    """Analyzes media files using FFmpeg to extract codec information."""

    # Common video file extensions
    VIDEO_EXTENSIONS = {
        ".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm",
        ".m4v", ".mpg", ".mpeg", ".3gp", ".ogv", ".ts", ".m2ts",
        ".mts", ".vob", ".f4v", ".asf", ".rm", ".rmvb", ".m3u8"
    }
    
    _ffprobe_path = None  # Cached path to ffprobe
    
    @staticmethod
    def _find_ffprobe() -> Optional[str]:
        """Find ffprobe executable in PATH or common locations.
        
        Returns:
            Path to ffprobe executable, or None if not found
        """
        # Check if already cached
        if FFmpegAnalyzer._ffprobe_path:
            return FFmpegAnalyzer._ffprobe_path
        
        # Try to find ffprobe in PATH using shutil
        ffprobe_in_path = shutil.which("ffprobe")
        if ffprobe_in_path:
            logger.info(f"Found ffprobe in PATH: {ffprobe_in_path}")
            FFmpegAnalyzer._ffprobe_path = ffprobe_in_path
            return ffprobe_in_path
        
        # If not in PATH, check common installation locations
        common_paths = []
        
        if sys.platform == "win32":
            # Windows common locations
            localappdata = os.environ.get("LOCALAPPDATA", "")
            if localappdata:
                common_paths.append(os.path.join(localappdata, "Microsoft", "WinGet", "Links", "ffprobe.exe"))
            
            common_paths.extend([
                r"C:\Program Files\ffmpeg\bin\ffprobe.exe",
                r"C:\Program Files (x86)\ffmpeg\bin\ffprobe.exe",
                r"C:\FFmpeg\bin\ffprobe.exe",
                r"C:\tools\ffmpeg\bin\ffprobe.exe",
            ])
        elif sys.platform == "darwin":
            # macOS common locations
            common_paths = [
                "/usr/local/bin/ffprobe",
                "/opt/homebrew/bin/ffprobe",
                "/usr/bin/ffprobe",
            ]
        else:
            # Linux common locations
            common_paths = [
                "/usr/bin/ffprobe",
                "/usr/local/bin/ffprobe",
                "/bin/ffprobe",
            ]
        
        for path in common_paths:
            try:
                # Test if the path works
                result = subprocess.run(
                    [path, "-version"],
                    capture_output=True,
                    timeout=3
                )
                if result.returncode == 0:
                    logger.info(f"Found ffprobe at: {path}")
                    FFmpegAnalyzer._ffprobe_path = path
                    return path
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        logger.error("ffprobe not found in PATH or common locations")
        return None

    @staticmethod
    def is_video_file(filepath: str) -> bool:
        """Check if file is a video file based on extension.
        
        Args:
            filepath: Path to the file
            
        Returns:
            True if file extension matches known video formats
        """
        extension = filepath[filepath.rfind("."):].lower()
        return extension in FFmpegAnalyzer.VIDEO_EXTENSIONS

    @staticmethod
    def get_codec_info(filepath: str) -> Optional[Dict[str, Any]]:
        """Extract codec information from a video file using FFprobe.
        
        Args:
            filepath: Path to the video file
            
        Returns:
            Dictionary with 'video_codec' and 'audio_codec' keys, or None if error
        """
        # Find ffprobe executable
        ffprobe_path = FFmpegAnalyzer._find_ffprobe()
        if not ffprobe_path:
            logger.error("FFprobe not found. Ensure FFmpeg is installed and in PATH.")
            return None
        
        try:
            # Run ffprobe to get full output
            cmd = [ffprobe_path, filepath]
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            # Combine stdout and stderr (ffprobe outputs to both)
            output = result.stdout + result.stderr
            
            video_codec = "Unknown"
            audio_codec = "Unknown"
            
            # Parse output for video codec
            # Look for lines like "Stream #0:0: Video: h264 ..." or "Stream #0:0: Video: h.264 ..."
            video_match = re.search(
                r'Stream\s+#\d+:\d+.*?Video:\s+([^\s,\[]+)',
                output
            )
            if video_match:
                video_codec = video_match.group(1).strip()
                # Clean up codec names
                video_codec = FFmpegAnalyzer._clean_codec_name(video_codec)
            
            # Parse output for audio codec
            # Look for lines like "Stream #0:1: Audio: aac ..." or "Stream #0:1: Audio: vorbis ..."
            audio_match = re.search(
                r'Stream\s+#\d+:\d+.*?Audio:\s+([^\s,\[]+)',
                output
            )
            if audio_match:
                audio_codec = audio_match.group(1).strip()
                # Clean up codec names
                audio_codec = FFmpegAnalyzer._clean_codec_name(audio_codec)
            
            logger.info(f"Analyzed {filepath}: video={video_codec}, audio={audio_codec}")
            
            return {
                "video_codec": video_codec,
                "audio_codec": audio_codec
            }
            
        except subprocess.TimeoutExpired:
            logger.error(f"FFprobe timeout analyzing {filepath}")
            return None
        except Exception as e:
            logger.error(f"Error analyzing {filepath}: {e}")
            return None
    
    @staticmethod
    def _clean_codec_name(codec: str) -> str:
        """Clean up codec name from ffprobe output.
        
        Args:
            codec: Raw codec name from ffprobe
            
        Returns:
            Cleaned codec name
        """
        if not codec:
            return "Unknown"
        
        # Remove parenthetical information (profile, level, etc.)
        codec = codec.split('(')[0].strip()
        
        # Handle common codec name variations
        replacements = {
            "h.264": "h264",
            "aac": "aac",
            "mp3": "mp3",
            "ac-3": "ac3",
            "e-ac-3": "eac3",
            "flac": "flac",
            "pcm": "pcm",
        }
        
        codec_lower = codec.lower()
        for pattern, replacement in replacements.items():
            if codec_lower == pattern:
                return replacement
        
        return codec

    @staticmethod
    def convert_to_compatible_format(input_filepath: str, output_filepath: str, 
                                      on_progress=None) -> bool:
        """Convert video to Samsung TV compatible format (H.264 + AAC).
        
        Args:
            input_filepath: Path to input video file
            output_filepath: Path to output video file
            on_progress: Optional callback function for progress updates
            
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            # Get ffmpeg path (similar logic to ffprobe)
            ffmpeg_path = shutil.which("ffmpeg")
            if not ffmpeg_path:
                logger.error("FFmpeg not found in PATH")
                return False
            
            cmd = [
                ffmpeg_path,
                "-i", input_filepath,
                "-c:v", "libx264",
                "-preset", "medium",
                "-c:a", "aac",
                "-b:a", "128k",
                "-y",
                output_filepath
            ]
            
            # Run conversion
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                logger.info(f"Successfully converted {input_filepath} to {output_filepath}")
                return True
            else:
                logger.error(f"Conversion failed: {stderr}")
                return False
                
        except FileNotFoundError:
            logger.error("FFmpeg not found. Ensure FFmpeg is installed and in PATH.")
            return False
        except Exception as e:
            logger.error(f"Error converting {input_filepath}: {e}")
            return False
