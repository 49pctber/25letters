package main

import (
	"fmt"
	"os"
	"strings"
)

// TODO keep track of hashes instead of the strings of the words themselves
// TODO sort by actual letter frequency, not by some arbitrary ordering I found online.
// TODO sort by least frequent MSBs in hash

var word2bits map[string]uint32
var msb2words [][]string
var letter2index []int

// var letterfreq []int

func init() {
	word2bits = make(map[string]uint32, 13000)
	msb2words = make([][]string, 26)
	for i := 0; i < 26; i++ {
		msb2words[i] = make([]string, 0)
	}
	// letterfreq = make([]int, 26)
	letter2index = make([]int, 26)
	for i, c := range strings.ToLower("ETAOINSRHDLUCMFYWGPBVKXQZJ") {
		letter2index[int(c)-int('a')] = i
	}
}

type State struct {
	state              uint32
	words              []string
	greatest_unset_bit uint32
	skipped_letter     bool
}

func (s State) String() string {
	return fmt.Sprintf("%08x %d %s", s.state, s.greatest_unset_bit, s.words)
}

/*
A simple "hash" of each word that represents the word as a uint32
The most significant bit (MSB) is also included in the return value
*/
func Bitify(word string) (uint32, int, error) {
	var bits uint32 = 0
	var msb int = 0
	for _, c := range word {
		i := letter2index[uint32(c)-uint32('a')]
		if i > msb {
			msb = i
		}

		if (bits>>i)&0b1 == 0b1 {
			return 0, 0, fmt.Errorf("not all letters are unique")
		}
		bits |= 1 << i
	}
	return bits, msb, nil
}

/*
Recursively search for new words using a given state
*/
func Search(s *State) {

	// return if all letters have been found
	if s.state == 0x03ffffff {
		fmt.Printf("%v\n", s.words)
		return
	}

	// find next letter to include
	for {
		if (s.state>>s.greatest_unset_bit)&0b1 == 0 {
			break
		}
		s.greatest_unset_bit--
	}

	// look for words with the least common letter that hasn't yet been included
	for _, word := range msb2words[s.greatest_unset_bit] {
		if (word2bits[word] & s.state) == 0 { // all new letters
			newstate := &State{state: word2bits[word] | s.state, words: append(s.words, word), greatest_unset_bit: s.greatest_unset_bit - 1, skipped_letter: s.skipped_letter}
			Search(newstate)
		}
	}

	// try skipping least common letter that hasn't yet been found
	if !s.skipped_letter {
		s.state |= 1 << s.greatest_unset_bit
		s.greatest_unset_bit--
		for _, word := range msb2words[s.greatest_unset_bit] {
			if (word2bits[word] & s.state) == 0 { // all new letters
				newstate := &State{state: word2bits[word] | s.state, words: append(s.words, word), greatest_unset_bit: s.greatest_unset_bit - 1, skipped_letter: true}
				Search(newstate)
			}
		}
	}
}

func main() {

	// get user-specified path to wordlist
	if len(os.Args) < 2 {
		panic(fmt.Errorf("specify wordlist"))
	}

	// read file
	b, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}

	// sanitize word list
	words := strings.Split(string(b), "\n")
	for _, word := range words {
		word = strings.ToLower(strings.TrimSpace(word))
		if len(word) != 5 {
			continue
		}

		bits, msb, err := Bitify(word)
		if err != nil {
			continue
		}
		word2bits[word] = bits
		msb2words[msb] = append(msb2words[msb], word)
	}

	// start recursive search
	s := &State{state: 0, words: make([]string, 0), greatest_unset_bit: 25, skipped_letter: false}
	Search(s)
}
