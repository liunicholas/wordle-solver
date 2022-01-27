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

def main():

    dictionaryList = readSysWord("/usr/share/dict/words")

    knownSpotsT, knownSpotsF, knownLetters, notPresent = ["2a","4e","5l","3b"], ["1b"], ["b"], ["r","i","t","s","d","g","z","c","m","n"]

    possibleWords = findPossibilities(knownSpotsT, knownSpotsF, knownLetters, notPresent, dictionaryList)

    print(possibleWords)

main()
