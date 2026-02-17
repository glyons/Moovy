"""Movie data model."""


class Movie:
    """Represents a movie file with codec information."""

    def __init__(self, filepath: str):
        """Initialize a movie object.
        
        Args:
            filepath: Full path to the movie file
        """
        self.filepath = filepath
        self.filename = filepath.split("\\")[-1] if "\\" in filepath else filepath.split("/")[-1]
        self.video_codec = None
        self.audio_codec = None
        self.is_compatible = False
        self.is_analyzing = False
        self.error = None

    def __repr__(self) -> str:
        """String representation of the movie."""
        return f"Movie(filename='{self.filename}', video={self.video_codec}, audio={self.audio_codec})"
