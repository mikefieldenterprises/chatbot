# CUSTOM NLP MODULE
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.tokenize import RegexpTokenizer
import chatbot.spellchecker as spellchecker # Custom spellchecker.py in the current directory
import chatbot.config as config       # Custom config module
import string # to process standard python strings


# Point the app to your data folder
nltk.data.path.append( config.PATH_TO_NLTK_DATA_FOLDER )


# Correct spelling
def correctSpelling( input ):
    retval = []
    word_tokens = word_tokenize( input )
    for word in word_tokens:
        retval.append( spellchecker.correction( word ) )
    return " ".join(retval)      


def getTfidfAndCosineSimilariy( lines, documents, userinput ):

    # Add user input to document list
    documents.append( userinput )

    # Use TF-IDF and Cosine Similarity to find nearest match
    TfidfVec = TfidfVectorizer(tokenizer=preProcessDocument)
    tfidf = TfidfVec.fit_transform( documents )

    # Calculate cosine similarity between userinput and all documents. Returns a matrix (array of arrays)
    # Cosine similarity measures the difference in the angle between vectors. Better than finding the 
    # Euclidean distance between the two points, since some documents can be much longer than others.
    # We eventually want the highest value that isn't 1 (1 is the userinput, a perfect match.)
    csmatrix = cosine_similarity( tfidf[-1], tfidf )
    id_of_second_highest = csmatrix.argsort()[0][-2] # argsort returns the indexes of the sorted array elements. We want the second highest one. The highest one is the userinput, and should be equal to 1.
    flat = csmatrix.flatten() # Flattens the array of arrays into a one-dimensional array for easier retrieval
    flat.sort() # Sorts the flattened values, just like argsort above, but in a flattened matrix
    tfidf_of_second_highest = flat[-2] # Gets the value of the second highest/closest document

    # Now that we've done our calculation, remove the userinput from documents
    documents.remove( userinput )

    # If the TF-IDF of the second highest data point is zero, that means there were no matches. Show a message stating we couldn't understand or find a match.
    if ( tfidf_of_second_highest == 0 ):
        logging.debug("No match found")
        return ""
    else:
        return lines[ id_of_second_highest ]

# Lemmatize using WordNet
def lemmatizeWords(tokens):
    lemmer = nltk.stem.WordNetLemmatizer()
    return [lemmer.lemmatize(token) for token in tokens]


# Pre-process each corpus document (text) by removing stop words, converting to lower case, removing puctuation and lemmatizing with WordNet
def preProcessDocument(text):
    # Remove stop words
    text = removeStopWords( text )
    # Get punctuation dictionary
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    return lemmatizeWords(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Remove punctuation (not used, but can be)
def removePunctuation( userinput ):
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize( userinput )
    return " ".join(words)

# Remove stop words
def removeStopWords( userinput ):
    stop_words = set(stopwords.words( config.LANGUAGE ))
    word_tokens = word_tokenize( userinput )
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return " ".join( filtered_sentence )