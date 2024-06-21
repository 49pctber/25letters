# 25letters

|Contact||
|-|-|
|Author|Bryan Redd|
|Website|[bryanredd.com](bryanredd.com)
|Email|[me@bryanredd.com](me@bryanredd.com)|

## Description

This cointains two solutions to the problem posed in [this video by Stand-up Maths](https://www.youtube.com/watch?v=_-AfhLQfb6w).
It is based on the backtracking technique.
The two implmentations are in `go/` and `python/`

Backtracking is used to efficiently test every possible permutation of a given set.
Backtracking is more efficient than a brute force search because it "backtracks" when it finds itself in a position that won't meet the given criteria.
This process of ignoring permutation that won't work is called "pruning."
In our case, we're really only interested in combinations, and that is reflected in how I set up the algorithm.

Here's how this solution works:

1. Read in the list of words, and remove any words that are not 5 letters long.
2. Find any anagrams to a given word, but only use one of those words during our backtracking search.
3. Find which letters in the list are the most rare, and prioritize searching with those letters first (Essentially, we don't want to have a list of 4 words and spend a lot of time looking for a word with a rare letter that will fit the bill. Instead, we start with those rare letters. We will likely find common letters along the way.)
4. Specify what our solution looks like. In our case that means there are five words where the 25 letters composing them are all unique.
5. Start the backtracking algorithm.

The backtracking algorithm itself works as follows:

1. Start with a candidate set of words. Initially, this set will be empty.
2. See if that candidate set is a valid solution.
    - If so, log this set of words along with any combinations of anagrams that can be formed from it. End this branch of the search.
    - If not, move on to step 3.
3. Try skipping the least common letter you haven't yet seen in this branch of your search.
    - If you've already skipped a letter in this branch, move on to step 4.
    - If you haven't already skipped a letter in this branch, pretend as though you've seen it, and start a new branch at step 1. When you're done searching this new branch, continue on this branch to step 4 *without* skipping any letters.
4. Find every valid word that contains the least frequent letter that hasn't already been seen. Start a new branch of your search where each of those words has been appended at step 1.

## Word Lists

If you would like to run this code, you will need to provide your own word list. For example, you can combine the [possible Wordle answers](https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b#file-wordle-answers-alphabetical-txt) with the [allowed Wordle guesses](https://gist.github.com/cfreshman/cdcdf777450c5b5301e439061d29694c) to get a comprehensive list. I do not own those lists, so the links may die in the future.

## Performance

I was able to find all 831 solutions with the Python version in about 60 seconds on my laptop using this technique. (I have not benchmarked my Go version...I don't have access to the same wordlist I originally used two years ago.)

One neat feature of solving the problem this way is you can find *most* of the solutions almost immediately. I was able to find 725 of the 831 solutions in 10 seconds.

I have not profiled my code, so you might be able to shave a significant percentage off of the runtime simply by optimizing one or two lines somewhere. Submit a pull request if you have any good insights.

### Follow Up Video

After I posted this repository, Stand-up Maths posted a [follow up video](https://www.youtube.com/watch?v=c33AZBnRHks) which showcased some insanely efficient algorithms that are order of magnitudes better than my Python version. I think the value of mine is the simplicity in which one can reason about the backtracking algorithm in Python. If you want more speed, you probably shouldn't be using Python's dictionaries logging text the way that I am, or Python in general. You can also reduce the wordlist to only include valid Wordle guesses (I ran my tests with a dictionary of English words, not necessarily 5 characters long, so I'm sure that slowed me down a bit).
