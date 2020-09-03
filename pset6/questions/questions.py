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
    files_mapping = {}
    for file_name in os.listdir(directory):
        with open(os.path.join(directory, file_name), encoding="utf8") as f:
            files_mapping[file_name] = f.read()
    return files_mapping


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    filestring = nltk.word_tokenize(document.lower())
    doclist = list()
    for word in filestring:
        if word not in nltk.corpus.stopwords.words("english") and word not in string.punctuation:
            doclist.append(word)

    return doclist


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    counts = dict()

    for filename in documents:
        seen = set()
        for word in documents[filename]:
            if word not in seen:
                seen.add(word)
                if word not in counts:
                    counts[word] = 1
                else:
                    counts[word] += 1
    return {word: math.log(len(documents) / counts[word]) for word in counts}

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidflist = list()
    for filename in files:
        tfidf = 0
        for word in query:
            tfidf += idfs[word] * files[filename].count(word)
        tfidflist.append((filename, tfidf))
    tfidflist.sort(key=lambda x:x[1], reverse=True)
    return [x[0] for x in tfidflist[:n]]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranks = list()
    for sentence in sentences:
        idf = 0
        totalWords = 0
        for word in query:
            if word in sentences[sentence]:
                totalWords += 1
                idf += idfs[word]
        termDensity = float(totalWords / len(sentences[sentence]))
        ranks.append((sentence, idf, termDensity))
    ranks.sort(key=lambda x: (x[1], x[2]), reverse=True)
    return [x[0] for x in ranks[:n]]

    
    


if __name__ == "__main__":
    main()
