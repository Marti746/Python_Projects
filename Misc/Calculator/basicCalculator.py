# Basic Calculator Project
# Steps:
# 1.) Define functions needed (add, sub, div, mul)
# 2.) Print options to the user + exit
# 3.) Ask for values 
# 4.) Call the functions and add while loop to continue the program until exit
def add(a, b):
    answer = a + b
    print(f"{a} + {b} = {answer} \n")

def sub(a, b):
    answer = a - b
    print(f"{a} - {b} = {answer} \n")

def mul(a, b):
    answer = a * b
    print(f"{a} * {b} = {answer} \n")

def div(a, b):
    # error handling to not allow divison of 0
    if b == 0:
        print("Error: Division by zero is not allowed. \n")
    else:
        answer = a / b
        print(f"{a} / {b} = {answer} \n")

while True:
    print("*" * 30)
    print("A. Addition")
    print("B. Subtraction")
    print("C. Multiplication")
    print("D. Division")
    print("E. Exit")
    print("*" * 30)
    choice = input("What would you like to do: ").lower()

    # Added basic error handling to only allow numbers to be entered 
    if choice == "a":
        print("Addition")
        try:
            a = float(input("Input first number: "))
            b = float(input("Input second number: "))
            add(a, b)
        except ValueError:
            print("Error: Please input valid numbers.\n")
    elif choice == "b":
        print("Subtraction")
        try:
            a = float(input("Input first number: "))
            b = float(input("Input second number: "))
            sub(a, b)
        except ValueError:
            print("Error: Please input valid numbers.\n")
    elif choice == "c":
        print("Multiplication")
        try:
            a = float(input("Input first number: "))
            b = float(input("Input second number: "))
            mul(a, b)
        except ValueError:
            print("Error: Please input valid numbers.\n")
    elif choice == "d":
        print("Division")
        try:
            a = float(input("Input first number: "))
            b = float(input("Input second number: "))
            div(a, b)
        except ValueError:
            print("Error: Please input valid numbers.\n")
    else:
        quit()
