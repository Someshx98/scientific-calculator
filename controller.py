import random
from engine import MathEngine
from mapper import ButtonMapper
from ui import CalculatorUI


class CalculatorController:

    def __init__(self):
        self.engine = MathEngine()
        self.mapper = ButtonMapper()
        self.ui = CalculatorUI()

        self.memory = 0.0
        self.second_mode = False

        self._connect_signals()

        self.ui.showMaximized()
        self.ui.switch_to_basic()

    def _connect_signals(self):
        self.ui.mode_button.clicked.connect(self._handle_mode_toggle)
        self._connect_basic_buttons()
        self._connect_scientific_buttons()

    def _connect_basic_buttons(self):
        basic_buttons = [
            'MC', 'M+', 'M-', 'MR',
            'AC', '⌫', '±', '÷',
            '7', '8', '9', '×',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '%', '0', '.', '='
        ]

        for btn_text in basic_buttons:
            key = f"basic_{btn_text}"
            if key in self.ui.button_refs:
                self._connect_button(btn_text, lookup_key=key)

    def _connect_scientific_buttons(self):
        scientific_buttons = [
            '2ⁿᵈ', '(', ')', '10ˣ', 'MC', 'M+', 'M-', 'MR',
            '1/x', 'x²', 'x³', 'xʸ', 'AC', '⌫', '±', '÷',
            'x!', '√', 'ʸ√x', 'log', '7', '8', '9', '×',
            'sin', 'cos', 'tan', 'ln', '4', '5', '6', '-',
            'sinh', 'cosh', 'tanh', 'eˣ', '1', '2', '3', '+',
            'DEG', 'π', 'e', 'Rand', '%', '0', '.', '='
        ]

        for btn_text in scientific_buttons:
            if btn_text in self.ui.button_refs:
                self._connect_button(btn_text)

    def _connect_button(self, text, lookup_key=None):
        key = lookup_key if lookup_key else text
        btn = self.ui.button_refs.get(key)
        if not btn:
            return

        operators = ['AC', '⌫', '±', '÷', '×', '-', '+']
        scientific_functions = ['√', '∛', 'x²', 'x³', 'xʸ', 'π', 'e', '10ˣ', 'eˣ',
                                '1/x', 'x!', 'sin', 'cos', 'tan', 'sinh',
                                'cosh', 'tanh', 'log', 'ln', 'ʸ√x',
                                'asin', 'acos', 'atan', 'asinh', 'acosh', 'atanh',
                                'e^x', '10^x']

        if text == '2ⁿᵈ':
            btn.clicked.connect(self._handle_second_mode_toggle)
        elif text == 'DEG':
            btn.clicked.connect(self._handle_angle_mode_toggle)
        elif text == '±':
            btn.clicked.connect(self._handle_toggle_sign)
        elif text == 'AC':
            btn.clicked.connect(self._handle_clear_all)
        elif text == '⌫':
            btn.clicked.connect(self._handle_backspace)
        elif text == '=':
            btn.clicked.connect(self._handle_calculate)
        elif text == 'MC':
            btn.clicked.connect(self._handle_memory_clear)
        elif text == 'M+':
            btn.clicked.connect(self._handle_add_memory)
        elif text == 'M-':
            btn.clicked.connect(self._handle_sub_memory)
        elif text == 'MR':
            btn.clicked.connect(self._handle_recall_memory)
        elif text == '%':
            btn.clicked.connect(self._handle_percentage)
        elif text == 'Rand':
            btn.clicked.connect(self._handle_insert_random)
        elif text in ['EE', 'Seed']:
            if text == 'EE':
                btn.clicked.connect(self._handle_scientific_notation)
            else:
                btn.clicked.connect(self._handle_set_random_seed)
        elif text in scientific_functions:
            btn.clicked.connect(lambda checked, val=text: self._handle_function_button(val))
        elif text in operators:
            btn.clicked.connect(lambda checked, val=text: self._handle_insert_operator(val))
        else:
            btn.clicked.connect(lambda checked, val=text: self._handle_insert_number(val))

    def _handle_mode_toggle(self):
        is_basic = self.ui.button_stack.currentIndex() == 0
        if is_basic:
            self.ui.switch_to_scientific()
        else:
            self.ui.switch_to_basic()

    def _handle_angle_mode_toggle(self):
        new_mode = self.engine.toggle_angle_mode()
        self.ui.update_angle_mode_button(new_mode)

    def _handle_second_mode_toggle(self):
        self.second_mode = not self.second_mode

        second_functions = {
            'sin': ('sin', 'asin'),
            'cos': ('cos', 'acos'),
            'tan': ('tan', 'atan'),
            'sinh': ('sinh', 'asinh'),
            'cosh': ('cosh', 'acosh'),
            'tanh': ('tanh', 'atanh'),
            'ln': ('ln', 'e^x'),
            'log': ('log', '10^x'),
            'x²': ('x²', '√'),
            'x³': ('x³', '∛'),
            'Rand': ('Rand', 'Seed'),
        }

        self.ui.update_second_mode_button(self.second_mode)

        for primary, (normal, alt) in second_functions.items():
            text = alt if self.second_mode else normal
            self.ui.update_function_button_text(primary, text)

    def _handle_toggle_sign(self):
        current = self.ui.expression_label.text()

        if not current:
            return

        try:
            result = self.ui.result_label.text()
            if result != "0" and result != "Error":
                value = float(result)
                new_value = -value
                self.ui.expression_label.setText(str(new_value))
                self.ui.result_label.setText(str(new_value))
        except ValueError:
            if current.startswith('-'):
                self.ui.expression_label.setText(current[1:])
            else:
                self.ui.expression_label.setText('-' + current)

    def _handle_insert_number(self, val):
        current = self.ui.expression_label.text()
        new_text = current + str(val)
        self.ui.expression_label.setText(new_text)

    def _handle_insert_operator(self, op):
        current = self.ui.expression_label.text()
        ops = ['+', '-', '×', '÷', '.', '%']

        if not current and op != '-':
            return

        if current and current[-1] in ops:
            new_text = current[:-1] + op
        else:
            new_text = current + op

        self.ui.expression_label.setText(new_text)

    def _handle_function_button(self, button_text):
        current = self.ui.expression_label.text()
        new_text = self.mapper.transform(button_text, current)
        self.ui.expression_label.setText(new_text)

    def _handle_clear_all(self):
        self.ui.expression_label.setText("")
        self.ui.result_label.setText("0")

    def _handle_backspace(self):
        current = self.ui.expression_label.text()
        self.ui.expression_label.setText(current[:-1])

    def _handle_calculate(self):
        try:
            expression = self.ui.expression_label.text()
            result = self.engine.evaluate(expression)

            if 1e10 > abs(result) > 1e-10:
                formatted = f"{result:.10g}"
                self.ui.result_label.setText(formatted)
            else:
                self.ui.result_label.setText(f"{result:.6e}")
        except Exception as e:
            error_msg = str(e) if len(str(e)) < 30 else "Error"
            self.ui.result_label.setText(error_msg)

    def _handle_percentage(self):
        try:
            expression = self.ui.expression_label.text()
            result = self.engine.evaluate(expression) / 100
            self.ui.result_label.setText(f"{result:.10g}")
        except Exception:
            self.ui.result_label.setText("Error")

    def _handle_memory_clear(self):
        self.memory = 0.0

    def _handle_add_memory(self):
        try:
            current = float(self.ui.result_label.text())
            self.memory += current
        except ValueError:
            pass

    def _handle_sub_memory(self):
        try:
            current = float(self.ui.result_label.text())
            self.memory -= current
        except ValueError:
            pass

    def _handle_recall_memory(self):
        self.ui.expression_label.setText(str(self.memory))

    def _handle_insert_random(self):
        current = self.ui.expression_label.text()
        rand_num = random.random()

        if current and (current[-1].isdigit() or current[-1] == ')'):
            new_text = current + '*' + str(rand_num)
        else:
            new_text = current + str(rand_num)

        self.ui.expression_label.setText(new_text)

    def _handle_scientific_notation(self):
        current = self.ui.expression_label.text()

        if not current or not current[-1].isdigit():
            return

        self.ui.expression_label.setText(current + 'e')

    def _handle_set_random_seed(self):
        try:
            result = self.ui.result_label.text()
            if result != "0" and result != "Error":
                seed_value = int(float(result))
                random.seed(seed_value)
                self.ui.result_label.setText(f"Seed: {seed_value}")
        except ValueError:
            pass

    def show(self):
        self.ui.show()