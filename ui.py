from PySide6.QtWidgets import (QWidget, QGridLayout, QPushButton,
                               QVBoxLayout, QLabel, QFrame, QStackedWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon


class CalculatorUI(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scientific Calculator")
        self.setWindowIcon(QIcon("assets/icon/logo.ico"))
        self.setStyleSheet("background-color: hsl(0, 0%, 1%)")

        self.mode_button = None
        self.expression_label = None
        self.result_label = None
        self.button_stack = None
        self.angle_mode_button = None
        self.second_button = None
        self.button_refs = {}

        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)

        self.watermark = QLabel("© Somesh Behera | Hybrid Scientific Calculator")
        self.watermark.setAlignment(Qt.AlignCenter)
        self.watermark.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.25);
                font-size: 11px;
                padding-top: 4px;
            }
        """)

        self.mode_button = self._create_mode_button()
        main_layout.addWidget(self.mode_button)

        main_layout.addWidget(self.watermark)

        display_frame = self._create_display()
        main_layout.addWidget(display_frame)

        self.button_stack = QStackedWidget()
        self.button_stack.addWidget(self._create_basic_panel())
        self.button_stack.addWidget(self._create_scientific_panel())
        main_layout.addWidget(self.button_stack)

        self.setLayout(main_layout)

    def _create_mode_button(self):
        btn = QPushButton("Scientific")
        btn.setFixedHeight(40)
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.8);
                color: black;
            }
        """)
        return btn

    def _create_display(self):
        frame = QFrame()
        frame.setFixedHeight(120)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)

        self.expression_label = QLabel("")
        self.expression_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.expression_label.setWordWrap(True)
        self.expression_label.setFixedHeight(30)
        self.expression_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.6); font-size: 16px;"
        )
        layout.addWidget(self.expression_label)

        layout.addStretch()

        self.result_label = QLabel("0")
        self.result_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.result_label.setStyleSheet(
            "color: white; font-size: 48px; font-weight: bold;"
        )
        layout.addWidget(self.result_label)

        return frame

    def _create_basic_panel(self):
        panel = QWidget()
        grid = QGridLayout(panel)
        grid.setSpacing(12)
        grid.setContentsMargins(0, 0, 0, 0)

        buttons = [
            'MC', 'M+', 'M-', 'MR',
            'AC', '⌫', '±', '÷',
            '7', '8', '9', '×',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '%', '0', '.', '='
        ]

        row, col = 0, 0
        for text in buttons:
            btn = self._create_button(text, is_scientific=False)
            grid.addWidget(btn, row, col)
            self.button_refs[f"basic_{text}"] = btn
            col += 1
            if col > 3:
                col = 0
                row += 1

        return panel

    def _create_scientific_panel(self):
        panel = QWidget()
        grid = QGridLayout(panel)
        grid.setSpacing(12)
        grid.setContentsMargins(0, 0, 0, 0)

        buttons = [
            '2ⁿᵈ', '(', ')', '10ˣ', 'MC', 'M+', 'M-', 'MR',
            '1/x', 'x²', 'x³', 'xʸ', 'AC', '⌫', '±', '÷',
            'x!', '√', 'ʸ√x', 'log', '7', '8', '9', '×',
            'sin', 'cos', 'tan', 'ln', '4', '5', '6', '-',
            'sinh', 'cosh', 'tanh', 'eˣ', '1', '2', '3', '+',
            'DEG', 'π', 'e', 'Rand', '%', '0', '.', '='
        ]

        row, col = 0, 0
        for text in buttons:
            btn = self._create_button(text, is_scientific=True)
            grid.addWidget(btn, row, col)

            self.button_refs[text] = btn

            if text == 'DEG':
                self.angle_mode_button = btn
            elif text == '2ⁿᵈ':
                self.second_button = btn

            col += 1
            if col > 7:
                col = 0
                row += 1

        return panel

    def _create_button(self, text, is_scientific=False):
        btn = QPushButton(text)
        btn.setMinimumSize(80, 80)

        operators = ['AC', '⌫', '±', '÷', '×', '-', '+']

        if text == '=':
            btn.setStyleSheet(self._get_equal_style())
        elif text == 'DEG':
            btn.setStyleSheet(self._get_angle_mode_style())
        elif text == '2ⁿᵈ':
            btn.setStyleSheet(self._get_second_mode_style())
        elif text in operators:
            btn.setStyleSheet(self._get_operator_style())
        else:
            btn.setStyleSheet(self._get_button_style())

        return btn

    def _get_button_style(self):
        return """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 40px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.8);
                color: black;
            }
        """

    def _get_operator_style(self):
        return self._get_button_style() + """
            QPushButton {
                background-color: rgba(199, 150, 14, 0.15);
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(199, 150, 14, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(199, 150, 14, 0.8);
            }
        """

    def _get_equal_style(self):
        return self._get_button_style() + """
            QPushButton {
                background-color: rgba(236, 96, 89, 0.15);
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(236, 96, 89, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(236, 96, 89, 0.8);
            }
        """

    def _get_angle_mode_style(self):
        return self._get_button_style() + """
            QPushButton {
                background-color: rgba(100, 150, 255, 0.2);
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(100, 150, 255, 0.35);
            }
            QPushButton:pressed {
                background-color: rgba(100, 150, 255, 0.8);
            }
        """

    def _get_second_mode_style(self):
        return self._get_button_style() + """
            QPushButton {
                background-color: rgba(255, 150, 100, 0.2);
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 150, 100, 0.35);
            }
            QPushButton:pressed {
                background-color: rgba(255, 150, 100, 0.8);
            }
        """

    def _get_second_mode_active_style(self):
        return self._get_button_style() + """
            QPushButton {
                background-color: rgba(255, 150, 100, 0.6);
                font-weight: bold;
                border: 2px solid rgba(255, 150, 100, 1.0);
            }
            QPushButton:hover {
                background-color: rgba(255, 150, 100, 0.7);
            }
            QPushButton:pressed {
                background-color: rgba(255, 150, 100, 0.9);
            }
        """

    def switch_to_scientific(self):
        self.button_stack.setCurrentIndex(1)
        self.mode_button.setText("Basic")

    def switch_to_basic(self):
        self.button_stack.setCurrentIndex(0)
        self.mode_button.setText("Scientific")

    def update_angle_mode_button(self, mode_text):
        if self.angle_mode_button:
            self.angle_mode_button.setText(mode_text)

    def update_second_mode_button(self, is_active):
        if self.second_button:
            if is_active:
                self.second_button.setStyleSheet(self._get_second_mode_active_style())
            else:
                self.second_button.setStyleSheet(self._get_second_mode_style())

    def update_function_button_text(self, button_name, text):
        if button_name in self.button_refs:
            self.button_refs[button_name].setText(text)