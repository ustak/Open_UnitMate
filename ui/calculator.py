
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton, 
                             QLineEdit, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction

class CalculatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_input = ""
        self.result_shown = False

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Display
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont("Arial", 28))
        self.display.setFixedHeight(70)
        # Using default QLineEdit styles from styles.py, just overriding font size
        layout.addWidget(self.display)

        # Buttons
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        layout.addLayout(grid_layout)

        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('C', 3, 2), ('+', 3, 3),
            ('=', 4, 0, 1, 4)
        ]

        for btn_data in buttons:
            text = btn_data[0]
            row = btn_data[1]
            col = btn_data[2]
            row_span = btn_data[3] if len(btn_data) > 3 else 1
            col_span = btn_data[4] if len(btn_data) > 4 else 1

            btn = QPushButton(text)
            btn.setFixedSize(60, 60) if text != '=' else btn.setFixedHeight(60)
            
            # Set Property for Styling
            if text == '=':
                 btn.setProperty("role", "calc_equal")
                 btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            elif text == 'C':
                btn.setProperty("role", "calc_clear")
            elif text in ['/', '*', '-', '+']:
                btn.setProperty("role", "calc_op")
            else:
                btn.setProperty("role", "calc_num")

            btn.clicked.connect(lambda _, t=text: self.on_button_click(t))
            grid_layout.addWidget(btn, row, col, row_span, col_span)

    def on_button_click(self, text):
        if text == 'C':
            self.current_input = ""
            self.display.clear()
            self.result_shown = False
        elif text == '=':
            self.calculate_result()
        else:
            if self.result_shown:
                if text in ['+', '-', '*', '/']:
                    self.result_shown = False # Continue operation on result
                else:
                    self.current_input = "" # Start new number
                    self.result_shown = False
            
            self.current_input += text
            self.display.setText(self.current_input)

    def calculate_result(self):
        try:
            # Dangerous for production but okay for simple local calculator
            # In a real app, write a proper parser
            result = str(eval(self.current_input)) 
            self.display.setText(result)
            self.current_input = result
            self.result_shown = True
        except Exception:
            self.display.setText("Error")
            self.current_input = ""
            self.result_shown = True
