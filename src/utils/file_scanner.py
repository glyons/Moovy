"""File scanner for recursively finding video files in folders."""

import os
from pathlib import Path
from typing import List, Callable, Optional
from .ffmpeg_analyzer import FFmpegAnalyzer


class FileScanner:
    """Recursively scans folders for video files."""

    @staticmethod
    def scan_folder(folder_path: str, on_file_found: Optional[Callable[[str], None]] = None) -> List[str]:
        """Recursively scan folder for video files.
        
        Args:
            folder_path: Root folder path to scan
            on_file_found: Optional callback function called for each file found
            
        Returns:
            List of full paths to video files found
        """
        video_files = []
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            return video_files
        
        if not folder_path.is_dir():
            return video_files
        
        try:
            # Recursively walk through all directories
            for root, dirs, files in os.walk(folder_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in sorted(files):
                    # Skip macOS metadata files (._filename)
                    if file.startswith('._'):
                        continue
                    
                    filepath = os.path.join(root, file)
                    
                    # Check if it's a video file
                    if FFmpegAnalyzer.is_video_file(filepath):
                        video_files.append(filepath)
                        
                        # Call callback if provided
                        if on_file_found:
                            on_file_found(filepath)
        
        except PermissionError:
            pass
        except Exception as e:
            print(f"Error scanning folder: {e}")
        
        return video_files
