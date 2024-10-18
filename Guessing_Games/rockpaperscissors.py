# Rock, Paper, Scissor Games with Python
# Using basics of Python
# Using random library to get a random value from the list of options
import random
# Using functions
def get_choices():
    player_choice = input("Enter your choice (rock, paper, or scissors): ")

    # List that stores the choices
    options = ["rock", "paper", "scissors"]
    # Allows the computer to choose a random item from the list
    comp_choice = random.choice(options)

    # Dictionary to store both player and computer choices
    # With the pair value being player and computer {Key : Value}
    choices = {"player" : player_choice, "computer" : comp_choice}

    return choices

# New function that takes arguments
# Pass the player choice and computer choice
def check_winner(player, computer):
    # Prints the two choices that the player and computer choose
    print(f"You choose {player}, and the computer choose {computer}")

    # If statements dont need the () to surround information
    if player == computer:
        return "It's a tie!"
    # can do if player == "" and computer == ""
    elif player == "rock":
        if computer == "scissors":
            return "Rock smashes scissors! You Win!"
        else:
            return "Paper covers rock! You Lose."
    elif player == "paper":
        if computer == "rock":
            return "Paper covers rock! You Win!"
        else:
            return "Scissors cuts paper! You Lose."
    elif player == "scissors":
        if computer == "paper":
            return "Scissors cuts paper! You Win!"
        else:
            return "Rock crushes scissors! You Lose."

# Gets the choices from the function and stores it in a choices variable
choices = get_choices()
# Sends to see who won
# Can get information from a dictionary to send by choices[key] getting the key
winner = check_winner(choices["player"], choices["computer"])
print(winner)

