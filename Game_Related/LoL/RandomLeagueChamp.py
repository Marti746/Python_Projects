import random

# Function for printing the instructions out for the game
def printInstructions():
    print("Welcome to random League Champ Picker")
    print('''You can choose between
          1. Top
          2. Jungle
          3. Mid
          4. ADC
          5. Support
        ''')

# Function to get the list for the random champion
def getList():
    topList = ['Jax','Aatrox','Singed','Malphite','Teemo','Fiora','Trundle','Gwen','Mordekaiser',
               'Riven','Kled','Kayle','Tryndamere','Poppy','Kennen','Rumble','Nassus','Urgot',
               'Vayne','Akshan','Quinn','Rengar','Ornn','Vladmir','Warwick','Udyr','Maokai',
               'Gnar','Tahm Kench','RTyze','Gragas','Shen','Sylas','Pantheon','LeBlanc','Akali',
               'Dr. Mundo','Irelia','Cho Gath','Camille','Gangplank','Yone','Olaf','Sett','Yorick',
               'Volibear','Sion','KSante','Jayce','Darius','Garen','Renekton','Illaoi']
    jgList = ['Evelynn','Graves','Rengar','Master Yi','Briar','Bel Veth','Lee Sin','Lillia',
              'Xin Zhao','Jax','Rammus','Ekko','Ivern','Kindred','Brand','Viego','Rek Sai',
              'Elise','Vi','Trundle','Gwen','Poppy','Nocturne','Warwick','Kha Zix','Nunu',
              'Maokai','Udyr','Talon','Hecarim','Wukong','Taliyah','Fiddlesticks','Sejuani',
              'Shyvana','Nidalee','Amumu','Diana','Gragas','Zac','Jarvan IV','Shaco','Sylas',
              'Kayn','Karthus']
    midList = ['Tahm Kench','Neeko','Ahri','Annie','Talon','Camille','Anivia','Katarina',
               'Cassiopia','Fizz','Irelia','LeBlanc','Malzahar','Kassadin','Zed','Sett',
               'Annie','Akali','Yone','Ekko','Twisted Fate','Vladmir','Akshan','Zoe','Sylas',
               'Vex','Galio','Yassuo','Lissandra','Qiyana','Hwei','Syndra','Azir','Viktor',
               'Orianna','Xerath','Lux','Malzhar','Jayce','Veigar','Aurelion Soul']
    adcList = ['Aphelios', 'Ashe','Caitlyn','Corki','Draven','Ezreal','Jhin','Jinx','Kai Sa',
               'Kalista','Kog Maw','Lucian','Miss Fortune','Samira','Sivir','Tristana','Twitch',
               'Varus','Vayne','Xayah','Zeri']
    # List of supports in League to pick
    supList = ['Brand','Thresh','Sona','Nautilus','Karma','Bard','Lulu','Pyke','Blitzcrank',
                'Nami','Morgana','Zyra','Leona','Zilean','Alistar','Taric','Janna','Tahm Kench',
                'Rakan','Braum','Vel Koz','Lux','Soraka','Fiddlesticks','Hwei','Senna','Twitch',
                'Tahm Kench','Xerath']

    # Gets the user input for the list they want then checks to see what list it is
    listChoice = int(input("Enter your role choice (1-5): "))
    if listChoice == 1:
        characterChoice = random.choice(topList)
    elif listChoice == 2:
        characterChoice = random.choice(jgList)
    elif listChoice == 3:
        characterChoice = random.choice(midList)
    elif listChoice == 4:
        characterChoice = random.choice(adcList)
    else:
        characterChoice = random.choice(supList)

    return characterChoice

printInstructions()
champion = getList()
print("Your random champion is", champion)