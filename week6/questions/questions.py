import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    # print(f"{directory=}")
    result = {}
    for fn in os.listdir(directory):
        with open(os.path.join(directory, fn)) as f:
            result[fn] = f.read()
    # print(f"{result=}")
    return result


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # print(f"{document=}")
    result = []
    for token in nltk.word_tokenize(document):
        token = token.lower()
        # skip all kinds of invalid tokens
        if token in string.punctuation:
            continue
        if token in nltk.corpus.stopwords.words("english"):
            continue
        if not token.isalpha():     # NOTE it seems that previous don't are not enough ...
            continue
        result.append(token)
    return result


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # print(f"{documents=}")
    result = {}
    all_words = set()
    for _, words in documents.items():
        all_words.update(words)
    for word in all_words:
        contained_in_docs = 0
        for _, words in documents.items():
            if word in words:
                contained_in_docs += 1
        total_documents = len(documents) + 1    # 1 to compensate for div by 0 in case of math.log(1)
        idf = math.log(total_documents / contained_in_docs)
        result[word] = idf
    # print(f"{result=}")
    return result

def tfidf_select(query, objects, idfs, n):
    """
    Perform select using words in `query` on `objects` which is 
        a dictionary of (keys and words). 
    `idfs` provides IDF values for the words.
    `n` is the number of results (keys from `objects`) to be returned.
    """
    # print(f"{query=}")
    # print(f"{objects=}")
    # print(f"{idfs=}")
    # print(f"{n=}")
    result = {}
    for word in query:
        for obj, words in objects.items():
            tf = words.count(word)
            tfidf = tf * idfs[word]
            if obj not in result:
                result[obj] = 0
            result[obj] += tfidf
    # print(f"{result=}")
    scored = sorted(result.items(), key=lambda x: x[1], reverse=True)
    return [fn for fn, _ in scored[:n]]


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    return tfidf_select(query, files, idfs, n)


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    return tfidf_select(query, sentences, idfs, n)
    


if __name__ == "__main__":
    main()
