from re import L
import nltk.corpus
from allWords import allWordleWords, falseWords

numLetters = 5

def readSysWord(systemFile):
    '''
    Description: reads in the system dictionary
    Parameters: systemFile ("/usr/share/dict/words"- probably a text file)
    Returns: dictionaryList (list of all words in the dictionary)
    '''

    sFile = open(systemFile, 'r')

    dictionaryList = []
    for word in sFile:
        indWord = word.strip()
        #makes sure the word has only characters that are letters
        if indWord.isalpha() and len(indWord) == numLetters:
            dictionaryList.append(indWord.lower())

    sFile.close()

    return dictionaryList

def getResult():
    while True:
        VALID = True
        result = input("\nPlease enter result: ").lower()
        if len(result) == numLetters*2 and result.isalpha():
            for i in range(0,numLetters,1):
                if result[2*i] not in ["f","y","g"]:
                    VALID = False
        else:
            VALID = False

        if not VALID:
            print("Sorry there was an error")
        if VALID:
            break

    return result

def parseResults(result, knownSpotsT, knownSpotsF, knownLetters, notPresent):
    word = ""
    for i in range(0,numLetters,1):
        letter = result[2*i+1]
        word+=letter

    for i in range(0,numLetters,1):
        letter = word[i]
        if result[2*i] == "y":
            if letter not in knownLetters:
                knownLetters.append(letter)
            knownSpotsF.append(f"{i+1}{letter}")
        elif result[2*i] == "g":
            if letter not in knownLetters:
                knownLetters.append(letter)
            knownSpotsT.append(f"{i+1}{letter}")
        elif result[2*i] == "f":
            # if letter not in notPresent and letter not in knownLetters and letter not in word[:i] and letter not in word[i+1:]:
            if letter not in notPresent and letter not in knownLetters:
                NOTPRESENT = True
                for i in range(len(word)):
                    if word[i] == letter:
                        if result[2*i] == "y" or result[2*i] == "g":
                            NOTPRESENT = False
                            break
                if NOTPRESENT:
                    notPresent.append(letter)
        else:
            print("ERROR, please restart")
            quit()

    return

def findPossibilities(knownSpotsT, knownSpotsF, knownLetters, notPresent, dictionaryList):
    possibleWords = []

    for word in dictionaryList:
        WORKS = True
        for comb in knownSpotsT:
            position = int(comb[0])-1
            letter = comb[1]
            if word[position] != letter:
                WORKS = False
        for comb in knownSpotsF:
            position = int(comb[0])-1
            letter = comb[1]
            if word[position] == letter:
                WORKS = False
        for letter in knownLetters:
            if letter not in word:
                WORKS = False
        for letter in notPresent:
            if letter in word:
                WORKS = False
        if WORKS:
            possibleWords.append(word)

    return possibleWords

def countLetters(dictionaryList, alphabet):
    countList = []

    for letter in alphabet:
        countList.append(0)

    for word in dictionaryList:
         for letter in word:
             if letter in alphabet:
                 index = alphabet.index(letter)
                 countList[index] += 1

    for i in range(len(alphabet)):
        print(f"{alphabet[i]}: {countList[i]}")

def rateWords(possibleWords, dictionaryList, knownLetters, notPresent):
    scoreDict = {}
    letterScores = {}
    for word in possibleWords:
        for letter in word:
            if letter in letterScores.keys():
                letterScores[letter] +=1
            else:
                letterScores[letter] = 1
    maxAppearanceNum = letterScores[max(letterScores, key=lambda key: letterScores[key])]
    print(letterScores)
    
    for word in dictionaryList:
        score = 0.0
        for letter in word:
            #bad if word is already known
            score = score-0.5 if letter in knownLetters else score
            #bad if words is known to be not present already
            score = score-1 if letter in notPresent else score
            #bad if there are many repeats in word
            score -= word.count(letter)
            #good if letter appears a lot in possible words
            if letter not in knownLetters and letter in letterScores.keys():
                score += letterScores[letter]*3/maxAppearanceNum
        scoreDict[word] = score
    
    return scoreDict



def main():

    # dictionaryList = readSysWord("/usr/share/dict/words")
    dictionaryList = allWordleWords + falseWords

    #for knownSpotsT, put number and letter for letters you know
    #for knownSpotsF, put number and leter of letter you know isn't there
    #for knownLetters, put letters you know are there
    #for not present, put letters that aren't there

    knownSpotsT, knownSpotsF, knownLetters, notPresent = [], [], [], []

    while True:
        print("\nInstructions: enter given information with designation first followed by letter")
        # print("Enter 'stern' for your first word, and 'yclad' for the second")
        print("f for grey, y for yellow, g for green")

        result = getResult()
        parseResults(result, knownSpotsT, knownSpotsF, knownLetters, notPresent)

        # print("\nData in case the code crashes:")
        # print(knownSpotsT, knownSpotsF, knownLetters, notPresent)

        possibleWords = findPossibilities(knownSpotsT, knownSpotsF, knownLetters, notPresent, allWordleWords)
        print(f"\nPossible words:\n{possibleWords}")

        # freqs = nltk.FreqDist([w.lower() for w in nltk.corpus.brown.words()])
        # wordlist_sorted = sorted(possibleWords, key=lambda x: freqs[x.lower()], reverse=True)

        # print(f"\nPossible words sorted by popularity:\n{wordlist_sorted[:10]}")

        scoreDict = rateWords(possibleWords, dictionaryList, knownLetters, notPresent)
        # print(scoreDict)
        bestForRemove = sorted(dictionaryList, key=lambda x: scoreDict[x], reverse=True)

        print(f"\nbest words for narrowing options: {bestForRemove[:10]}")

        wait = input("\nPress enter to continue")

    # alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    # countLetters(dictionaryList, alphabet)

main()
