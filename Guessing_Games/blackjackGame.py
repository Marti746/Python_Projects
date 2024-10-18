# BlackJack Mini Porject applying what I have learned in Python so far
import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    # calls when there is a print called
    def __str__(self):
        return f"{self.rank['rank']} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        suits = ["spades", "clubs", "hearts", "diamonds"]
        # a list with each rank begin a dictionary
        ranks = [{"rank": "A", "value" : 11}, {"rank": "2", "value" : 2}, {"rank": "3", "value" : 3}, 
                {"rank": "4", "value" : 4}, {"rank": "5", "value" : 5}, {"rank": "6", "value" : 6}, 
                {"rank": "7", "value" : 7}, {"rank": "8", "value" : 8}, {"rank": "9", "value" : 9}, 
                {"rank": "10", "value" : 10}, {"rank": "J", "value" : 10}, {"rank": "Q", "value" : 10}, {"rank": "K", "value" : 10}]

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    # shuffles the card in the cards list
    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards) # inorder to access the variable we have to add self.cards

    # deals the cards
    def deal(self, number):
        cards_dealt = []
        for n in range(number):
            if len(self.cards) > 0:
                card = self.cards.pop()
                cards_dealt.append(card)
        return cards_dealt

class Hand:
    def __init__(self, dealer = False):
        self.cards = []
        self.value = 0
        self.dealer = dealer
    
    def addCard(self, cardList):
        self.cards.extend(cardList)
    
    def calcValue(self):
        self.value = 0
        hasAce = False
        
        # goes throught the cards and assignes the value to the self.value as well as sees if it is a A
        for card in self.cards:
            cardValue = int(card.rank["value"])
            self.value += cardValue
            if card.rank["rank"] == "A":
                hasAce = True
        # sets the value of an A to 1 if the total is over 21
        if hasAce and self.value > 21:
            self.value -= 10
    
    # gets the total value of the two cards
    def getValue(self):
        self.calcValue()
        return self.value
    
    # checks to see if the hand is a blackjack and returns true or false
    def isBlackJack(self):
        return self.getValue() == 21
    
    # displays the hand of either the user or dealer
    def display(self, showAllDealerCards=False):
        print(f'''{"Dealer's" if self.dealer else "Your"} hand:''')
        for index, card in enumerate(self.cards):
            # checks to see if the index is 0 and the its the dealer and if it is then the first card is hidden
            # can add a \ to go to the next line
            if index == 0 and self.dealer and not showAllDealerCards and not self.isBlackJack():
                print("Hidden")
            else:
                print(card)
        
        # prints the value of the player
        if not self.dealer:
            print("Value: ", self.getValue())
        print()

class Game():
    def play(self):
        gameNumber = 0
        gameToPlay = 0

        while gameToPlay <= 0:
            try:
                gameToPlay = int(input("How many games do you want to play? "))
            except:
                print("You must enter in a number!")
        
        while gameNumber < gameToPlay:
            gameNumber += 1

            deck = Deck()
            deck.shuffle()

            playerHand = Hand()
            dealerHand = Hand(dealer=True)

            for i in range(2):
                playerHand.addCard(deck.deal(1))
                dealerHand.addCard(deck.deal(1))
            
            print()
            print("*" * 30)
            print(f"Game {gameNumber} of {gameToPlay}")
            print("*" * 30)
            playerHand.display()
            dealerHand.display()

            # checks to see if the game is won then continues to the next game
            if self.checkWinner(playerHand, dealerHand):
                continue

            choice = ""
            # checks for player chose if they want another card or not
            while playerHand.getValue() < 21 and choice not in ["s", "stand"]:
                choice = input("Please choose 'Hit' or 'Stand': ").lower()
                print()
                while choice not in ["h", "s", "hit", "stand"]:
                    choice = input("Please enter 'Hit or 'Stand' or (H/S)").lower()
                    print()
                if choice in ["hit", "h"]:
                    playerHand.addCard(deck.deal(1))
                    playerHand.display()
            
            if self.checkWinner(playerHand, dealerHand):
                continue

            playerHandValue = playerHand.getValue()
            dealerHandValue = dealerHand.getValue()

            # while loop to make the dealer continue hitting if there hand is below 17
            while dealerHandValue < 17:
                dealerHand.addCard(deck.deal(1))
                dealerHandValue = dealerHand.getValue()
            
            # shows all the cards after for the dealer
            dealerHand.display(showAllDealerCards=True)

            if self.checkWinner(playerHand, dealerHand):
                continue

            print("Final Results")
            print("Your Hand: ", playerHandValue)
            print("Dealers Hand: ", dealerHandValue)
            
            # to make the game be over
            self.checkWinner(playerHand, dealerHand, True)

        print("\nThanks for playing!")

    # checks who is the winner of the game and returns true if there is a winner
    def checkWinner(self, playerHand, dealerHand, gameOver = False):
        if not gameOver:
            if playerHand.getValue() > 21:
                print("You busted. Dealer wins! :)")
                return True
            elif dealerHand.getValue() > 21:
                print("Dealer busted. You win! :)")
                return True
            elif dealerHand.isBlackJack() and playerHand.isBlackJack():
                print("You both had a Blackjack! Tie! :)")
                return True
            elif playerHand.isBlackJack():
                print("You have Blackjack! You Win! :)")
                return True
            elif playerHand.isBlackJack():
                print("Dealer has Blackjack! Dealer Wins! :)")
                return True
        else:
            if playerHand.getValue() > dealerHand.getValue():
                print("You Win! :)")
            elif playerHand.getValue() == dealerHand.getValue():
                print("Tie!")
            else:
                print("Dealer Wins.")
            return True
        return False

g = Game()
g.play()