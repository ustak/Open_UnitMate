
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPlainTextEdit, QLabel, QComboBox, QPushButton, 
                             QGroupBox, QSystemTrayIcon, QMenu, QApplication, 
                             QFrame, QSizePolicy, QDialog, QTabWidget)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QEvent
from PyQt6.QtGui import QIcon, QAction, QPixmap, QColor, QPainter, QClipboard, QCursor, QFont

from core.converter import convert_units
from core.utils import parse_input_text
from core.config import ConfigManager
from ui.styles import STYLESHEET
from ui.calculator import CalculatorWidget

class UnitConverterWidget(QWidget):
    def __init__(self, config: ConfigManager, parent=None):
        super().__init__(parent)
        self.config = config
        self.converted_values = []
        self.converted_full = []
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.clear_status)
        self.init_ui()
        self.load_ui_state()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)



        # Input Section
        input_group = QGroupBox("输入与控制")
        input_layout = QVBoxLayout(input_group)
        
        self.input_edit = QPlainTextEdit()
        self.input_edit.setPlaceholderText("在此粘贴或输入数值...")
        self.input_edit.setFont(QFont("Consolas", 11))
        self.input_edit.setFixedHeight(100)
        input_layout.addWidget(self.input_edit)

        # Controls Row
        controls_layout = QHBoxLayout()
        
        controls_layout.addWidget(QLabel("从:"))
        self.input_unit_combo = QComboBox()
        self.input_unit_combo.addItems(["mm", "um", "inch", "mil"])
        controls_layout.addWidget(self.input_unit_combo)

        self.swap_btn = QPushButton("⇄")
        self.swap_btn.setFixedSize(40, 32)
        self.swap_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.swap_btn.setToolTip("交换单位")
        self.swap_btn.clicked.connect(self.swap_units)
        self.swap_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #BB86FC;
                font-size: 24px;
                border: 1px solid #333333;
                border-radius: 4px;
                padding-bottom: 4px; 
            }
            QPushButton:hover {
                background-color: #2C2C2C;
                border-color: #BB86FC;
            }
        """)
        controls_layout.addWidget(self.swap_btn)

        controls_layout.addWidget(QLabel("转换到:"))
        self.output_unit_combo = QComboBox()
        self.output_unit_combo.addItems(["mil", "mm", "um", "inch"])
        controls_layout.addWidget(self.output_unit_combo)
        
        controls_layout.addSpacing(20)
        controls_layout.addWidget(QLabel("小数位数:"))
        self.decimals_combo = QComboBox()
        self.decimals_combo.addItems(["0", "1", "2", "3"])
        controls_layout.addWidget(self.decimals_combo)
        
        controls_layout.addStretch()
        
        input_layout.addLayout(controls_layout)

        # Action Buttons
        button_layout = QHBoxLayout()
        self.convert_btn = QPushButton("转换")
        self.convert_btn.setProperty("role", "primary")
        self.convert_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.convert_btn.clicked.connect(self.convert)
        
        self.clear_btn = QPushButton("清除")
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_all)
        
        button_layout.addWidget(self.convert_btn)
        button_layout.addWidget(self.clear_btn)
        
        self.copy_val_btn = QPushButton("复制数值")
        self.copy_val_btn.clicked.connect(self.copy_values)
        button_layout.addWidget(self.copy_val_btn)
        
        button_layout.addStretch()
        
        input_layout.addLayout(button_layout)
        main_layout.addWidget(input_group)

        # Result Section
        result_group = QGroupBox("转换结果")
        result_layout = QVBoxLayout(result_group)
        
        self.result_edit = QPlainTextEdit()
        self.result_edit.setFont(QFont("Consolas", 11))
        self.result_edit.setReadOnly(True)
        result_layout.addWidget(self.result_edit)
        
        main_layout.addWidget(result_group)



        # Status Bar
        self.status_label = QLabel("")
        self.status_label.setProperty("role", "status_success")
        main_layout.addWidget(self.status_label)

        # Footer Actions
        footer_layout = QHBoxLayout()

        author_label = QLabel("作者：Kim")
        author_label.setProperty("role", "subtle")
        footer_layout.addWidget(author_label)

        self.help_btn = QPushButton("帮助")
        self.help_btn.setProperty("role", "subtle")
        self.help_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.help_btn.clicked.connect(self.show_help)
        
        footer_layout.addStretch()
        footer_layout.addWidget(self.help_btn)
        
        main_layout.addLayout(footer_layout)

    def load_ui_state(self):
        def_in = self.config.get("default_input_unit")
        def_out = self.config.get("default_output_unit")
        decimals = self.config.get("decimal_places", 2)
        
        self.set_combo_text(self.input_unit_combo, def_in)
        self.set_combo_text(self.output_unit_combo, def_out)
        self.set_combo_text(self.decimals_combo, str(decimals))

    def set_combo_text(self, combo, text):
        index = combo.findText(text)
        if index >= 0:
            combo.setCurrentIndex(index)

    def convert(self):
        input_text = self.input_edit.toPlainText()
        input_matrix = parse_input_text(input_text)
        
        if not input_matrix:
            return

        input_unit = self.input_unit_combo.currentText()
        output_unit = self.output_unit_combo.currentText()
        try:
            decimals = int(self.decimals_combo.currentText())
        except ValueError:
            decimals = 2
            
        # Update config temporarily (or permanently if desired, original did persistent)
        self.config.set("decimal_places", decimals) 
        
        self.converted_values = []
        self.converted_full = []
        
        for row in input_matrix:
            row_vals = []
            row_full = []
            for val in row:
                if val is None:
                    row_vals.append("")
                    row_full.append("")
                else:
                    try:
                        res = convert_units(val, input_unit, output_unit)
                        fmt = f"{res:.{decimals}f}"
                        row_vals.append(fmt)
                        row_full.append(f"{val} {input_unit} = {fmt} {output_unit}")
                    except ValueError as e:
                        row_vals.append("Error")
                        row_full.append(str(e))
            
            self.converted_values.append(row_vals)
            self.converted_full.append(row_full)
            
        # Display results (tab separated for display is simple, but we can make it nicer if needed. 
        # Using simple text to match original behavior logic)
        display_text = "\n".join(["\t".join(row) for row in self.converted_full])
        self.result_edit.setPlainText(display_text)

    def clear_all(self):
        self.input_edit.clear()
        self.result_edit.clear()
        self.converted_values = []
        self.converted_full = []
        self.status_label.setText("")

    def swap_units(self):
        in_idx = self.input_unit_combo.currentIndex()
        out_idx = self.output_unit_combo.currentIndex()
        
        # Check if units exist in both (they generally do in this app)
        in_text = self.input_unit_combo.itemText(in_idx)
        out_text = self.output_unit_combo.itemText(out_idx)
        
        # Swap logic
        self.set_combo_text(self.input_unit_combo, out_text)
        self.set_combo_text(self.output_unit_combo, in_text)
        
        # Animate or just provide feedback?
        # Trigger conversion if there is input
        if self.input_edit.toPlainText().strip():
             self.convert()

    def copy_values(self):
        if not self.converted_values:
            self.show_message("没有可复制的内容", error=True)
            return
        text = "\n".join(["\t".join(row) for row in self.converted_values])
        QApplication.clipboard().setText(text)
        self.show_message("✓ 数值已成功复制到剪贴板")

    def save_settings(self):
        try:
            decimals = int(self.decimals_combo.currentText())
        except ValueError:
            decimals = 2
            
        self.config.set("decimal_places", decimals)
        self.config.set("default_input_unit", self.input_unit_combo.currentText())
        self.config.set("default_output_unit", self.output_unit_combo.currentText())

    def show_message(self, msg, error=False):
        self.status_label.setText(msg)
        self.status_label.setProperty("role", "status_error" if error else "status_success")
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        self.status_timer.start(2500)

    def clear_status(self):
        self.status_label.setText("")
        self.status_timer.stop()



    def show_help(self):
        # Could implement a custom dialog, for now minimal
        from PyQt6.QtWidgets import QMessageBox
        help_text = """
