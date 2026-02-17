"""Main entry point for Moovy application."""

import sys
import logging

from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    """Main application entry point."""
    setup_logging()
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
