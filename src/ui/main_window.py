"""Main application window UI."""

import os
import sys
import threading
import platform
import subprocess
import string
from pathlib import Path
from typing import Optional, List

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QFileDialog,
    QMenu, QMessageBox, QLabel, QProgressBar, QDialog,
    QLineEdit, QMenuBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject, QSize
from PyQt6.QtGui import QIcon, QFont, QAction

from src.models.movie import Movie
from src.utils.ffmpeg_analyzer import FFmpegAnalyzer
from src.utils.samsung_compatibility import SamsungTVCompatibility
from src.utils.file_scanner import FileScanner


class CodecWorker(QObject):
    """Worker thread for analyzing video codecs."""
    
    finished = pyqtSignal()
    progress = pyqtSignal(Movie)
    error = pyqtSignal(str)
    
    def __init__(self, movies: List[Movie]):
        """Initialize worker.
        
        Args:
            movies: List of Movie objects to analyze
        """
        super().__init__()
        self.movies = movies
    
    def run(self):
        """Run codec analysis for all movies."""
        try:
            for movie in self.movies:
                movie.is_analyzing = True
                
                # Get codec information
                codec_info = FFmpegAnalyzer.get_codec_info(movie.filepath)
                
                if codec_info:
                    movie.video_codec = codec_info["video_codec"]
                    movie.audio_codec = codec_info["audio_codec"]
                    
                    # Check Samsung TV compatibility
                    movie.is_compatible = SamsungTVCompatibility.is_compatible(
                        movie.video_codec, movie.audio_codec
                    )
                else:
                    movie.error = "Failed to analyze codec information"
                
                movie.is_analyzing = False
                self.progress.emit(movie)
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(f"Analysis error: {str(e)}")


class ScanWorker(QObject):
    """Worker thread for scanning folders."""
    
    file_found = pyqtSignal(str)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, folder_path: str):
        """Initialize scanner.
        
        Args:
            folder_path: Path to folder to scan
        """
        super().__init__()
        self.folder_path = folder_path
        self.cancelled = False
    
    def cancel(self):
        """Cancel the scan operation."""
        self.cancelled = True
    
    def run(self):
        """Run folder scan."""
        try:
            if self.cancelled:
                self.finished.emit([])
                return
            
            video_files = FileScanner.scan_folder(
                self.folder_path,
                on_file_found=lambda f: self.file_found.emit(f) if not self.cancelled else None
            )
            
            if not self.cancelled:
                self.finished.emit(video_files)
            else:
                self.finished.emit([])
        except Exception as e:
            if not self.cancelled:
                self.error.emit(f"Scan error: {str(e)}")


class BatchConversionWorker(QObject):
    """Worker thread for batch converting multiple videos."""
    
    progress = pyqtSignal(int, str)  # (current_file, total_files, filename)
    file_finished = pyqtSignal(str, bool)  # (filename, success)
    finished = pyqtSignal(int, int)  # (succeeded, failed)
    error = pyqtSignal(str)
    
    def __init__(self, movies: List[Movie], output_dir: str):
        """Initialize batch conversion worker.
        
        Args:
            movies: List of incompatible Movie objects to convert
            output_dir: Directory to save converted files
        """
        super().__init__()
        self.movies = movies
        self.output_dir = output_dir
        self.succeeded = 0
        self.failed = 0
    
    def run(self):
        """Run batch conversion."""
        try:
            total = len(self.movies)
            
            for idx, movie in enumerate(self.movies):
                current = idx + 1
                self.progress.emit(current, total)
                
                try:
                    # Generate output filename
                    input_path = Path(movie.filepath)
                    output_filename = input_path.with_stem(input_path.stem + "_converted").name
                    output_path = os.path.join(self.output_dir, output_filename)
                    
                    # Handle duplicate filenames
                    counter = 1
                    base_output = output_path
                    while os.path.exists(output_path):
                        output_path = os.path.join(
                            self.output_dir,
                            input_path.with_stem(
                                f"{input_path.stem}_converted_{counter}"
                            ).name
                        )
                        counter += 1
                    
                    # Perform conversion
                    success = FFmpegAnalyzer.convert_to_compatible_format(
                        movie.filepath,
                        output_path
                    )
                    
                    if success:
                        self.succeeded += 1
                        self.file_finished.emit(movie.filename, True)
                    else:
                        self.failed += 1
                        self.file_finished.emit(movie.filename, False)
                
                except Exception as e:
                    self.failed += 1
                    self.file_finished.emit(movie.filename, False)
            
            self.finished.emit(self.succeeded, self.failed)
        
        except Exception as e:
            self.error.emit(f"Batch conversion error: {str(e)}")


