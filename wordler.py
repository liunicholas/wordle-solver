import nltk.corpus
from allWords import allWordleWords
from lewdlewords import lewdleWords

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
        if indWord.isalpha() and len(indWord) == 5:
            dictionaryList.append(indWord.lower())

    sFile.close()

    return dictionaryList

def getResult():
    while True:
        VALID = True
        result = input("\nPlease enter result: ").lower()
        if len(result) == 10 and result.isalpha():
            for i in range(0,5,1):
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
    for i in range(0,5,1):
        letter = result[2*i+1]
        word+=letter

    for i in range(0,5,1):
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
            if letter not in notPresent and letter not in knownLetters and letter not in word:
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

def main():

    # dictionaryList = readSysWord("/usr/share/dict/words")
    dictionaryList = allWordleWords
    # dictionaryList = lewdleWords

    #for knownSpotsT, put number and letter for letters you know
    #for knownSpotsF, put number and leter of letter you know isn't there
    #for knownLetters, put letters you know are there
    #for not present, put letters that aren't there

    knownSpotsT, knownSpotsF, knownLetters, notPresent = [], [], [], []

    while True:
        print("\nInstructions: enter given information with designation first followed by letter")
        print("f for grey, y for yellow, g for green")

        result = getResult()
        parseResults(result, knownSpotsT, knownSpotsF, knownLetters, notPresent)

        print("\nData in case the code crashes:")
        print(knownSpotsT, knownSpotsF, knownLetters, notPresent)

        possibleWords = findPossibilities(knownSpotsT, knownSpotsF, knownLetters, notPresent, dictionaryList)
        print(f"\nPossible words:\n{possibleWords}")

        freqs = nltk.FreqDist([w.lower() for w in nltk.corpus.brown.words()])
        wordlist_sorted = sorted(possibleWords, key=lambda x: freqs[x.lower()], reverse=True)

        print(f"\nPossible words sorted by popularity:\n{wordlist_sorted[:10]}")


        wait = input("\nPress enter to continue")

    # alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    # countLetters(dictionaryList, alphabet)

main()
