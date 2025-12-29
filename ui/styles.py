
# Modern Dark Theme QSS

STYLESHEET = """
/* Global Reset */
QWidget {
    background-color: #121212; /* Very dark grey, Material Design recommended */
    color: #E0E0E0;
    font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
    font-size: 14px;
}

QMainWindow {
    background-color: #121212;
}

/* Frames & Containers */
QFrame {
    border: none;
}

QGroupBox {
    border: 1px solid #333333;
    border-radius: 8px;
    margin-top: 24px; /* Space for title */
    background-color: #1E1E1E;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 5px;
    color: #BB86FC; /* Material Design Primary Variant or similar accent */
    font-weight: bold;
    font-size: 13px;
    background-color: transparent;
}

/* Text Inputs */
QPlainTextEdit, QLineEdit {
    background-color: #2C2C2C;
    color: #FFFFFF;
    border: 1px solid #333333;
    border-radius: 6px;
    padding: 8px;
    selection-background-color: #BB86FC;
    selection-color: #000000;
}

QPlainTextEdit:focus, QLineEdit:focus {
    border: 1px solid #BB86FC; /* Accent color on focus */
}

/* Buttons */
QPushButton {
    background-color: #2C2C2C;
    color: #E0E0E0;
    border: 1px solid #333333;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #383838;
    border-color: #444444;
}

QPushButton:pressed {
    background-color: #1A1A1A;
}

/* Primary/Accent Button Style */
QPushButton[role="primary"] {
    background-color: #BB86FC;
    color: #000000;
    border: none;
}

QPushButton[role="primary"]:hover {
    background-color: #D4B2FC; /* Lighter shade */
}

QPushButton[role="primary"]:pressed {
    background-color: #9955E8; /* Darker shade */
}

/* Subtle Link Button */
QPushButton[role="subtle"] {
    background-color: transparent;
    border: none;
    color: #AAAAAA;
    font-weight: normal;
    text-align: center;
}

QPushButton[role="subtle"]:hover {
    color: #FFFFFF;
    text-decoration: underline;
}

/* Combo Boxes */
QComboBox {
    background-color: #2C2C2C;
    border: 1px solid #333333;
    border-radius: 6px;
    padding: 5px 10px;
    min-width: 70px;
}

QComboBox:hover {
    border-color: #555555;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
    background-color: transparent;
}

QComboBox QAbstractItemView {
    background-color: #2C2C2C;
    border: 1px solid #333333;
    selection-background-color: #BB86FC;
    selection-color: #000000;
}

/* ScrollBars */
QScrollBar:vertical {
    border: none;
    background: #121212;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #444444;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #555555;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Labels */
QLabel {
    color: #B0B0B0;
}

QLabel[role="heading"] {
    color: #FFFFFF;
    font-size: 16px;
    font-weight: bold;
}

/* Status Bar / Message */
QLabel[role="status_success"] {
    color: #03DAC6; /* Teal */
}
QLabel[role="status_error"] {
    color: #CF6679; /* Red/Pink */
}

/* --- Tab Widget --- */
QTabWidget::pane {
    border: 1px solid #333333;
    border-radius: 8px;
    background-color: #1E1E1E;
    top: -1px;
}

QTabBar::tab {
    background: #121212;
    color: #808080;
    padding: 8px 20px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border: 1px solid transparent;
    margin-right: 4px;
    font-weight: 600;
}

QTabBar::tab:selected {
    background: #1E1E1E;
    color: #BB86FC;
    border: 1px solid #333333;
    border-bottom: 1px solid #1E1E1E;
}

QTabBar::tab:hover:!selected {
    background: #1A1A1A;
    color: #B0B0B0;
}

/* --- Calculator Specifics --- */
QPushButton[role="calc_num"] {
    background-color: #2C2C2C;
    font-size: 18px;
    border-radius: 8px;
}
QPushButton[role="calc_num"]:hover {
    background-color: #3E3E3E;
}

QPushButton[role="calc_op"] {
    background-color: #333333;
    color: #BB86FC;
    font-size: 20px;
    border-radius: 8px;
}
QPushButton[role="calc_op"]:hover {
    background-color: #404040;
}

QPushButton[role="calc_equal"] {
    background-color: #BB86FC;
    color: #000000;
    border-radius: 8px;
    font-weight: bold;
    font-size: 20px;
}
QPushButton[role="calc_equal"]:hover {
    background-color: #D4B2FC;
}

QPushButton[role="calc_clear"] {
    background-color: #CF6679;
    color: #000000;
    border-radius: 8px;
    font-weight: bold;
}
QPushButton[role="calc_clear"]:hover {
    background-color: #E57373;
}"""
