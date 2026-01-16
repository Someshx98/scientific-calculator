import math


class MathEngine:
    def __init__(self):
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        self.right_assoc = {'^'}
        self.angle_mode = 'DEG'

        self.functions = {
            'sin', 'cos', 'tan', 'sqrt', 'log10', 'ln', 'exp',
            'fact', 'inv', 'sinh', 'cosh', 'tanh', 'pow10', 'root',
            'asin', 'acos', 'atan', 'asinh', 'acosh', 'atanh'
        }

        self.constants = {
            'pi': math.pi,
            'e': math.e
        }

    def set_angle_mode(self, mode):
        if mode in ['DEG', 'RAD']:
            self.angle_mode = mode

    def get_angle_mode(self):
        return self.angle_mode

    def toggle_angle_mode(self):
        self.angle_mode = 'RAD' if self.angle_mode == 'DEG' else 'DEG'
        return self.angle_mode

    def tokenize(self, expression):
        expression = expression.replace(' ', '')
        expression = expression.replace('×', '*').replace('÷', '/')

        tokens = []
        i = 0

        while i < len(expression):
            if expression[i].isdigit() or expression[i] == '.':
                num = ''
                has_dot = False
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        if has_dot:
                            raise ValueError("Invalid number format")
                        has_dot = True
                    num += expression[i]
                    i += 1
                if num and num != '.':
                    tokens.append(num)
                continue

            if expression[i].isalpha():
                func = ''
                while i < len(expression) and expression[i].isalpha():
                    func += expression[i]
                    i += 1

                if func in self.functions:
                    tokens.append(func)
                elif func in self.constants:
                    tokens.append(str(self.constants[func]))
                else:
                    raise ValueError(f"Unknown function: {func}")
                continue

            if expression[i] in '+-*/^(),':
                tokens.append(expression[i])
                i += 1
                continue

            raise ValueError(f"Unknown character: {expression[i]}")

        return tokens

    def infix_to_postfix(self, tokens):
        output = []
        stack = []
        prev_token = None

        for token in tokens:
            if token in self.functions:
                stack.append(token)

            elif token not in '+-*/^(),':
                output.append(token)

            elif token == '(':
                stack.append(token)

            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack:
                    stack.pop()
                    if stack and stack[-1] in self.functions:
                        output.append(stack.pop())
                else:
                    raise ValueError("Mismatched parentheses")

            elif token == ',':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())

            elif token in self.precedence:
                if token == '-' and (prev_token is None or prev_token in '(+-*/^,'):
                    output.append('0')

                while (stack and
                       stack[-1] != '(' and
                       stack[-1] in self.precedence and
                       (self.precedence[stack[-1]] > self.precedence[token] or
                        (self.precedence[stack[-1]] == self.precedence[token] and
                         token not in self.right_assoc))):
                    output.append(stack.pop())
                stack.append(token)

            prev_token = token

        while stack:
            if stack[-1] in '()':
                raise ValueError("Mismatched parentheses")
            output.append(stack.pop())

        return output

    def apply_function(self, func, *args):
        if func == 'sin':
            angle = args[0]
            if self.angle_mode == 'DEG':
                angle = math.radians(angle)
            return math.sin(angle)

        elif func == 'cos':
            angle = args[0]
            if self.angle_mode == 'DEG':
                angle = math.radians(angle)
            return math.cos(angle)

        elif func == 'tan':
            angle = args[0]
            if self.angle_mode == 'DEG':
                angle = math.radians(angle)
            if abs(math.cos(angle)) < 1e-10:
                raise ValueError("tan undefined")
            return math.tan(angle)

        elif func == 'sinh':
            return math.sinh(args[0])

        elif func == 'cosh':
            return math.cosh(args[0])

        elif func == 'tanh':
            return math.tanh(args[0])

        elif func == 'asin':
            if args[0] < -1 or args[0] > 1:
                raise ValueError("asin domain error")
            result = math.asin(args[0])
            if self.angle_mode == 'DEG':
                result = math.degrees(result)
            return result

        elif func == 'acos':
            if args[0] < -1 or args[0] > 1:
                raise ValueError("acos domain error")
            result = math.acos(args[0])
            if self.angle_mode == 'DEG':
                result = math.degrees(result)
            return result

        elif func == 'atan':
            result = math.atan(args[0])
            if self.angle_mode == 'DEG':
                result = math.degrees(result)
            return result

        elif func == 'asinh':
            return math.asinh(args[0])

        elif func == 'acosh':
            if args[0] < 1:
                raise ValueError("acosh domain error")
            return math.acosh(args[0])

        elif func == 'atanh':
            if args[0] <= -1 or args[0] >= 1:
                raise ValueError("atanh domain error")
            return math.atanh(args[0])

        elif func == 'sqrt':
            if args[0] < 0:
                raise ValueError("sqrt of negative")
            return math.sqrt(args[0])

        elif func == 'log10':
            if args[0] <= 0:
                raise ValueError("log of non-positive")
            return math.log10(args[0])

        elif func == 'ln':
            if args[0] <= 0:
                raise ValueError("ln of non-positive")
            return math.log(args[0])

        elif func == 'exp':
            try:
                return math.exp(args[0])
            except OverflowError:
                raise ValueError("exp too large")

        elif func == 'pow10':
            try:
                return 10 ** args[0]
            except OverflowError:
                raise ValueError("pow10 too large")

        elif func == 'fact':
            if args[0] < 0:
                raise ValueError("factorial negative")
            if args[0] != int(args[0]):
                raise ValueError("factorial integer only")
            if args[0] > 170:
                raise ValueError("factorial too large")
            return math.factorial(int(args[0]))

        elif func == 'inv':
            if args[0] == 0:
                raise ZeroDivisionError("1/x where x=0")
            return 1.0 / args[0]

        elif func == 'root':
            if len(args) != 2:
                raise ValueError("root needs 2 args")
            n, x = args
            if n == 0:
                raise ValueError("root index 0")
            if x < 0 and int(n) == n and int(n) % 2 == 0:
                raise ValueError("even root negative")
            if x == 0:
                return 0
            if x < 0:
                return -(abs(x) ** (1.0 / n))
            return x ** (1.0 / n)

        raise ValueError(f"Unknown function: {func}")

    def evaluate_postfix(self, tokens):
        stack = []

        for token in tokens:
            if token in self.functions:
                if token == 'root':
                    if len(stack) < 2:
                        raise ValueError("root needs 2 args")
                    x = stack.pop()
                    n = stack.pop()
                    result = self.apply_function(token, n, x)
                else:
                    if len(stack) < 1:
                        raise ValueError(f"{token} needs arg")
                    arg = stack.pop()
                    result = self.apply_function(token, arg)
                stack.append(result)

            elif token in self.precedence:
                if len(stack) < 2:
                    raise ValueError("Invalid expression")

                right = stack.pop()
                left = stack.pop()

                if token == '+':
                    result = left + right
                elif token == '-':
                    result = left - right
                elif token == '*':
                    result = left * right
                elif token == '/':
                    if right == 0:
                        raise ZeroDivisionError("Division by zero")
                    result = left / right
                elif token == '^':
                    try:
                        result = left ** right
                    except OverflowError:
                        raise ValueError("Number too large")

                stack.append(result)
            else:
                try:
                    stack.append(float(token))
                except ValueError:
                    raise ValueError(f"Invalid number: {token}")

        if len(stack) != 1:
            raise ValueError("Invalid expression")

        return stack[0]

    def evaluate(self, expression):
        if not expression or expression.strip() == '':
            raise ValueError("Empty expression")

        tokens = self.tokenize(expression)
        postfix = self.infix_to_postfix(tokens)
        result = self.evaluate_postfix(postfix)

        return result