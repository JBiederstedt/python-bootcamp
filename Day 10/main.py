import art

def add(n1, n2):
    return n1 + n2

def substract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    if n2 == 0:
        print("Error! Cannot divide by zero.")
        return None
    return n1 / n2

operations = {
    "+": add,
    "-": substract,
    "*": multiply,
    "/": divide
}

def get_number_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a valid number.")

def get_operation_input():
    while True:
        operation = input("Pick an operation: ")
        print()
        if operation in operations:
            return operation
        else:
            print("Invalid operation! Please choose from the available operations: +, -, *, /")

def get_continue_input():
    while True:
        next_calculation = input(f"Type 'y' to continue calculating or 'n' to start a new calculation: ")
        print()
        if next_calculation.lower() in ['y', 'n']:
            return next_calculation.lower()
        else:
            print("Invalid input! Please type 'y' to continue or 'n' to start a new calculation.")

def calculator():
    print(art.logo)
    print()
    num1 = get_number_input("What's the first number?: ")
    print()
    
    for symbol in operations:
        print(symbol)
    should_continue = True
    print()

    while should_continue:
        operation_symbol = get_operation_input()
        num2 = get_number_input("What's the next number?: ")
        print()

        calculator_function = operations[operation_symbol]
        answer = calculator_function(num1, num2)
        
        if answer is not None:
            print(f"{num1} {operation_symbol} {num2} = {answer:.2f}")
            print()
        else:
            continue

        next_calculation = get_continue_input()
        if next_calculation == "y":
            num1 = answer
        else:
            should_continue = False
            print("Starting a new calculation...")
            print()

calculator()
