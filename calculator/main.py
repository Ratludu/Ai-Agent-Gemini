# main.py

import sys
from pkg.calculator import Calculator
#from pkg.render import render


def main():
    print("Running main function")
    calculator = Calculator()
    expression = "3 + 7 * 2"
    #if len(sys.argv) <= 1:
    #    print("Calculator App")
    #    print('Usage: python main.py "<expression>"')
    #    print('Example: python main.py "3 + 5"')
    #    return

    #expression = " ".join(sys.argv[1:])
    try:
        result = calculator.evaluate(expression)
        #to_print = render(expression, result)
        print(f"The result is: {result}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
