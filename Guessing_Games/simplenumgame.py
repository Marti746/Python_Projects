import random
n = random.randrange(1,10)
guess = int(input("Enter any number: "))
# While loop checks to see if n is not equal to the guess
while n!= guess:
    # outputs message depending on guess value relevent to the n
    # Too low if guess is less than num
    if guess < n:
        print("Too low")
        guess = int(input("Enter number again: "))
    # Outputs too high if guess is greater than num
    elif guess > n:
        print("Too high!")
        guess = int(input("Enter number again: "))
    else:
      break
print("you guessed it right!!")
