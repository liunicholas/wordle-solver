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

    #for knownSpotsT, put number and letter for letters you know
    #for knownSpotsF, put number and leter of letter you know isn't there
    #for knownLetters, put letters you know are there
    #for not present, put letters that aren't there

    knownSpotsT, knownSpotsF, knownLetters, notPresent = ["5t"], ["3t","1s","2i","3s"], ["t","s","i"], ["l","a","e","r", "g","h","v"]

    possibleWords = findPossibilities(knownSpotsT, knownSpotsF, knownLetters, notPresent, dictionaryList)

    print(possibleWords)

main()