单位转换器 - 使用指南

1. 在顶部的输入框中输入或粘贴数值
   - 支持从Excel直接复制粘贴
   - 支持多种分隔符 (空格, 逗号, 分号等)

2. 选择输入和输出单位

3. 点击“转换”按钮

4. 复制结果
   - 点击“复制数值”可将纯数字结果复制到剪贴板
   - 结果兼容Excel粘贴
        """
        QMessageBox.information(self, "帮助", help_text)


class MainWindow(QMainWindow):
    def __init__(self, config: ConfigManager):
        super().__init__()
        self.config = config
        self.setWindowTitle("UnitMate")
        self.resize(720, 650)
        self.setMinimumSize(700, 550)
        
        # Apply Stylesheet
        self.setStyleSheet(STYLESHEET)

        self.init_tray()
        self.init_ui()

    def init_ui(self):
        # Main Tab Widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Unit Converter Tab
        self.converter_widget = UnitConverterWidget(self.config)
        self.tabs.addTab(self.converter_widget, "单位转换")
        
        # Calculator Tab
        self.calculator_widget = CalculatorWidget()
        self.tabs.addTab(self.calculator_widget, "计算器")

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.create_icon(QColor("#1E90FF"), QColor("#FFFFFF")))
        
        menu = QMenu()
        
        show_action = QAction("显示", self)
        show_action.triggered.connect(self.show_window)
        menu.addAction(show_action)
        
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_application)
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

    def create_icon(self, color1, color2, width=64, height=64):
        pixmap = QPixmap(width, height)
        pixmap.fill(color1)
        painter = QPainter(pixmap)
        painter.fillRect(width // 2, 0, width // 2, height // 2, color2)
        painter.fillRect(0, height // 2, width // 2, height // 2, color2)
        painter.end()
        return QIcon(pixmap)

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show_window()

    def show_window(self):
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.activateWindow()

    def quit_application(self):
        self.converter_widget.save_settings()
        self.tray_icon.hide() # Remove icon immediately
        QApplication.quit()

    def closeEvent(self, event):
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            self.converter_widget.save_settings()
            event.accept()


