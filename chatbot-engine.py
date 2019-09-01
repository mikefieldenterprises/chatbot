#!/usr/local/bin/python3

# Setup NLP
import nltk
import numpy as np
import random
import string # to process standard python strings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import cgi
import spellchecker # Custom spellchecker.py in the current directory
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.tokenize import RegexpTokenizer
import json
import logging

# Load config vars
PATH_TO_NLTK_DATA_FOLDER = "./nltk_data"
PATH_TO_CORPUS_FILE = "./corpora/corpus-robert.txt"
LANGUAGE = "english"
LOG_LEVEL = logging.DEBUG # INFO, WARN, DEBUG, ERROR


# Set logging level
logging.basicConfig(level=LOG_LEVEL)

# Point the app to your data folder
nltk.data.path.append( PATH_TO_NLTK_DATA_FOLDER )


# Define Conversational Scripts/Channels. Don't use punctuation in the inputs. Punctuation in the responses is fine.
THANKYOU_INPUTS = ("thanks","thank you","gracias","grazie","danke","cheers","sweet","chur",)
THANKYOU_RESPONSES = ["You're welcome", "My pleasure", "No problem at all"]
GREETING_INPUTS = ("hello","hi","greetings","hey","hola",)
GREETING_RESPONSES = ["Hi!","Hello","Hello!",":-)","Hi :-)"]
HOWAREYOU_INPUTS = ("how are you","how are things","what's new","sup","what's up","how r u","how u doin",)
HOWAREYOU_RESPONSES = ["Good, thanks","I'm great, thanks for asking","Excellent, thanks"]
WHOAREYOU_INPUTS = ("who are you","what your name","what is your name",)
WHOAREYOU_RESPONSES = ["I'm Jenny, Robert's virtual assistant."]
GOODBYE_INPUTS = ("bye","see you","later", "see you later", "adios", "chao", "ciao", "good bye", "goodbye",)
GOODBYE_RESPONSES = ["Bye! Thanks for the chat."]
NOT_UNDERSTAND_RESPONSES = ["I'm sorry, I don't understand. Could you please rephrase the question?", "I'm sorry, I didn't get that. Could you try asking that a different way?"]

# Channel entry indicators
ASKFOREMAIL_INPUTS = ("can you email me","can i sign up for your mailing list", "can you send me listings in my area","email me")
ASKFOREMAIL_RESPONSES = ["Of course. Which email address should we send it to?","Sure. What's your email address?"]

# Expects that each element (line) is a json string with "tags" and "content", and concatenates them together
def convertCorpusArrayIntoDocumentArray( lines ):
    documents = []
    for line in lines:
        jsonobj = json.loads( line )
        doc = jsonobj["tags"]+" "+jsonobj["content"]
        documents.append( doc )
    return documents

# Correct spelling
def correctSpelling( input ):
    retval = []
    word_tokens = word_tokenize( input )
    for word in word_tokens:
        retval.append( spellchecker.correction( word ) )
    return " ".join(retval)

# Surround plain text answer with JSON string
def formatWithJSON( input ):
    return "{\"content\":\""+input+"\"}"

# Find occurences of user input in a script. If found, choose a random response
def getResponseFromScript( input_raw, input_corrected, scriptinputs, scriptoutputs):
    # Remove punctuation from input
    input_corrected = removePunctuation( input_corrected )
    input_raw = removePunctuation( input_raw )
    if input_raw.lower() in scriptinputs:
        return formatWithJSON( random.choice(scriptoutputs) )
    elif input_corrected.lower() in scriptinputs:
        return formatWithJSON( random.choice(scriptoutputs) )
            
