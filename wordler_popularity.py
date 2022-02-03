import nltk.corpus

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

def parseResults(result, knownSpotsT, knownSpotsF, knownLetters, notPresent):
    for i in range(0,5,1):
        letter = result[2*i+1]
        if result[2*i] == "f":
            if letter not in notPresent:
                notPresent.append(letter)
        elif result[2*i] == "y":
            if letter not in knownLetters:
                knownLetters.append(letter)
            knownSpotsF.append(f"{i+1}{letter}")
        elif result[2*i] == "g":
            if letter not in knownLetters:
                knownLetters.append(letter)
            knownSpotsT.append(f"{i+1}{letter}")
        else:
            print("Error in input, please restart")
            return

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

    dictionaryList = readSysWord("/usr/share/dict/words")

    #for knownSpotsT, put number and letter for letters you know
    #for knownSpotsF, put number and leter of letter you know isn't there
    #for knownLetters, put letters you know are there
    #for not present, put letters that aren't there

    knownSpotsT, knownSpotsF, knownLetters, notPresent = [], [], [], []

    while True:
        print("\nInstructions: enter given information with designation first followed by letter")
        print("f for grey, y for yellow, g for green")
        while True:
            result = input("\nPlease enter result: ")
            if len(result) == 10 and result.isalpha():
                break
            else:
                print("Sorry there was an error")

        parseResults(result, knownSpotsT, knownSpotsF, knownLetters, notPresent)
        print("\nData in case the code crashes:")
        print(knownSpotsT, knownSpotsF, knownLetters, notPresent)

        possibleWords = findPossibilities(knownSpotsT, knownSpotsF, knownLetters, notPresent, dictionaryList)

        freqs = nltk.FreqDist([w.lower() for w in nltk.corpus.brown.words()])

        wordlist_sorted = sorted(possibleWords, key=lambda x: freqs[x.lower()], reverse=True)
        print(f"\nPossible words:\n{wordlist_sorted}")

        wait = input("\nPress enter to continue")

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    countLetters(dictionaryList, alphabet)

main()
