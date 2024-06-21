#
# backtrack.py
#
# Author: redd
#
import time
import logging

#
# Input filename
#
infname = "wordlist_small.txt"  # filepath goes here

#
# Output settings
#
filename = "out.csv"
print(f"Valid solutions are being logged to {filename}")
logging.basicConfig(
    format="%(message)s", level=logging.INFO, filename=filename, filemode="w"
)

#
# Start timer
#
tic = time.perf_counter()

#
# Get 5-letter words that each contain 5 unique letters
#
with open(infname, "r") as f:
    wl = f.read().split("\n")  # all words from the input file
    wl5wa = [
        word for word in wl if (len(word) == 5 and len(set(word)) == 5)
    ]  # word list with anagrams

#
# find anagrams
#
anagram_dict = (
    {}
)  # anagram_dict has keys of the sorted letters of a word and values of the words corresponding to those letters
wl5 = []  # word list without anagrams to use in backtracking algorithm
for word in wl5wa:
    s = "".join(sorted(word))
    if (
        s in anagram_dict.keys()
    ):  # check if word has an anagram that's already been found
        anagram_dict[s].append(word)
    else:
        anagram_dict[s] = [word]
        wl5.append(word)

#
# create a LUT based on words that contain a given letter
# keys are letters of the alphabet
# values are words that contain that letter
#
lut = {}
for letter in "abcdefghijklmnopqrstuvwxyz":
    lut[letter] = []

for word in wl5:
    for i in range(0, 5):
        lut[word[i]].append(word)

#
# sort letters based on their relative frequency
# the idea here is to start with rare letters so that we spend less time looking for them later
#
alphabet = list("abcdefghijklmnopqrstuvwxyz")
occurances = []
for i in range(len(alphabet)):
    occurances.append(len(lut[alphabet[i]]))
z = sorted(
    list(zip(occurances, alphabet)), key=lambda x: x[0]
)  # sorted by least frequent letter
lfl = [p[1] for p in z]  # least frequent letters
lp = {}  # letter position LUT
for i in range(26):
    lp[i] = lfl[i]
    lp[lfl[i]] = i

#
# reorder our lookup table so that words with rarer letters are prioritized in our search
# this is a heuristic, but it seems to work well
#
for l in alphabet:
    scores = []
    words = lut[l]
    for i in range(len(words)):
        score = 0
        word = words[i]
        for letter in word:
            score += z[lfl.index(letter)][0]
        scores.append(score)
    sbs = sorted(list(zip(words, scores)), key=lambda x: x[1])  # sorted by score
    sorted_words = [p[0] for p in sbs]
    lut[l] = sorted_words.copy()


#
# A class that stores information about the current search.
#
class CandidateSolution:
    def __init__(self):
        self.words = []
        self.skip = None
        self.x = [False] * 26
        self.checked = set()

    def populate(self, other):
        """
        Populates a solution object with the information from another object.
        """
        self.words = other.words.copy()
        self.skip = other.skip
        self.x = other.x.copy()
        self.checked = other.checked.copy()

    def checkValidSolution(self):
        """
        Checks if we found a solution.
        We simply need to check if we have five words in the list.
        """
        return len(self.words) == 5

    def checkValidWord(self, word):
        """
        Checks that every letter in word hasn't yet been seen.
        """
        for letter in word:
            if self.x[lp[letter]] == True:
                return False
        return True

    def addWord(self, word):
        """
        Attempts to add a word to the candidate solution.
        If so, this returns a new object with that word included.
        """
        if word in self.checked:
            return False, self
        else:
            self.checked.add(word)

        if self.checkValidWord(word):
            y = CandidateSolution()
            y.populate(self)
            y.words.append(word)
            for letter in word:
                y.x[lp[letter]] = True
            return True, y
        return False, self

    def firstFalse(self):
        """
        Return the index of the first False in self.x
        This corresponds to the index of the rarest letter yet to be seen.
        """
        return self.x.index(False)

    def skipLetter(self):
        """
        If self.skip is None, this skips the least frequent letter that hasn't been found yet.
        """
        if self.skip == None:
            y = CandidateSolution()
            y.populate(self)
            i = self.firstFalse()
            y.skip = lp[i]
            y.x[i] = True
            return True, y
        else:
            return False, self

    def printAnagrams(self):
        """
        Prints all combinations of anagrams to the log file.
        I don't think I've ever used a quintuple loop before. Neat.
        """
        for word0 in anagram_dict["".join(sorted(self.words[0]))]:
            for word1 in anagram_dict["".join(sorted(self.words[1]))]:
                for word2 in anagram_dict["".join(sorted(self.words[2]))]:
                    for word3 in anagram_dict["".join(sorted(self.words[3]))]:
                        for word4 in anagram_dict["".join(sorted(self.words[4]))]:
                            str = f"{word0},{word1},{word2},{word3},{word4}"
                            logging.info(str)

    def __repr__(self):
        if len(self.words) == 5:
            str = f"{self.words[0]}"
            for i in range(1, 5):
                str = f"{str},{self.words[i]}"
            return str
        else:
            return f"{self.words} (Skip: {self.skip})"


#
# The backtracking algorithm itself
#
def backtrack(s):
    # stopping condition
    if s.checkValidSolution():
        s.printAnagrams()
        return

    # try skipping least frequent letters first
    skip, skips = s.skipLetter()
    if skip:
        backtrack(skips)

    # find a valid candidate word for next letter
    for candidate in lut[
        lfl[s.firstFalse()]
    ]:  # candidates are chosen from list of words containing the least frequent letter that hasn't yet been seen
        valid, news = s.addWord(candidate)
        if valid:
            backtrack(news)


backtrack(CandidateSolution())  # should find 831 solutions for valid Wordle guesses

toc = time.perf_counter()

print("Done!")
print(f"Computation took {toc-tic} seconds.")
