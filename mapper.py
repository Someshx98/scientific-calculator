class ButtonMapper:

    def __init__(self):
        self.transforms = {
            '√': lambda txt: self._wrap_last_term(txt, 'sqrt'),
            '∛': lambda txt: self._wrap_last_term(txt, 'root(3,'),
            'x²': lambda txt: self._append_power(txt, '2'),
            'x³': lambda txt: self._append_power(txt, '3'),
            'xʸ': lambda txt: txt + '^',
            'π': lambda txt: self._smart_multiply(txt, 'pi'),
            'e': lambda txt: self._smart_multiply(txt, 'e'),
            '10ˣ': lambda txt: self._wrap_last_term(txt, 'pow10'),
            'eˣ': lambda txt: self._wrap_last_term(txt, 'exp'),
            '1/x': lambda txt: self._wrap_last_term(txt, 'inv'),
            'x!': lambda txt: self._wrap_last_term(txt, 'fact'),
            'sin': lambda txt: txt + 'sin(',
            'cos': lambda txt: txt + 'cos(',
            'tan': lambda txt: txt + 'tan(',
            'sinh': lambda txt: txt + 'sinh(',
            'cosh': lambda txt: txt + 'cosh(',
            'tanh': lambda txt: txt + 'tanh(',
            'log': lambda txt: txt + 'log10(',
            'ln': lambda txt: txt + 'ln(',
            'ʸ√x': lambda txt: txt + 'root(',
            'asin': lambda txt: txt + 'asin(',
            'acos': lambda txt: txt + 'acos(',
            'atan': lambda txt: txt + 'atan(',
            'asinh': lambda txt: txt + 'asinh(',
            'acosh': lambda txt: txt + 'acosh(',
            'atanh': lambda txt: txt + 'atanh(',
            'e^x': lambda txt: self._wrap_last_term(txt, 'exp'),
            '10^x': lambda txt: self._wrap_last_term(txt, 'pow10'),
        }

    def _smart_multiply(self, txt, value):
        if txt and (txt[-1].isdigit() or txt[-1] == ')'):
            return txt + '*' + value
        return txt + value

    def _append_power(self, txt, power):
        if txt and (txt[-1].isdigit() or txt[-1] == ')'):
            return txt + '^' + power
        return txt

    def _wrap_last_term(self, txt, func):
        if not txt:
            return txt + f'{func}('

        if txt[-1].isdigit():
            i = len(txt) - 1
            while i >= 0 and (txt[i].isdigit() or txt[i] == '.'):
                i -= 1

            number = txt[i + 1:]
            prefix = txt[:i + 1]

            needs_multiply = prefix and (prefix[-1].isdigit() or prefix[-1] == ')')

            if needs_multiply:
                return prefix + f'*{func}({number})'
            return prefix + f'{func}({number})'

        elif txt[-1] == ')':
            paren_count = 1
            i = len(txt) - 2

            while i >= 0 and paren_count > 0:
                if txt[i] == ')':
                    paren_count += 1
                elif txt[i] == '(':
                    paren_count -= 1
                i -= 1

            start = i + 1

            func_start = start
            while func_start > 0 and txt[func_start - 1].isalpha():
                func_start -= 1

            expr = txt[func_start:]
            prefix = txt[:func_start]

            needs_multiply = prefix and (prefix[-1].isdigit() or prefix[-1] == ')')

            if needs_multiply:
                return prefix + f'*{func}({expr})'
            return prefix + f'{func}({expr})'

        return txt + f'{func}('

    def transform(self, button_text, current_text):
        if button_text in self.transforms:
            return self.transforms[button_text](current_text)
        else:
            return current_text + button_text