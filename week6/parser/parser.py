import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> SV | SVO | VO
S -> S Conj S


SV -> NP VA | NP VA Adv
SVO -> NP VA PANPs | NP VA PANPs Adv
VO -> VA PANPs

ADJs -> Adj | ADJs Adj
ANP -> Det ADJs NP | NP
NP -> Det N | N

PANP -> P ANP | ANP | ANP P ANP
PANPs -> PANP | PANPs PANP

VA -> V | Adv V
"""

# NONTERMINALS = """
# S -> NP VP
# S -> NP V P ANP
# S -> NP V ANP
# S -> NP V PANP
# S -> NP Adv V NP Conj NP V P NP Adv
# S -> NP V Adv
# S -> V NP
# S -> NP V ANP PANP
# S -> V NP P ANP
# S -> NP V ANP P NP P NP

# S -> S Conj S

# ADJs -> Adj | ADJs Adj
# ANP -> Det ADJs N  | NP
# NP -> Det N | N
# VP -> V | V NP | V NP PANP
# PANP -> P ANP
# """

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # print(f"{sentence=}")
    tokens = nltk.word_tokenize(sentence)
    tokens = [t.lower() for t in tokens if t.isalpha()]
    # print(f"{tokens=}")
    return tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    result = []
    # print(f"{tree=}")
    for node in tree.subtrees():
        if node.label() == "NP":
            result.append(node[0])
    return result


if __name__ == "__main__":
    main()