class ConversionDialog(QDialog):
    """Dialog for converting video to compatible format."""
    
    def __init__(self, parent, input_file: str):
        """Initialize conversion dialog.
        
        Args:
            parent: Parent widget
            input_file: Path to input video file
        """
        super().__init__(parent)
        self.input_file = input_file
        self.output_file = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI elements."""
        self.setWindowTitle("Convert to Samsung TV Compatible Format")
        self.setGeometry(100, 100, 500, 150)
        
        layout = QVBoxLayout()
        
        # Input file display
        input_label = QLabel(f"Input: {os.path.basename(self.input_file)}")
        layout.addWidget(input_label)
        
        # Output file selection
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Output file:"))
        self.output_input = QLineEdit()
        
        # Suggest output filename
        input_path = Path(self.input_file)
        suggested_output = input_path.with_stem(input_path.stem + "_converted").with_suffix(".mp4")
        self.output_input.setText(str(suggested_output))
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_output)
        
        output_layout.addWidget(self.output_input)
        output_layout.addWidget(browse_btn)
        layout.addLayout(output_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Buttons
        button_layout = QHBoxLayout()
        convert_btn = QPushButton("Convert")
        convert_btn.clicked.connect(self.start_conversion)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(convert_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Apply background design
        bg_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'src', 'icons', 'bg.jpg'
        )
        if os.path.exists(bg_path):
            self.setStyleSheet(f"""
                QDialog {{
                    background-image: url('{bg_path.replace(chr(92), '/')}'');
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
            """)
    
    def browse_output(self):
        """Open file browser to select output file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Converted Video As",
            str(Path(self.input_file).parent),
            "MP4 Files (*.mp4);;All Files (*)"
        )
        if file_path:
            self.output_input.setText(file_path)
    
    def start_conversion(self):
        """Start video conversion."""
        self.output_file = self.output_input.text()
        
        if not self.output_file:
            QMessageBox.warning(self, "Warning", "Please specify an output file.")
            return
        
        if os.path.exists(self.output_file):
            reply = QMessageBox.question(
                self,
                "File Exists",
                f"Output file already exists. Overwrite?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Run conversion in background thread
        def convert():
            success = FFmpegAnalyzer.convert_to_compatible_format(
                self.input_file,
                self.output_file
            )
            
            if success:
                QMessageBox.information(
                    self,
                    "Success",
                    f"Video converted successfully!\n{self.output_file}"
                )
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Failed to convert video. Check that FFmpeg is installed and the file is valid."
                )
        
        thread = threading.Thread(target=convert)
        thread.daemon = True
        thread.start()


class AboutDialog(QDialog):
    """About dialog for the application."""
    
    def __init__(self, parent=None):
        """Initialize about dialog.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle("About Moovy")
        self.setGeometry(300, 300, 500, 400)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("🐄 Moovy - Movie Codec Analyzer")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Version and info
        info_text = QLabel(
            "Version: 1.0.0\n\n"
            "A desktop application for analyzing video files and checking\n"
            "Samsung TV compatibility.\n\n"
            "Features:\n"
            "  • Recursive folder and drive scanning\n"
            "  • FFmpeg-based codec detection\n"
            "  • Samsung TV compatibility checking\n"
            "  • Batch file conversion\n"
            "  • Multi-threaded analysis\n\n"
            "Supported Formats:\n"
            "  • Video: H.264, H.265, VP9, and many more\n"
            "  • Audio: AAC, MP3, AC3, EAC3, FLAC, PCM\n\n"
            "Tech Stack:\n"
            "  • Python 3.13\n"
            "  • PyQt6 for GUI\n"
            "  • FFmpeg for codec detection\n\n"
            "Developer: Gavin Lyons\n"
            "License: MIT\n"
            "Copyright: © 2026 Gavin Lyons"
        )
        layout.addWidget(info_text)
        
        # OK Button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        
        self.setLayout(layout)
        
        # Apply background design
        bg_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'src', 'icons', 'bg.jpg'
        )
        if os.path.exists(bg_path):
            self.setStyleSheet(f"""
                QDialog {{
                    background-image: url('{bg_path.replace(chr(92), '/')}'');
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
            """)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        self.movies: List[Movie] = []
        self.ffmpeg_path = None
        self.ffmpeg_available = self._check_ffmpeg()
        self.scan_worker = None
        self.scan_thread = None
        self.cancel_btn = None
        self.init_ui()
        
        # Set application icon
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'src', 'icons', 'icon_256.png'
        )
        if os.path.exists(icon_path):
            from PyQt6.QtGui import QIcon as PyQtIcon
            self.setWindowIcon(PyQtIcon(icon_path))
        
        if not self.ffmpeg_available:
            QMessageBox.warning(
                self,
                "FFmpeg Not Found",
                "⚠️  FFmpeg/FFprobe could not be found.\n\n"
                "The application needs FFmpeg to analyze video codecs.\n\n"
                "Install FFmpeg using one of these methods:\n\n"
                "Windows:\n"
                "  • Winget: winget install ffmpeg\n"
                "  • Chocolatey: choco install ffmpeg\n"
                "  • Scoop: scoop install ffmpeg\n"
                "  • Manual: https://ffmpeg.org/download.html\n\n"
                "macOS:\n"
                "  • Homebrew: brew install ffmpeg\n\n"
                "Linux:\n"
                "  • Ubuntu: sudo apt-get install ffmpeg\n"
                "  • Fedora: sudo dnf install ffmpeg\n"
                "  • Arch: sudo pacman -S ffmpeg\n\n"
                "After installing, restart this application."
            )
    
    def _check_ffmpeg(self) -> bool:
        """Check if FFmpeg/FFprobe is available in PATH.
        
        Returns:
            True if ffprobe is available, False otherwise
        """
        try:
            ffprobe_path = FFmpegAnalyzer._find_ffprobe()
            if ffprobe_path:
                self.ffmpeg_path = ffprobe_path
                return True
            return False
        except Exception:
            return False
    
    def init_ui(self):
        """Initialize UI elements."""
        self.setWindowTitle("Moovy - Movie Codec Analyzer")
        self.setGeometry(100, 100, 1000, 700)
        
        # Helper for getting icon paths
        def get_icon_path(filename):
            return os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'src', 'icons', filename
            )
        
        # Create menu bar
        menubar = self.menuBar()
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        # Rescan Codecs action
        rescan_action = QAction("Rescan Codecs", self)
        rescan_action.setToolTip("Re-analyze codecs for all files")
        icon_path = get_icon_path('btn_reload.png')
        if os.path.exists(icon_path):
            rescan_action.setIcon(QIcon(icon_path))
        rescan_action.triggered.connect(self.reload_codecs)
        tools_menu.addAction(rescan_action)
        
        # Batch Convert action
        batch_action = QAction("Batch Convert", self)
        batch_action.setToolTip("Batch convert all incompatible files")
        icon_path = get_icon_path('btn_batch_convert.png')
        if os.path.exists(icon_path):
            batch_action.setIcon(QIcon(icon_path))
        batch_action.triggered.connect(self.batch_convert_incompatible)
        tools_menu.addAction(batch_action)
        
        # About menu
        about_menu = menubar.addMenu("About")
        
        about_action = QAction("About Moovy", self)
        about_action.triggered.connect(self.show_about)
        about_menu.addAction(about_action)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Toolbar with scan buttons
        toolbar_layout = QHBoxLayout()
        
        # Scan Folder Button with text
        scan_folder_container = QWidget()
        scan_folder_vbox = QVBoxLayout()
        scan_folder_vbox.setContentsMargins(0, 0, 0, 0)
        scan_folder_vbox.setSpacing(2)
        
        scan_btn = QPushButton()
        scan_icon_path = get_icon_path('btn_scan_folder.png')
        if os.path.exists(scan_icon_path):
            from PyQt6.QtGui import QIcon as PyQtIcon
            scan_btn.setIcon(PyQtIcon(scan_icon_path))
            scan_btn.setIconSize(QSize(32, 32))
        else:
            scan_btn.setText("Scan")
        scan_btn.setToolTip("Scan a folder for video files (Recursive)")
        scan_btn.setFixedSize(40, 40)
        scan_btn.clicked.connect(self.scan_folder)
        scan_btn.setFlat(True)
        
        scan_label = QLabel("Scan")
        scan_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scan_label.setStyleSheet("font-size: 9px;")
        
        scan_folder_vbox.addWidget(scan_btn)
        scan_folder_vbox.addWidget(scan_label)
        scan_folder_container.setLayout(scan_folder_vbox)
        
        # Status label with FFmpeg status
        ffmpeg_status = "✓ FFmpeg Ready" if self.ffmpeg_available else "❌ FFmpeg Not Found"
        self.status_label = QLabel(f"Ready - {ffmpeg_status}")
        
        # Cancel Scan Button (hidden by default)
        self.cancel_btn = QPushButton("Cancel Scan")
        self.cancel_btn.setToolTip("Cancel the current scan operation")
        self.cancel_btn.setFixedSize(100, 40)
        self.cancel_btn.clicked.connect(self.cancel_scan)
        self.cancel_btn.setVisible(False)
        self.cancel_btn.setStyleSheet("QPushButton { background-color: #ff6b6b; color: white; font-weight: bold; }")
        
        toolbar_layout.addWidget(scan_folder_container)
        toolbar_layout.addWidget(self.cancel_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.status_label)
        
        layout.addLayout(toolbar_layout)
        
        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "File Name",
            "Video Codec",
            "Audio Codec",
            "Samsung TV Compatible",
            "Details"
        ])
        
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        self.table.doubleClicked.connect(self.on_table_double_click)
        
        # Set column widths
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 200)
        
        layout.addWidget(self.table)
        
        central_widget.setLayout(layout)
        
        # Add background to central widget
        bg_path = get_icon_path('bg.jpg')
        if os.path.exists(bg_path):
            central_widget.setStyleSheet(f"""
                QWidget {{
                    background-image: url('{bg_path.replace(chr(92), '/')}'');
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                QTableWidget {{
                    background-color: rgba(255, 255, 255, 0.95);
                }}
            """)
    
    def scan_folder(self):
        """Open folder selection dialog and scan for video files."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Scan")
        
        if not folder:
            return
        
        self.status_label.setText("Scanning folder...")
        self.table.setRowCount(0)
        self.movies.clear()
        self.cancel_btn.setVisible(True)
        
        # Create and run scanner thread
        self.scan_thread = QThread()
        self.scan_worker = ScanWorker(folder)
        self.scan_worker.moveToThread(self.scan_thread)
        
        self.scan_thread.started.connect(self.scan_worker.run)
        self.scan_worker.file_found.connect(self.on_file_found)
        self.scan_worker.finished.connect(self.on_scan_finished)
        self.scan_worker.error.connect(self.on_scan_error)
        
        self.scan_thread.start()
    
    def scan_drive(self):
        """Scan entire drive for video files."""
        # Get list of available drives
        drives = self._get_available_drives()
        
        if not drives:
            QMessageBox.warning(self, "No Drives", "Could not detect any drives.")
            return
        
        # Create selection dialog
        if len(drives) == 1:
            selected_drive = drives[0]
        else:
            # Simple selection dialog
            items = [f"{drive} ({self._get_drive_name(drive)})" for drive in drives]
            from PyQt6.QtWidgets import QInputDialog
            item, ok = QInputDialog.getItem(
                self,
                "Select Drive to Scan",
                "Choose drive:",
                items,
                0,
                False
            )
            if not ok:
                return
            selected_drive = drives[items.index(item)]
        
        # Warn user about scan time
        reply = QMessageBox.question(
            self,
            "Confirm Drive Scan",
            f"You are about to scan the entire drive: {selected_drive}\n\n"
            "This may take a while depending on the drive size.\n\n"
            "Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        self.status_label.setText(f"Scanning drive {selected_drive}...")
        self.table.setRowCount(0)
        self.movies.clear()
        self.cancel_btn.setVisible(True)
        
        # Create and run scanner thread
        self.scan_thread = QThread()
        self.scan_worker = ScanWorker(selected_drive)
        self.scan_worker.moveToThread(self.scan_thread)
        
        self.scan_thread.started.connect(self.scan_worker.run)
        self.scan_worker.file_found.connect(self.on_file_found)
        self.scan_worker.finished.connect(self.on_scan_finished)
        self.scan_worker.error.connect(self.on_scan_error)
        
        self.scan_thread.start()
    
    def _get_available_drives(self) -> List[str]:
        """Get list of available drives on the system.
        
        Returns:
            List of drive paths
        """
        drives = []
        
        if sys.platform == "win32":
            # Windows: check all drive letters
            import string
            for letter in string.ascii_uppercase:
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    drives.append(drive)
        else:
            # macOS/Linux: common mount points
            mount_points = [
                "/",
                "/home",
                "/mnt",
                "/media",
                "/Volumes",
            ]
            for point in mount_points:
                if os.path.exists(point):
                    drives.append(point)
        
        return drives
    
    def _get_drive_name(self, drive: str) -> str:
        """Get drive name/label.
        
        Args:
            drive: Drive path
            
        Returns:
            Drive name or size info
        """
        try:
            if sys.platform == "win32":
                import subprocess
                result = subprocess.run(
                    ["wmic", "logicaldisk", "get", "name,size", "/format:list"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                for line in result.stdout.split('\n'):
                    if drive[0] in line:
                        return drive
            return drive
        except Exception:
            return drive
    
    def on_file_found(self, filepath: str):
        """Handle file found during scan.
        
        Args:
            filepath: Path to found video file
        """
        movie = Movie(filepath)
        self.movies.append(movie)
        
        # Add row to table
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # File name
        filename_item = QTableWidgetItem(movie.filename)
        self.table.setItem(row, 0, filename_item)
        
        # Placeholder for other columns
        for col in range(1, 5):
            self.table.setItem(row, col, QTableWidgetItem("Analyzing..."))
    
    def on_scan_finished(self, video_files: List[str]):
        """Handle scan completion.
        
        Args:
            video_files: List of found video files
        """
        self.scan_thread.quit()
        self.scan_thread.wait()
        self.cancel_btn.setVisible(False)
        
        if not video_files:
            self.status_label.setText("No video files found in the selected folder.")
            return
        
        if not self.ffmpeg_available:
            QMessageBox.critical(
                self,
                "FFmpeg Not Available",
                "FFmpeg is required to analyze video codecs.\n\n"
                "Please install FFmpeg and restart the application."
            )
            self.status_label.setText("Ready (FFmpeg required)")
            return
        
        self.status_label.setText(f"Found {len(video_files)} video files. Analyzing codecs...")
        
        # Start codec analysis
        self.analyze_codecs()
    
    def on_scan_error(self, error_msg: str):
        """Handle scan error.
        
        Args:
            error_msg: Error message
        """
        self.scan_thread.quit()
        self.scan_thread.wait()
        self.cancel_btn.setVisible(False)
        QMessageBox.critical(self, "Scan Error", error_msg)
        self.status_label.setText("Ready")
    
    def analyze_codecs(self):
        """Analyze codecs for all movies."""
        # Create and run analyzer thread
        self.codec_thread = QThread()
        self.codec_worker = CodecWorker(self.movies)
        self.codec_worker.moveToThread(self.codec_thread)
        
        self.codec_thread.started.connect(self.codec_worker.run)
        self.codec_worker.progress.connect(self.on_codec_analyzed)
        self.codec_worker.finished.connect(self.on_analysis_finished)
        self.codec_worker.error.connect(self.on_analysis_error)
        
        self.codec_thread.start()
    
    def on_codec_analyzed(self, movie: Movie):
        """Handle codec analysis for a single movie.
        
        Args:
            movie: Analyzed Movie object
        """
        # Find and update the row
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() == movie.filename:
                # Video codec
                self.table.setItem(row, 1, QTableWidgetItem(movie.video_codec or "N/A"))
                
                # Audio codec
                self.table.setItem(row, 2, QTableWidgetItem(movie.audio_codec or "N/A"))
                
                # Compatibility icon
                compat_symbol = SamsungTVCompatibility.get_compatibility_icon(movie.is_compatible)
                compat_item = QTableWidgetItem(compat_symbol)
                compat_item.setFont(QFont("Arial", 14, QFont.Weight.Bold))
                
                if movie.is_compatible:
                    compat_item.setForeground(Qt.GlobalColor.green)
                else:
                    compat_item.setForeground(Qt.GlobalColor.red)
                
                self.table.setItem(row, 3, compat_item)
                
                # Details
                if not movie.is_compatible:
                    reason = SamsungTVCompatibility.get_incompatible_reason(
                        movie.video_codec, movie.audio_codec
                    )
                    self.table.setItem(row, 4, QTableWidgetItem(reason))
                else:
                    self.table.setItem(row, 4, QTableWidgetItem("Compatible"))
                
                break
    
    def on_analysis_finished(self):
        """Handle analysis completion."""
        self.codec_thread.quit()
        self.codec_thread.wait()
        
        compatible_count = sum(1 for m in self.movies if m.is_compatible)
        self.status_label.setText(
            f"Analysis complete: {compatible_count}/{len(self.movies)} compatible"
        )
    
    def on_analysis_error(self, error_msg: str):
        """Handle analysis error.
        
        Args:
            error_msg: Error message
        """
        self.codec_thread.quit()
        self.codec_thread.wait()
        QMessageBox.critical(self, "Analysis Error", error_msg)
        self.status_label.setText("Ready")
    
    def show_context_menu(self, position):
        """Show context menu for table items.
        
        Args:
            position: Position where menu was requested
        """
        item = self.table.itemAt(position)
        if not item:
            return
        
        row = item.row()
        if row < 0 or row >= len(self.movies):
            return
        
        movie = self.movies[row]
        
        menu = QMenu(self)
        
        if not movie.is_compatible:
            convert_action = menu.addAction("Convert to Compatible Format (H.264 + AAC)")
            convert_action.triggered.connect(lambda: self.convert_movie(movie))
        
        menu.addSeparator()
        
        open_action = menu.addAction("Open File Location")
        open_action.triggered.connect(lambda: self.open_file_location(movie))
        
        menu.addSeparator()
        
        info_action = menu.addAction("View Full Details")
        info_action.triggered.connect(lambda: self.show_movie_details(movie))
        
        menu.exec(self.table.mapToGlobal(position))
    
    def on_table_double_click(self, index):
        """Handle double-click on table row to launch movie.
        
        Args:
            index: QModelIndex of clicked item
        """
        row = index.row()
        if row < 0 or row >= len(self.movies):
            return
        
        movie = self.movies[row]
        self.launch_movie(movie)
    
    def launch_movie(self, movie: Movie):
        """Launch/open a movie file with default media player.
        
        Args:
            movie: Movie to launch
        """
        try:
            if not os.path.exists(movie.filepath):
                QMessageBox.warning(
                    self,
                    "File Not Found",
                    f"The file could not be found:\n{movie.filepath}"
                )
                return
            
            # Platform-specific file opening
            if sys.platform == "win32":
                os.startfile(movie.filepath)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", movie.filepath])
            else:
                subprocess.Popen(["xdg-open", movie.filepath])
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Could not launch movie:\n{str(e)}"
            )
    
    def convert_movie(self, movie: Movie):
        """Show conversion dialog for a movie.
        
        Args:
            movie: Movie to convert
        """
        dialog = ConversionDialog(self, movie.filepath)
        dialog.exec()
    
    def open_file_location(self, movie: Movie):
        """Open file location in file explorer.
        
        Args:
            movie: Movie whose location to open
        """
        folder = os.path.dirname(movie.filepath)
        if os.path.exists(folder):
            if sys.platform == "win32":
                os.startfile(folder)
            elif sys.platform == "darwin":
                # macOS
                subprocess.Popen(["open", folder])
            else:
                # Linux and other Unix-based systems
                subprocess.Popen(["xdg-open", folder])
    
    def show_movie_details(self, movie: Movie):
        """Show detailed information about a movie.
        
        Args:
            movie: Movie to show details for
        """
        details = f"""
File: {movie.filename}
Path: {movie.filepath}

Video Codec: {movie.video_codec or 'N/A'}
Audio Codec: {movie.audio_codec or 'N/A'}

Samsung TV Compatible: {'Yes ✓' if movie.is_compatible else 'No ✗'}

"""
        if not movie.is_compatible:
            reason = SamsungTVCompatibility.get_incompatible_reason(
                movie.video_codec, movie.audio_codec
            )
            details += f"Issue: {reason}"
        
        QMessageBox.information(self, "Movie Details", details)
    
    def reload_codecs(self):
        """Reload codec analysis for all movies."""
        if not self.movies:
            QMessageBox.information(self, "Info", "No movies loaded. Please scan a folder first.")
            return
        
        self.status_label.setText("Reloading codec information...")
        self.analyze_codecs()
    
    def batch_convert_incompatible(self):
        """Convert all incompatible files in batch."""
        # Get incompatible movies
        incompatible_movies = [m for m in self.movies if not m.is_compatible]
        
        if not incompatible_movies:
            QMessageBox.information(
                self,
                "No Incompatible Files",
                "All files in the current list are compatible with Samsung TV."
            )
            return
        
        # Ask for output directory
        output_dir = QFileDialog.getExistingDirectory(
            self,
            f"Select Output Folder for {len(incompatible_movies)} Conversions",
            str(Path.home())
        )
        
        if not output_dir:
            return
        
        # Confirm batch conversion
        reply = QMessageBox.question(
            self,
            "Confirm Batch Conversion",
            f"You are about to convert {len(incompatible_movies)} file(s) to Samsung TV compatible format.\n\n"
            f"Output folder: {output_dir}\n\n"
            "This may take a while depending on file sizes.\n\n"
            "Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Show progress dialog
        progress_dialog = QDialog(self)
        progress_dialog.setWindowTitle("Batch Converting Files")
        progress_dialog.setGeometry(200, 200, 500, 250)
        progress_dialog.setModal(True)
        
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel(f"Converting {len(incompatible_movies)} file(s)...")
        layout.addWidget(title_label)
        
        # Current file label
        current_file_label = QLabel("Starting conversion...")
        layout.addWidget(current_file_label)
        
        # Progress bar
        progress_bar = QProgressBar()
        progress_bar.setMaximum(len(incompatible_movies))
        progress_bar.setValue(0)
        layout.addWidget(progress_bar)
        
        # Status list
        status_text = QLabel("")
        status_text.setStyleSheet("border: 1px solid #ccc; padding: 5px;")
        status_text.setMinimumHeight(100)
        status_text.setWordWrap(True)
        layout.addWidget(status_text)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setEnabled(False)  # Disable during conversion
        layout.addWidget(cancel_btn)
        
        progress_dialog.setLayout(layout)
        
        # Track results
        results_text = ""
        
        # Create and run batch conversion worker
        self.batch_thread = QThread()
        self.batch_worker = BatchConversionWorker(incompatible_movies, output_dir)
        self.batch_worker.moveToThread(self.batch_thread)
        
        def on_progress(current, total):
            """Update progress."""
            progress_bar.setValue(current - 1)
            current_file_label.setText(f"Converting file {current}/{total}...")
        
        def on_file_finished(filename, success):
            """Update file status."""
            nonlocal results_text
            status = "✓ Success" if success else "✗ Failed"
            results_text += f"{filename}: {status}\n"
            status_text.setText(results_text)
            progress_bar.setValue(progress_bar.value() + 1)
        
        def on_finished(succeeded, failed):
            """Conversion finished."""
            self.batch_thread.quit()
            self.batch_thread.wait()
            cancel_btn.setEnabled(True)
            
            current_file_label.setText("Conversion Complete!")
            title_label.setText(f"Results: {succeeded} succeeded, {failed} failed")
            
            if failed == 0:
                cancel_btn.setText("Close")
            else:
                cancel_btn.setText("Close")
            
            self.status_label.setText(
                f"Batch conversion complete: {succeeded} succeeded, {failed} failed"
            )
        
        def on_error(error_msg):
            """Error occurred."""
            self.batch_thread.quit()
            self.batch_thread.wait()
            cancel_btn.setEnabled(True)
            QMessageBox.critical(
                self,
                "Conversion Error",
                f"Error during batch conversion:\n{error_msg}"
            )
            progress_dialog.reject()
        
        self.batch_thread.started.connect(self.batch_worker.run)
        self.batch_worker.progress.connect(on_progress)
        self.batch_worker.file_finished.connect(on_file_finished)
        self.batch_worker.finished.connect(on_finished)
        self.batch_worker.error.connect(on_error)
        cancel_btn.clicked.connect(progress_dialog.reject)
        
        self.batch_thread.start()
        progress_dialog.exec()
    
    def cancel_scan(self):
        """Cancel the current scan operation."""
        if self.scan_worker and not self.scan_worker.cancelled:
            self.scan_worker.cancel()
            self.status_label.setText("Scan cancelled by user")
            self.cancel_btn.setVisible(False)
    
    def show_about(self):
        """Show about dialog."""
        about_dialog = AboutDialog(self)
        about_dialog.exec()
    
    def show_settings(self):
        """Show settings dialog."""
        settings_text = """
Settings

Current Settings:
• FFmpeg Status: """
        ffmpeg_status = "✓ Installed" if self.ffmpeg_available else "✗ Not Found"
        settings_text += ffmpeg_status + "\n"
        settings_text += f"• Files Analyzed: {len(self.movies)}\n"
        
        compatible = sum(1 for m in self.movies if m.is_compatible)
        incompatible = len(self.movies) - compatible
        
        settings_text += f"• Compatible Files: {compatible}\n"
        settings_text += f"• Incompatible Files: {incompatible}\n\n"
        
        settings_text += """
To Use This Application:
1. Ensure FFmpeg is installed
   Windows: winget install ffmpeg
   macOS: brew install ffmpeg
   Linux: sudo apt install ffmpeg

2. Scan folders or drives for video files

3. View codec information in the grid

4. Convert incompatible files as needed

For advanced options, edit the configuration files
in the application folder.
        """
        
        QMessageBox.information(self, "Settings", settings_text)
