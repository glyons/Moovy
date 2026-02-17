"""Samsung TV compatibility checker for video codecs."""

from typing import Tuple


class SamsungTVCompatibility:
    """Checks if a video/audio codec combination is compatible with Samsung TVs."""

    # Compatible video codecs for Samsung TVs
    COMPATIBLE_VIDEO_CODECS = {
        "h264", "avc", "h.264",  # H.264 / AVC
        "h265", "hevc", "h.265"   # H.265 / HEVC
    }

    # Compatible audio codecs for Samsung TVs
    COMPATIBLE_AUDIO_CODECS = {
        "aac",
        "mp3",
        "ac3",
        "eac3",
        "flac",
        "pcm"
    }

    @staticmethod
    def normalize_codec_name(codec: str) -> str:
        """Normalize codec name for comparison.
        
        Args:
            codec: Codec name from FFmpeg
            
        Returns:
            Normalized codec name (lowercase, cleanup)
        """
        if not codec:
            return ""
        
        # Clean up and normalize codec names
        codec_lower = codec.lower().strip()
        
        # Handle specific cases
        replacements = {
            "mpeg2video": "mpeg2",
            "libx264": "h264",
            "libx265": "h265",
            "libfdk_aac": "aac",
        }
        
        for old, new in replacements.items():
            if codec_lower.startswith(old):
                codec_lower = codec_lower.replace(old, new)
        
        return codec_lower

    @staticmethod
    def is_compatible(video_codec: str, audio_codec: str) -> bool:
        """Check if video and audio codec combination is Samsung TV compatible.
        
        Args:
            video_codec: Video codec name from FFmpeg
            audio_codec: Audio codec name from FFmpeg
            
        Returns:
            True if both codecs are compatible for Samsung TV
        """
        # Normalize codec names
        video_normalized = SamsungTVCompatibility.normalize_codec_name(video_codec)
        audio_normalized = SamsungTVCompatibility.normalize_codec_name(audio_codec)
        
        # Check video codec
        video_compatible = any(
            compat in video_normalized 
            for compat in SamsungTVCompatibility.COMPATIBLE_VIDEO_CODECS
        )
        
        # Check audio codec
        audio_compatible = audio_normalized in SamsungTVCompatibility.COMPATIBLE_AUDIO_CODECS
        
        return video_compatible and audio_compatible

    @staticmethod
    def get_compatibility_icon(is_compatible: bool) -> str:
        """Get compatibility icon/symbol.
        
        Args:
            is_compatible: Whether the file is compatible
            
        Returns:
            ✓ for compatible, ✗ for incompatible
        """
        return "✓" if is_compatible else "✗"

    @staticmethod
    def get_incompatible_reason(video_codec: str, audio_codec: str) -> str:
        """Get reason why a file is not compatible.
        
        Args:
            video_codec: Video codec name
            audio_codec: Audio codec name
            
        Returns:
            String describing incompatibility
        """
        video_normalized = SamsungTVCompatibility.normalize_codec_name(video_codec)
        audio_normalized = SamsungTVCompatibility.normalize_codec_name(audio_codec)
        
        reasons = []
        
        # Check video codec
        video_compatible = any(
            compat in video_normalized 
            for compat in SamsungTVCompatibility.COMPATIBLE_VIDEO_CODECS
        )
        if not video_compatible:
            reasons.append(f"Video codec '{video_codec}' not compatible")
        
        # Check audio codec
        audio_compatible = audio_normalized in SamsungTVCompatibility.COMPATIBLE_AUDIO_CODECS
        if not audio_compatible:
            reasons.append(f"Audio codec '{audio_codec}' not compatible")
        
        return "; ".join(reasons) if reasons else "Unknown issue"
