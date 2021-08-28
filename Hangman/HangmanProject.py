#Title screen function
def titleScreen():
    hangmanWord = """
  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/                       
    """
    print(hangmanWord)
    print('MENU:')
    print('1. Single Player')
    print('2. Two Player')
    print('3. Leaderboard')
    print('4. Add Word')
    print('5. Help')
    print('6. Quit')
    playerChoice = eval(input('What would you like to do? '))
    print('\n')
    return playerChoice

#the pazzaz
def displayHangman(tries):
    stages = [  #state 6 (final state)
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                  ---""",
                #state 5
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                  ---""",
                #state 4
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                  ---""",
                #state 3
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                  ---""",
                #state 2
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                  ---""",
                #state 1
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                  ---""",
                #state 0 (initial state)
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                  ---"""
    ]
    return stages[tries]

#finding the number of rows in the word bank document
def numLinesWordBank(iFile):
    numLines = sum(1 for line in iFile) # open('wordBank.txt','r'))
    return numLines

#a simple random number generator using the total length of the word bank
def getRandomNumber(numRow):
    from random import randrange as rr
    upperLimit = numRow+1
    randNum = rr(1,upperLimit)
    return randNum

#open word bank
def openWordBank():
    iFile = open('wordBank.txt','r')
    return iFile

#get random number based on number of lines
def getWord(iFile):
    numRow = numLinesWordBank(iFile)
    randNum = getRandomNumber(numRow)
    #makes reading lines easier
    import linecache
    wordAndDef = linecache.getline('wordBank.txt',randNum)
    wordAndDefSplit = wordAndDef.split('|')
    randWord = wordAndDefSplit[0]
    randDef = wordAndDefSplit[1]
    randWord = randWord.upper()
    iFile.close()
    return randWord, randDef

#running the game, probably the most important function!!!  
def playHangman(word, wordDef = 'null'): 
    wordCompletion = '_' *len(word)
    guessed = False
    guessedLetters = []
    guessedWords = []
    triesLeft = 6
    defNeeded = False
    print(displayHangman(triesLeft))
    print(" ".join(str(x) for x in wordCompletion),'\n')
    while not guessed and triesLeft > 0:
        guess = input('Please select a letter A-Z or guess the word: ').upper()
        if len(guess) == 1 and guess.isalpha():
            if guess in guessedLetters:
                print('You already guessed this letter', guess)
                sassyRemarks()
            elif guess not in word:
                print('Sorry', guess, 'is not a letter in the word, try again')
                triesLeft -= 1
                guessedLetters.append(guess)
            else:
                print('YES!', guess, 'is a letter in the word')
                guessedLetters.append(guess)
                wordAsList = list(wordCompletion)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    wordAsList[index] = guess
                wordCompletion = "".join(wordAsList)
                if "_" not in wordCompletion:
                    guessed = True
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessedWords:
                print("You already guessed the word", guess)
            elif guess != word:
                print(guess, "is not the word.")
                sassyRemarks()
                triesLeft -= 1
                guessedWords.append(guess)
            else:
                guessed = True
                wordCompletion = word
        else:
            print("Not a valid guess.")
            sassyRemarks()
        print(displayHangman(triesLeft))
        print(" ".join(str(x) for x in wordCompletion))
        print("\n")
        if wordDef != 'null' and triesLeft == 1:
            print('Looks like you\'re down to your last try!')
            print('Here\'s a little hint, the definition is: ' + wordDef)
            defNeeded = True
    if guessed:
        print("Congrats, you guessed the word! You win!\n")
        win = True
    else:
        print("Sorry, you ran out of tries. The word was " + word + ". Better luck next time!")
        sassyRemarks()
        sassyRemarks()
        sassyRemarks()
        win = False
    return win, word, defNeeded

#getting user info if their score quailifies for the leaderboard
def getPlayerName():
    playerName = input('\nPlease enter your initials for the LEADERBOARD: ').upper()
    while(True):
        if len(playerName) != 3 or playerName.isalpha() == False:
            print('##########ERROR PLEASE ENTER YOUR INITIALS IN THIS FORMAT (EX: AAA)##########')
            sassyRemarks()
            playerName = input('Please enter your initials:')
        else:
            break
    return playerName

#sorting yay!
def sortLeaderboard():
    import pandas
    with open('leaderboard.txt', 'r') as f:
        text = [line.split() for line in f]
    #going from str in txt file to string
    for i in range(len(text)):
        text[i][1] = float(text[i][1])
    df = pandas.DataFrame(text, columns = ['NAME:', 'SCORE:'])
    #sorting us pandas
    dfSorted = df.sort_values("SCORE:", ascending=True) # Sort by values of the SCORE column2
    #store NAME: column as list
    nameSorted = dfSorted['NAME:'].tolist()
    #store SCORE: column as list
    scoreSortedFloat = dfSorted['SCORE:'].tolist()
    #new list to store strings in
    scoreSorted = [] 
    for x in scoreSortedFloat: 
	    scoreSorted.append(str(x)) 
    from itertools import zip_longest #helps combine two lists into list of lists
    leaderboardList = list(zip_longest(nameSorted,scoreSorted, fillvalue=""))
    #getting the top 10
    leaderboardListTrimmed = leaderboardList[:10]
    return leaderboardListTrimmed

#replacing leaderboard.txt with updated leaderboard
def updateLeaderboard(updatedLeaderboard):
    data = updatedLeaderboard  
    #create the pandas DataFrame  
    import pandas as pd 
    df = pd.DataFrame(data, columns = ['NAME:', 'SCORE:'])
    #import numpy
    import numpy as np
    np.savetxt(r'leaderboard.txt', df.values, fmt='%s')

#prints leaderboard
def getLeaderboard():
    iFileR = open('leaderboard.txt', 'r')
    print('\n\n*********LEADERBOARD*********')
    print('_____________________________')
    print('\n', '     NAME: ', '    SCORE:\n')
    for i, line in enumerate(iFileR):
        name, score = line.split()
        print(i+1,'.   ', name, '   ', score)
        print('\n')
    iFileR.close()

 #main leaderboard functions   
def leadboard(timeTaken, lowestName, lowestScore):
    print('Congradulations your time:', timeTaken, 'seconds, is one of the fastest recorded')
    print('You kicked', lowestName, 'score of: ', lowestScore, 'outa the top 10!!!!')
    playerName = getPlayerName()
    iFileTwoA = open('leaderboard.txt', 'a')
    score = str(timeTaken)
    iFileTwoA.write(playerName + ' ' + score +'\n')
    iFileTwoA.close()
    updatedLeaderboard = sortLeaderboard()
    updateLeaderboard(updatedLeaderboard)
    getLeaderboard()

#takes the bottom time from the leaderboad and compares it to the users time
def fastEnough(timeTaken):
    iFileR = open('leaderboard.txt', 'r')
    lines=iFileR.readlines()
    lowScore = lines[9]
    name, lowestScoreStr = lowScore.split()
    lowestScore = float(lowestScoreStr)
    iFileR.close()
    return name, lowestScore

def outputIfNotTopTen(timeTaken):
    if timeTaken <= 45:
        print('Good job on winning, but you were not fast enought to crack the top 10 times ever!')
        print('\n\t\t!!!!!YOU GOTTA BE QUICKER THAN THAT!!!!!\n')
    elif timeTaken > 45 and timeTaken <= 60:
        print('Under a minute, but over 45 seconds')
        print('Good, but not great')
        print('It\'s like getting a handjob, its fine but we all know what you really want')
        print('S/O to gambino for that zinger')
    elif timeTaken >= 60 and timeTaken <= 100:
        print('It took you over a minute to solve this..')
        print('Congrats you\'re a genius....if you\'re in the 3rd grade')
        sassyRemarks()
        print()
    elif timeTaken > 100 and timeTaken <= 150:
        print('This took you close to if not over two minutes to solve this')
        print('Idk if says more about you or more about me')
        print('I mean why am I letting morons use my computer?')
        sassyRemarks()
        print()
    elif timeTaken > 150 and timeTaken <= 240:
        print('Almost 3 minutes?')
        print('TOUGH LOOKS')
        print('I hope you simply got up to go to the bathroom in the middle of the game')
        print('That\'s the only logical reason I can think of for solving it that slow')
        sassyRemarks()
        print()
    else:
        print('I wanna say something here, but honestly I not gonna throw insults at you')
        print('Since your life is already an insult to everyone around you')
        sassyRemarks()
        print()

#Single player game mode
def runSinglePlayer():
    print('****************SINGLE PLAYER****************\n')
    iFile = openWordBank()
    randWord, randDef = getWord(iFile)
    print('\t The CPU has selected a word')
    print('     You can only choose WRONG 6 times!')
    print('\t       CHOOSE WISELY!!!\n')
    input('Enter any key to start the game! ')
    #allows the program to time how long it takes user to solve the hangman
    import time
    start = time.time()
    win, word, defNeeded = playHangman(randWord, randDef)
    end = time.time()
    timeTaken = round((end - start),5)
    if win == True:
        print('You guessed', word ,'in', timeTaken, 'seconds\n')
        if defNeeded == False:
            print('FUN FACT:')
            print('The definition of', word, 'is:', randDef)
        lowestName, lowestScore = fastEnough(timeTaken)
        if timeTaken < lowestScore:
            leadboard(timeTaken, lowestName, lowestScore)
        else:
            outputIfNotTopTen(timeTaken)
    playAgainChoice = playAgain()
    return playAgainChoice

#Getting TP basic info
def getTwoPlayerInfo():
    print('\n     ******************TWO PLAYER******************\n')
    print('So either they\'re two of you or you\'re just really lonely')
    print('\t   Or you couldn\'t handle the CPU\n')
    print('  Each player will enter a word for the other to solve\n')
    print('\t #######!!!fastest time wins!!!#######\n')
    playerOne = input('Player One please enter your name: ').upper()
    playerTwo = input('\nPlayer Two please enter your name: ').upper()
    print('\nWELCOME ' + playerOne.upper() + ' & ' +playerTwo.upper() + '\n')
    return playerOne, playerTwo

#Get's a users word (different than the other function tho this one is for TP)
def getWordsTP(player, otherPlayer):
    while(True):
        playerWord = input(player + ', Please enter your word: ').upper()
        if len(playerWord) < 4 or playerWord.isalpha() == False:
            print('Either you fucked up or the word is to short')
            print('Let me guess you wanted to put in a 3 letter word')
            print('Your words must be AT LEAST 4 letters long')
            print('Please keep in mind that there are no special characters/numbers in words')
            print('Additional note: this is hangman leave your weird foriegn accent marks at home\n')
        else:
            if len(playerWord) == 4:
                print('This better be a pretty unique 4 letter word')
                print('Shorter words are usually easier to solve')
                print('Are you trying to loose?\n')
            choice = input('Please confirm that ' + playerWord.upper() + ' is indeed your word (Y/N)? ').upper()
            if choice == 'Y':
                print('\nGOOD LUCK!!!')
                break
            elif choice == 'N':
                print('well let\'t try again shall we?')
            else:
                print('Well you couldn\'t even enter a Y or N')
                print('This is gonna be an easy dub for ' + otherPlayer +' it looks like')
                print('Try agian ya dingbat')
    return playerWord

#Getting players word
def getTwoPlayerWords(playerOne, playerTwo):
    print(playerOne + ' will enter their word first')
    print(playerTwo + ' please avert your eyes like you\'re Indiana Jones and the Screen is the Arc of the Covenant\n')
    playerOneWord = getWordsTP(playerOne, playerTwo)
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    print('_______________________________________________________________')
    print('\n'+ playerTwo + '\'s turn!!!')
    print(playerOne + ' please avert your eyes like you\'re looking at ' + playerTwo + '\'s mama heyyyyyyooooooo\n')
    playerTwoWord = getWordsTP(playerTwo, playerOne)
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    return playerOneWord, playerTwoWord

def resultsTP(playerOne, playerTwo, playerOneTime, playerTwoTime, timeDifference):
    print('The results are in!!!!!')
    input('Please enter any key to see who is a WINNER and who is a LOSER: ')
    print('\n_______________________________________________________________\n')
    #player one wins
    if playerOneTime < playerTwoTime:
        print()
        print('Congradulation ' + playerOne)
        print('Looks like you were able to beat ' + playerTwo + ' with a time of ', playerOneTime, 'seconds')
        print('That was', timeDifference, 'seconds better than '  + playerTwo)
        print(playerTwoTime, 'wasn\'t fast enough ' + playerTwo + ' gotta be quicker than that!!!')
    #player two wins
    elif playerOneTime > playerTwoTime:
        print()
        print('Congrats ' + playerTwo + '!!!')
        print('Looks like you were able to beat ' + playerOne + ' with a time of ', playerTwoTime, 'seconds')
        #to account for the extreme p1 time set if p1 looses
        if timeDifference < 1000000000000:
            print('That was', timeDifference, 'seconds better than ' + playerOne)
            print('Gotta be quicker than that ' + playerOne)
    #tie (this will never happen)
    elif playerOneTime == playerTwoTime:
        print()
        print('I have no words for this other than HOLY FUCKING SHIT')
        print('You somehow managed to get the same time')
        print(playerOne + ' got', playerOneTime, 'seconds & ' + playerTwo + ' got', playerTwoTime, 'seconds')
        print('IDK how that happened, but y\'all best get your asses of the computer and go get some lottery tickets')
        print('*NOTE: I\'m entitled to at least 3% of the winnings')

#1v1 rust quickscope only! no hard scoping you fuckboi
def runTwoPlayer():
    playerOne, playerTwo = getTwoPlayerInfo()
    playerOneWord, playerTwoWord = getTwoPlayerWords(playerOne, playerTwo)
    print('\n_______________________________________________________________\n')
    print('Both players have entered their words\n')
    input(playerOne + ' When you are ready enter any key and the clock will start: ')
    print('GOODSPEED!')
    #allows the program to time how long it takes user to solve the hangman
    import time
    start = time.time()
    #not sure how to deal with this?
    win, word, defNeeded = playHangman(playerTwoWord)
    end = time.time()
    playerOneTime = round((end - start),5)
    #setting these up for later
    k = True
    j = True
    if win == False:
        print('\nWell looks like '+ playerOne +' is garbage at hangman and couldn\'t even figure out the word')
        print('All you have to do ' + playerTwo + ' is guess the word')
        print('The heat death of the universe could come and go and you would still win if you finished eventually')
        print('See how fast you can get' + playerOne + '\'s word for fun!!!\n')
        #makes it impossible for p1 to win
        playerOneTime = 10000000000000000000
        j = False
    else:
        print('Hey you got the word!!!')
        print(playerTwo + ' maybe pick a harder word than ' + word + ', it helps to read so find yourself a book and expand that vocabulary!')
    print('\nYour turn ' + playerTwo)
    input('When you are ready enter any key and the clock will start: ')
    #run it back
    start = time.time()
    #not sure how to deal with this?
    win, word, defNeeded = playHangman(playerOneWord)
    end = time.time()
    playerTwoTime = round((end - start),5)
    timeDifference = round(abs(playerOneTime - playerTwoTime),5)
    if win == False:
        k == False 
        if j == True:
            #if p2 looses and p1 won
            print('\n' + playerTwo + ' what happened? You couldn\'t even figure out the word')
            print('Let me guess...the vocab section was your lowest score on the SAT')
            print('Better luck next time looks like ' + playerOne + ' walks away with the dub and a time of', playerOneTime, 'seconds')
            print('Maybe y\'all could do a best of 3?\n')
            playAgainChoice = playAgain()
            return playAgainChoice
    #both fail to get word
    if j == False and k == False:
        print('\nWell you both fucking suck apparently')
        sassyRemarks()
        print('Guess the only thing to do is run it back!!!')
        playAgainChoice = playAgain()
        return playAgainChoice
    else:
        resultsTP(playerOne, playerTwo, playerOneTime, playerTwoTime, timeDifference)
    print('\n_______________________________________________________________\n')
    print('Thanks for playing, hope you both had fun!!!\n')
    playAgainChoice = playAgain()
    return playAgainChoice

#just the leaderboard, nothing else to see here
def runLeaderboard():
    print('The leaderboard is based on how quickly you solve the hangman')
    print('While some words are definately easier than others (rng\'s a bitch ain\'t she?)')
    print('My lazy ass didn\'t feel like weighing every god damn word in the word bank')
    getLeaderboard()
    input('press any key to exit leaderboard...just not esc...or ctrl + alt + delete ')
    print()
    playAgainChoice = playAgain()
    return playAgainChoice

#Getting the new word and def
def getWordandDef():
    print('please note: new words CANNOT be propper nouns')
    while(True):
        newWord = input('Please enter new word: ').lower()
        if len(newWord) < 4 or newWord.isalpha() == False:
            print('Either you fucked up or the word is to short')
            print('Let me guess you wanted to put in a 3 letter word')
            print('New words must be AT LEAST 4 letters long')
            print('Please keep in mind that there are no special characters/numbers in words')
            print('Additional note: this is hangman leave your weird foriegn accent marks at home')
        else:
            if len(newWord) == 4:
                print('\nThis better be a pretty unique 4 letter word')
                print('Remember people have 6 guesses so the shorter the word usually means it\'s easier to solve\n')
            print(newWord.upper())
            choice = input('\nAre you 100% positive this is the CORRECT SPELLING of the word ' + newWord.upper() + ' (Y/N)? ').upper()
            if choice == 'Y':
                print('Hope you\'re right!!!')
                break
            elif choice == 'N':
                print('well let\'t try again shall we?')
            else:
                print('\nThat wasn\'t a "Y" or a "N" so we\'re just gonna quit before you mess anything else up\n')
                sassyRemarks()
                return False, False
    print('Now we\'re gonna do the same but with the definition!')
    print('PLEASE KEEP THE DEFINITION IN LOWER CASE')
    while(True):
        newDef = input('Please enter the definition of ' + newWord.upper() +': ').lower()
        print(newDef)
        choice = input('\nAre you 100% positive this is the CORRECT SPELLING/DEFINITION of,\n' + newDef + ',(Y/N)? ').upper()
        if choice == 'Y':
            print('Hope you\'re right!!!')
            break
        elif choice == 'N':
            print('well let\'t try again shall we?')
        else:
            print('\nThat wasn\'t a "Y" or a "N" so we\'re just gonna quit before you mess anything else up\n')
            sassyRemarks()
            return False, False
    print('Last Chance!!!\n')
    print(newWord.upper())
    print(newDef, '\n')
    finalChoice = input('Are you 100% positive this is the right WORD/DEFINITION and EVERYTHING is spelled CORRECTLY, (Y/N)? ').upper()
    if finalChoice == 'Y':
        print('\nOkay I trust ya!!!')
        return newWord, newDef
    else:
        print('\nWell you can always try again later...\n')
        return False, False

#testing if new word is already in the word bank or not
def isWordInWordBank(newWord):
    testWordBank = list()
    filename = open('wordBank.txt', 'r')
    for line in filename:
        words = line.split('|')
        testWordBank.append(words[0])
    res = [ele for ele in testWordBank if(ele in newWord)]
    wordOkay = not bool(res)
    return wordOkay

#adding new word to word bank and then sorting the word bank alphabetically
def addingNewWord(newWord, newDef):
    wordOkay = isWordInWordBank(newWord)
    if wordOkay == False:
        print('\nSorry ' + newWord + ' is already in the wordbank!')
        input('Enter any key to return you to main menu ')
        return wordOkay
    else:
        wordBank = open('wordBank.txt', 'a')
        wordBank.write(newWord + '|' + newDef + '\n')
        wordBank.close()
        filename = 'wordBank.txt'
        newWordBank = list()
        with open (filename) as fin:
            for line in fin:
                newWordBank.append(line.strip())
        newWordBank.sort()
        with open (filename, 'w') as fout:
            for band in newWordBank:
                fout.write(band + '\n')
        return wordOkay


#for people that think they can add a new word plus definition
#can't wait to sort this alphabetically
def runNewWord():
    print('\n*********ENTER NEW WORDS/DEFINITIONS*********\n')
    while(True):
        print('So you wanna enter a new word huh?')
        choice = input('Are ya sure? (Y/N)?').upper()
        if choice != 'Y' and choice != 'N':
            print('If I can\'t trust you with entering Y or N')
            print('I sure as hell ain\'t letting you enter in a new word')
            sassyRemarks()
            print('GTFO my GAME ya NUMSKULL')
            playAgainChoice = 'X'
            return playAgainChoice
        elif choice == 'N':
            playAgainChoice = playAgain()
            return playAgainChoice
        else:
            print('Ok better get you dictionary out!!!')
            print('& for the love of god check your')
            print('########!!!!!SPELLING!!!!!#########\n\n')
        newWord, newDef = getWordandDef()
        if newWord == False and newDef == False:
            print('Something went wrong while entering new word')
            print('Returning you to home screen!')
            return
        else:
            print('Adding', newWord, '& it\'s definition to the word bank!!!')
        wordOkay = addingNewWord(newWord, newDef)
        if wordOkay == False:
            playAgainChoice = 'Y'
            return playAgainChoice
        else:
            print(newWord + ' Has been added to the wordbank')
            while(True):
                newChoice = input('Would you like to add another word? (Y/N)?').upper()
                print()
                if newChoice == 'Y':
                    print('Lets run it back!\n')
                    break
                elif newChoice == 'N':
                    print('Thanks for contributing to the word bank!!!\n')
                    playAgainChoice = playAgain()
                    return playAgainChoice
                else:
                    print('\nThat wasn\'t a "Y" or a "N" try again (rhyme not intended)\n')
        
#single player help
def singlePlayerHelp():
    print('\n**********************Single Player Help**********************\n')
    print('Single player pits the user against the CPU')
    print('The CPU chooses a random word from the word bank for the player to solve')
    print('You will see "_" lines next to an empty gallow')
    print('The dashed lines represent the number of letters in the word the CPU choose')
    print('You then enter any letter or a word with the same number of letters')
    print('If the letter is in the word, the "_" will be replaced by the letter')
    print('e.g. if the word is "POWER" and one enters the letter "e"')
    print('The result will look like "_ _ _ E _"')
    print('If the letter is not in the word than a body part gets added to the gallow')
    print('You have 6 incorrect guesses before the body is complete and you loose the game')
    print('Head, Body, Right Arm, Left Arm, Right Leg, Left Leg')
    print('If you guess all of the letters correct or you enter the full word correctly')
    print('YOU WIN THE GAME')
    print('Your score is recorded as the time it took you to solve the hangman')
    print('Once the program runs the clock starts')
    print('The clock then finishes only once the word is complete')
    print('If you fails to guess the word no score is recorded')
    print('If you score is fast enough the you are entered into the leaderboard')
    print('More on that later')
    print('Hopefully this gave you a basic idea of what hangman is and how to play')
    print('If you have any other questions just google them haha')
    input('Enter any key to continue: ')

#two player help
def twoPlayerHelp():
    print('\n************************Two Player Help***********************\n')
    print('This game mode is designed to have two people race each other')
    print('Both players will enter their name and a word for the other to solve')
    print('e.g. name: "Bill" and word: "Pancakes"')
    print('Please note that the word CANNOT be a proper noun')
    print('Once the program has the required info it will run 2 games of hangman')
    print('Player One will go first, trying to solve Player Two\'s word')
    print('Then vice-versa')
    print('If both players guess correctly the fastest time wins')
    print('If only one player guesses correctly than obviously they win')
    print('If both players loose, well thats self explanitory')
    input('Enter any key to continue: ')

#leaderboard help
def leadboardHelp():
    print('\n***********************Leaderboard Help***********************\n')
    print('The leaderboard holds the best times ever recorded on this game')
    print('You gotta be pretty quick to be on the leaderboard')
    print('There are some really tough words to solve quickley')
    print('Yet alone solve')
    print('I could have weighed each individual word on how difficult it was,')
    print('but there are over 1250 words and I am way to lazy to do that')
    print('Plus I am not sure that I would know how to weigh them')
    print('Mind that rant leaderboards aren\'t that hard to understand tho')
    input('Enter any key to continue: ')

#help adding new words and definitions to the bank
def newWordHelp():
    print('\n************************New Word Help*************************\n')
    print('This allows the user to add a new word to the word bank')
    print('This can be any word in the English Language')
    print('Excluding proper nouns e.g. Santana, Anna, Canada, etc...')
    print('Additionally the user must provide a definition for the word')
    print('Just copy the definition from google please, it works the best')
    input('Enter any key to continue: ')

#kills leadboard
def deleteLeaderboard():
    #deletes all contents of leaderboard
    open('leaderboard.txt', 'w').close()
    #add default (AAA with times of 999.99999)
    #like old school arcade games
    fakeUser = 'AAA'
    fakeScore = '999.99999'
    leadboard = open('leaderboard.txt', 'a')
    for i in range (10):
        leadboard.write(fakeUser + ' ' + fakeScore + '\n')
    leadboard.close()

#honestly this page is just here as a front to reseting the leaderboard
def helpHelp():
    print('\n**************************Help Help***************************\n')
    print('Lmao I doubt you need a help page on the help page')
    print('Hopefully you now understand the game of Hangman better')
    print('Congrats you have now complete the all help pages!!! YAY!!!\n')
    resetLeaderboard = input('Enter any key to head back to the main menu ')
    if resetLeaderboard == 'b0F$qZD4kn*':
        print('\nReally hope this is Elias, otherwise how the fuck did you get this password?')
        print('Also how did you know this page even exsisted?\n')
        print('\n************************Admin Services************************\n')
        print('To edit leadboard enter L')
        print('To add a sassy remark press S')
        print('To return to main menu enter any other key')
        adminChoice = input('What do you want to do? ').upper()
        if adminChoice == 'S':
            while(True):
                newSass = input('Enter your new sassy phrase (capitalize the first letter) ')
                isRight = input('"' + newSass + '" are you sure this is right(Y/N)? ').upper()
                if isRight == 'Y':
                    filename = open('sassyRemarks.txt', 'a')
                    # Append 'hello' at the end of file
                    filename.write(newSass + '\n')
                    # Close the file
                    filename.close()
                    print('added ' + newSass + ' to sassyRemarks.txt')
                    break
                elif isRight == 'N':
                    print('Okay lets try again')
                    print('Note to break this loop enter a letter other than "y" or "n"')
                else:
                    print('if you didn\'t enter "y" or "n" than I assume you wanna return to main menu')
                    break
        elif adminChoice == 'L':
            while(True):
                newChoice = input('Are you 100% sure you would like to reset the leaderboard? (Y/N)? ').upper()
                print()
                if newChoice == 'Y':
                    input('\nLast Change only way out at this point is to kill the terminal! Enter any key to confirm leadboard reset ')
                    print()
                    deleteLeaderboard()
                    print('!!!Leadboard is now RESET!!!\n')
                    input('Enter any key to return to main menu ')
                    break
                elif newChoice == 'N':
                        break
                else:
                    print('\nThis probably isn\'t Elias cause he wouldn\'t make that mistake!')
                    print('Just in case he\'s drunk or something, try again\n')
        else:
            print()
    else:
        return

#for the idiots who apperently don't know how to play hangman
#seriously who never played hangman growing up?
def runHelp():
    print('\n************************HELP PAGE(S)**************************\n')
    print('This section will give you all the basic info for each gamemode')
    print('In addition to other options, & little tips/tricks to hangman')
    singlePlayerHelp()
    twoPlayerHelp()
    leadboardHelp()
    newWordHelp()
    helpHelp()

#rng for sassy remarks
def rngSassyRemarks():
    from random import randrange as rr
    randNum = rr(1,8)
    return randNum

#sassy remarks generator
def sassyRemarks():
    randNum = rngSassyRemarks()
    if randNum == 4:
        filename = open('sassyRemarks.txt', 'r')
        numRow = sum(1 for line in filename)
        randNum = getRandomNumber(numRow)
        #makes reading lines easier
        import linecache
        sassyRemarks = linecache.getline('sassyRemarks.txt',randNum)
        return(print(sassyRemarks))

#duh
def playAgain():
    while(True):
        playAgain = input('Would you like to play again (Y/N)? ').upper()
        if playAgain != 'Y' and playAgain != 'N':
            print(playAgain)
            print('#######ERROR PLEASE ENTER: Y for Yes or N for No########')
            print('Seriously does your dumbass not know the alphabet???')
        else:
            break
    return playAgain

#DUH!?
def runQuit():
    quitScreen = """
 _____ _                 _           __                   _             _             _ _ _ 
|_   _| |               | |         / _|                 | |           (_)           | | | |
  | | | |__   __ _ _ __ | | _____  | |_ ___  _ __   _ __ | | __ _ _   _ _ _ __   __ _| | | |
  | | | '_ \ / _` | '_ \| |/ / __| |  _/ _ \| '__| | '_ \| |/ _` | | | | | '_ \ / _` | | | |
  | | | | | | (_| | | | |   <\__ \ | || (_) | |    | |_) | | (_| | |_| | | | | | (_| |_|_|_|
  \_/ |_| |_|\__,_|_| |_|_|\_\___/ |_| \___/|_|    | .__/|_|\__,_|\__, |_|_| |_|\__, (_|_|_)
                                                   | |             __/ |         __/ |      
                                                   |_|            |___/         |___/       
    """
    print(quitScreen)
    
#could be cleaner
def main():
    #show title screen for hangman
    while(True):
        while(True):
            playerChoice = titleScreen()
            if playerChoice <= 6 and playerChoice > 0:
                break
            else:
                print("#############ERROR PLEASE ENTER NUMBER 1-6#############")
                print('it\'s not that hard')
    #Which program to run
        if playerChoice == 1:
            playAgain = runSinglePlayer()
            if playAgain == 'N':
                runQuit()
                break
        if playerChoice == 2:
            playAgain = runTwoPlayer()
            if playAgain == 'N':
                runQuit()
                break
        if playerChoice == 3:
            playAgain = runLeaderboard()
            if playAgain == 'N':
                runQuit()
                break
        if playerChoice == 4:
            playAgain = runNewWord()
            if playAgain == 'N':
                runQuit()
                break
            elif playAgain == 'X':
                break
        if playerChoice == 5:
            runHelp()
        if playerChoice == 6:
            print('Why\'d you even start me up???')
            runQuit()
            break


if __name__ == "__main__":
    main()