import sys
from PySide6.QtWidgets import QApplication
from controller import CalculatorController


def main():
    app = QApplication(sys.argv)
    calculator = CalculatorController()
    calculator.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()