# Search coprus based on TF-IDF and cosine-similarity calculation
def getResponseFromCorpus( input_raw, input_corrected ):

    # Remove stop words
    input_corrected = removeStopWords( input_corrected )
    logging.debug("spell-corrected input after removing stop words: "+input_corrected)

    # Load the corpus and convert each line into a document
    lines = loadFileIntoArray( PATH_TO_CORPUS_FILE )
    documents = convertCorpusArrayIntoDocumentArray( lines )
    
    # Use TF-IDF and Cosine Similarity to find matches in corpus
    # First check for the non-spell-checked input. Then, if nothing found, search for the spell-checked input
    answer = getTfidfAndCosineSimilariy( lines, documents, input_raw )
    if answer == "":
        logging.debug("Didn't find anything after searching with raw input, so now searching with spell-checked input")
        answer = getTfidfAndCosineSimilariy( lines, documents, input_corrected )

    # Return answer. It might be an empty string.
    return answer

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

# Loads the given file into an array, one element per line. Ignore emtpy lines and lines starting with #
def loadFileIntoArray( filenameandpath ):
    file = open( filenameandpath ,'r',errors = 'ignore')
    lines = []
    for line in file.readlines():
        if line.strip() != "" and line[0] != "#":
            lines.append(line)
    return lines

# Calculate answer based on "input"
def main():

    # Setup vars
    output = ""

    # Get data input from form/querystring           
    input_raw = cgi.FieldStorage().getvalue("q")
    channelname = cgi.FieldStorage().getvalue("cn")
    stepnumber = cgi.FieldStorage().getvalue("sn")
    logging.debug("raw: "+input_raw)

    # Change all input to lower case
    input_raw = input_raw.lower()

    # Remove punctuation
    input_nopunkt = input_raw.translate(str.maketrans('', '', string.punctuation))

    # Correct spelling
    input_corrected = correctSpelling( input_nopunkt )
    logging.debug("corrected: "+input_corrected)

    # First check our predefined scripts
    if( getResponseFromScript( input_raw, input_corrected, ASKFOREMAIL_INPUTS, ASKFOREMAIL_RESPONSES) != None ):
        output = getResponseFromScript( input_raw, input_corrected, ASKFOREMAIL_INPUTS, ASKFOREMAIL_RESPONSES)
        jsonobj = json.loads( output )
        jsonobj["channelname"]="askforemail" # PICKUP FROM HERE
        jsonobj["stepnumber"]="1"
        output = json.dumps( jsonobj )

    elif( getResponseFromScript( input_raw, input_corrected, THANKYOU_INPUTS, THANKYOU_RESPONSES) != None ):
        output = getResponseFromScript( input_raw, input_corrected, THANKYOU_INPUTS, THANKYOU_RESPONSES)

    elif( getResponseFromScript( input_raw, input_corrected, GOODBYE_INPUTS, GOODBYE_RESPONSES) != None ):
        output = getResponseFromScript( input_raw, input_corrected, GOODBYE_INPUTS, GOODBYE_RESPONSES)

    elif( getResponseFromScript( input_raw, input_corrected, GREETING_INPUTS, GREETING_RESPONSES) != None ):
        output = getResponseFromScript( input_raw, input_corrected, GREETING_INPUTS, GREETING_RESPONSES)

    elif( getResponseFromScript( input_raw, input_corrected, WHOAREYOU_INPUTS, WHOAREYOU_RESPONSES) != None ):
        output = getResponseFromScript( input_raw, input_corrected, WHOAREYOU_INPUTS, WHOAREYOU_RESPONSES)

    elif( getResponseFromScript( input_raw, input_corrected, HOWAREYOU_INPUTS, HOWAREYOU_RESPONSES) != None ):
        output = getResponseFromScript( input_raw, input_corrected, HOWAREYOU_INPUTS, HOWAREYOU_RESPONSES)

    # If nothing was found in the scripts, then search the corpus
    else:
        output = getResponseFromCorpus( input_raw, input_corrected )

    # If nothing found, say so.
    if output == "":
        logging.debug("No answer found at all. Showing an i-don't-understand message.")
        output = formatWithJSON( random.choice( NOT_UNDERSTAND_RESPONSES ) )

    print("",end="")
    print( output )



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
    stop_words = set(stopwords.words( LANGUAGE ))
    word_tokens = word_tokenize( userinput )
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return " ".join( filtered_sentence )

# Main code entry point
# Output html header then run main()
# If there's an error, show the error
try:
    print("Content-type: text/html\n")
    main() 
except:
    cgi.print_exception()