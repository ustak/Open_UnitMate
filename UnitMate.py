
import sys
import os
import tempfile
from PyQt6.QtWidgets import QApplication, QMessageBox
from core.utils import is_already_running, create_lock_file, remove_lock_file
from core.config import ConfigManager
from ui.main_window import MainWindow

def main():
    # Lock file path
    lock_file_path = os.path.join(tempfile.gettempdir(), 'unit_converter_app.lock')

    # Check for existing instance
    if is_already_running(lock_file_path):
        app = QApplication(sys.argv)
        QMessageBox.warning(None, "程序已运行", "单位转换器已经在运行中。\n请在系统托盘中找到它的图标。")
        sys.exit(0)

    create_lock_file(lock_file_path)
    
    try:
        app = QApplication(sys.argv)
        
        # Prevent app from exiting when window is closed (because of tray icon)
        app.setQuitOnLastWindowClosed(False)
        
        # Load Config
        config = ConfigManager()
        
        # Create and Show Main Window
        window = MainWindow(config)
        window.show()
        
        sys.exit(app.exec())
    finally:
        remove_lock_file(lock_file_path)

if __name__ == "__main__":
    main()