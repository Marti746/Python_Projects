# This is a mini project working with variables and user input
# imports the random library
import random
my_num = random.randint(1,50)
# gets user name and prints it
usr_name = input("What is your name? ")
print(f"Thank you {usr_name}!")

# asks user for number
# cast the user input from string to int
usr_num = int(input("Guess the number I am thinking of! Its between 1 and 50 "))
total_guess = 10

if usr_num == 0:
    exit()
# While loop to check if number is not the same and keep asking for input
while usr_num != my_num:
    total_guess = total_guess - 1
    # Displays a messages for the user with their guess and amount of guess left
    print(f"Sorry {usr_name}, {usr_num} was the wrong number! You have \
{total_guess} guess left")
    usr_num = int(input("Guess again! "))
    # Checks to see how many guesses they have left
    if total_guess == 0:
        print("this is the number, ", my_num)
        exit()
    # Checks to see if the user enters 0 and if they did then exit program
    elif usr_num == 0:
        exit()
# if user matched the random number then display message
# part of the while loop
else:
    print(f"Good job {usr_name}, you guessed my number! It was {my_num}")

# While loop can have a else statement in it
