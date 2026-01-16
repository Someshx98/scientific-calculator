import unittest
import sys
import os

# Add parent directory to path so we can import engine
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine import MathEngine


class TestMathEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MathEngine()

    def test_operator_precedence_basic(self):
        self.assertAlmostEqual(self.engine.evaluate("2+3*4"), 14)
        self.assertAlmostEqual(self.engine.evaluate("2*3+4"), 10)
        self.assertAlmostEqual(self.engine.evaluate("10-2*3"), 4)
        self.assertAlmostEqual(self.engine.evaluate("10/2+3"), 8)

    def test_operator_precedence_power(self):
        self.assertAlmostEqual(self.engine.evaluate("2^3^2"), 512)
        self.assertAlmostEqual(self.engine.evaluate("2*3^2"), 18)
        self.assertAlmostEqual(self.engine.evaluate("2+3^2"), 11)
        self.assertAlmostEqual(self.engine.evaluate("10-2^3"), 2)

    def test_operator_precedence_mixed(self):
        self.assertAlmostEqual(self.engine.evaluate("2+3*4^2"), 50)
        self.assertAlmostEqual(self.engine.evaluate("10/2^2+3"), 5.5)
        self.assertAlmostEqual(self.engine.evaluate("5*2^3-1"), 39)

    def test_parentheses_basic(self):
        self.assertAlmostEqual(self.engine.evaluate("(2+3)*4"), 20)
        self.assertAlmostEqual(self.engine.evaluate("2*(3+4)"), 14)
        self.assertAlmostEqual(self.engine.evaluate("(10-2)*3"), 24)
        self.assertAlmostEqual(self.engine.evaluate("10/(2+3)"), 2)

    def test_parentheses_nested(self):
        self.assertAlmostEqual(self.engine.evaluate("((2+3)*4)"), 20)
        self.assertAlmostEqual(self.engine.evaluate("2*((3+4)*5)"), 70)
        self.assertAlmostEqual(self.engine.evaluate("(2+(3*(4+5)))"), 29)
        self.assertAlmostEqual(self.engine.evaluate("((2+3)*(4+5))"), 45)

    def test_parentheses_with_power(self):
        self.assertAlmostEqual(self.engine.evaluate("(2+3)^2"), 25)
        self.assertAlmostEqual(self.engine.evaluate("2^(3+1)"), 16)
        self.assertAlmostEqual(self.engine.evaluate("(2^3)^2"), 64)

    def test_trig_deg_mode(self):
        self.engine.set_angle_mode('DEG')
        self.assertAlmostEqual(self.engine.evaluate("sin(0)"), 0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("sin(30)"), 0.5, places=10)
        self.assertAlmostEqual(self.engine.evaluate("sin(90)"), 1.0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("cos(0)"), 1.0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("cos(60)"), 0.5, places=10)
        self.assertAlmostEqual(self.engine.evaluate("cos(90)"), 0.0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("tan(0)"), 0.0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("tan(45)"), 1.0, places=10)

    def test_trig_rad_mode(self):
        self.engine.set_angle_mode('RAD')
        self.assertAlmostEqual(self.engine.evaluate("sin(0)"), 0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("sin(1.5707963267948966)"), 1.0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("cos(0)"), 1.0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("cos(3.141592653589793)"), -1.0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("tan(0)"), 0.0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("tan(0.7853981633974483)"), 1.0, places=10)

    def test_trig_hyperbolic(self):
        self.assertAlmostEqual(self.engine.evaluate("sinh(0)"), 0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("cosh(0)"), 1, places=10)
        self.assertAlmostEqual(self.engine.evaluate("tanh(0)"), 0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("sinh(1)"), 1.1752011936438014, places=10)
        self.assertAlmostEqual(self.engine.evaluate("cosh(1)"), 1.5430806348152437, places=10)

    def test_factorial_valid(self):
        self.assertAlmostEqual(self.engine.evaluate("fact(0)"), 1)
        self.assertAlmostEqual(self.engine.evaluate("fact(1)"), 1)
        self.assertAlmostEqual(self.engine.evaluate("fact(5)"), 120)
        self.assertAlmostEqual(self.engine.evaluate("fact(10)"), 3628800)
        self.assertAlmostEqual(self.engine.evaluate("fact(20)"), 2432902008176640000)

    def test_factorial_boundaries(self):
        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("fact(-1)")
        self.assertIn("factorial negative", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("fact(2.5)")
        self.assertIn("factorial integer only", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("fact(171)")
        self.assertIn("factorial too large", str(context.exception))

    def test_sqrt_valid(self):
        self.assertAlmostEqual(self.engine.evaluate("sqrt(0)"), 0)
        self.assertAlmostEqual(self.engine.evaluate("sqrt(1)"), 1)
        self.assertAlmostEqual(self.engine.evaluate("sqrt(4)"), 2)
        self.assertAlmostEqual(self.engine.evaluate("sqrt(16)"), 4)
        self.assertAlmostEqual(self.engine.evaluate("sqrt(2)"), 1.4142135623730951, places=10)

    def test_sqrt_domain_error(self):
        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("sqrt(-1)")
        self.assertIn("sqrt of negative", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("sqrt(-100)")
        self.assertIn("sqrt of negative", str(context.exception))

    def test_log10_valid(self):
        self.assertAlmostEqual(self.engine.evaluate("log10(1)"), 0)
        self.assertAlmostEqual(self.engine.evaluate("log10(10)"), 1)
        self.assertAlmostEqual(self.engine.evaluate("log10(100)"), 2)
        self.assertAlmostEqual(self.engine.evaluate("log10(1000)"), 3)

    def test_log10_domain_error(self):
        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("log10(0)")
        self.assertIn("log of non-positive", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("log10(-1)")
        self.assertIn("log of non-positive", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("log10(-100)")
        self.assertIn("log of non-positive", str(context.exception))

    def test_ln_valid(self):
        self.assertAlmostEqual(self.engine.evaluate("ln(1)"), 0)
        self.assertAlmostEqual(self.engine.evaluate("ln(2.718281828459045)"), 1, places=10)
        self.assertAlmostEqual(self.engine.evaluate("ln(7.38905609893065)"), 2, places=10)

    def test_ln_domain_error(self):
        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("ln(0)")
        self.assertIn("ln of non-positive", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("ln(-1)")
        self.assertIn("ln of non-positive", str(context.exception))

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.engine.evaluate("1/0")

        with self.assertRaises(ZeroDivisionError):
            self.engine.evaluate("10/0")

        with self.assertRaises(ZeroDivisionError):
            self.engine.evaluate("5/(2-2)")

    def test_inv_zero(self):
        with self.assertRaises(ZeroDivisionError) as context:
            self.engine.evaluate("inv(0)")
        self.assertIn("1/x where x=0", str(context.exception))

    def test_inv_valid(self):
        self.assertAlmostEqual(self.engine.evaluate("inv(1)"), 1)
        self.assertAlmostEqual(self.engine.evaluate("inv(2)"), 0.5)
        self.assertAlmostEqual(self.engine.evaluate("inv(4)"), 0.25)
        self.assertAlmostEqual(self.engine.evaluate("inv(10)"), 0.1)

    def test_exp_valid(self):
        self.assertAlmostEqual(self.engine.evaluate("exp(0)"), 1)
        self.assertAlmostEqual(self.engine.evaluate("exp(1)"), 2.718281828459045, places=10)
        self.assertAlmostEqual(self.engine.evaluate("exp(2)"), 7.38905609893065, places=10)

    def test_exp_overflow(self):
        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("exp(1000)")
        self.assertIn("exp too large", str(context.exception))

    def test_pow10_valid(self):
        self.assertAlmostEqual(self.engine.evaluate("pow10(0)"), 1)
        self.assertAlmostEqual(self.engine.evaluate("pow10(1)"), 10)
        self.assertAlmostEqual(self.engine.evaluate("pow10(2)"), 100)
        self.assertAlmostEqual(self.engine.evaluate("pow10(3)"), 1000)

    def test_pow10_overflow(self):
        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("pow10(1000)")
        self.assertIn("pow10 too large", str(context.exception))

    def test_root_valid(self):
        self.assertAlmostEqual(self.engine.evaluate("root(2,4)"), 2)
        self.assertAlmostEqual(self.engine.evaluate("root(3,8)"), 2)
        self.assertAlmostEqual(self.engine.evaluate("root(2,9)"), 3)
        self.assertAlmostEqual(self.engine.evaluate("root(4,16)"), 2)

    def test_root_domain_error(self):
        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("root(2,-4)")
        self.assertIn("even root negative", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("root(0,5)")
        self.assertIn("root index 0", str(context.exception))

    def test_constants(self):
        self.assertAlmostEqual(self.engine.evaluate("pi"), 3.141592653589793, places=10)
        self.assertAlmostEqual(self.engine.evaluate("e"), 2.718281828459045, places=10)
        self.assertAlmostEqual(self.engine.evaluate("2*pi"), 6.283185307179586, places=10)
        self.assertAlmostEqual(self.engine.evaluate("e^2"), 7.38905609893065, places=10)

    def test_negative_numbers(self):
        self.assertAlmostEqual(self.engine.evaluate("-5"), -5)
        self.assertAlmostEqual(self.engine.evaluate("-5+3"), -2)
        self.assertAlmostEqual(self.engine.evaluate("10--5"), 15)
        self.assertAlmostEqual(self.engine.evaluate("-(5+3)"), -8)

    def test_complex_expressions(self):
        self.assertAlmostEqual(self.engine.evaluate("sin(30)+cos(60)"), 1.0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("sqrt(16)+fact(4)"), 28)
        self.assertAlmostEqual(self.engine.evaluate("log10(100)*ln(e)"), 2, places=10)
        self.assertAlmostEqual(self.engine.evaluate("2^3+sqrt(9)*fact(3)"), 26)

    def test_empty_expression(self):
        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("")
        self.assertIn("Empty expression", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("   ")
        self.assertIn("Empty expression", str(context.exception))

    def test_mismatched_parentheses(self):
        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("(2+3")
        self.assertIn("Mismatched parentheses", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("2+3)")
        self.assertIn("Mismatched parentheses", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("((2+3)")
        self.assertIn("Mismatched parentheses", str(context.exception))

    def test_tan_undefined(self):
        self.engine.set_angle_mode('DEG')
        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("tan(90)")
        self.assertIn("tan undefined", str(context.exception))

    def test_inverse_trig_deg_mode(self):
        self.engine.set_angle_mode('DEG')
        self.assertAlmostEqual(self.engine.evaluate("asin(0)"), 0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("asin(0.5)"), 30, places=10)
        self.assertAlmostEqual(self.engine.evaluate("asin(1)"), 90, places=10)
        self.assertAlmostEqual(self.engine.evaluate("acos(1)"), 0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("acos(0.5)"), 60, places=10)
        self.assertAlmostEqual(self.engine.evaluate("atan(0)"), 0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("atan(1)"), 45, places=10)

    def test_inverse_trig_rad_mode(self):
        self.engine.set_angle_mode('RAD')
        self.assertAlmostEqual(self.engine.evaluate("asin(0)"), 0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("asin(1)"), 1.5707963267948966, places=10)
        self.assertAlmostEqual(self.engine.evaluate("acos(1)"), 0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("atan(1)"), 0.7853981633974483, places=10)

    def test_inverse_trig_domain_errors(self):
        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("asin(2)")
        self.assertIn("asin domain error", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("acos(-2)")
        self.assertIn("acos domain error", str(context.exception))

    def test_inverse_hyperbolic(self):
        self.assertAlmostEqual(self.engine.evaluate("asinh(0)"), 0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("acosh(1)"), 0, places=10)
        self.assertAlmostEqual(self.engine.evaluate("atanh(0)"), 0, places=10)

        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("acosh(0.5)")
        self.assertIn("acosh domain error", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.engine.evaluate("atanh(1)")
        self.assertIn("atanh domain error", str(context.exception))


def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMathEngine)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print(f"\n{'=' * 70}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'=' * 70}")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)