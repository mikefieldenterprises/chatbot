# CUSTOM DAO FOR CORPORA MODULE
import chatbot.utils as utils
import chatbot.config as config
import chatbot.nlp as nlp
import json
import logging

# Expects that each element (line) is a json string with "tags" and "content", and concatenates them together
def convertCorpusArrayIntoDocumentArray( lines ):
    documents = []
    for line in lines:
        thisline = json.loads( line )
        doc = thisline["tags"]+" "+thisline["content"]
        documents.append( doc )
    return documents

# Search coprus based on TF-IDF and cosine-similarity calculation
def getResponseFromCorpus( input_raw, input_corrected ):

    # Remove stop words
    input_corrected = nlp.removeStopWords( input_corrected )
    logging.debug("spell-corrected input after removing stop words: "+input_corrected)

    # Load the corpus and convert each line into a document
    lines = loadCorpusAsArray()
    documents = convertCorpusArrayIntoDocumentArray( lines )
    
    # Use TF-IDF and Cosine Similarity to find matches in corpus
    # First check for the non-spell-checked input. Then, if nothing found, search for the spell-checked input
    answer = nlp.getTfidfAndCosineSimilariy( lines, documents, input_raw )
    if answer == "":
        logging.debug("Didn't find anything after searching with raw input, so now searching with spell-checked input")
        answer = nlp.getTfidfAndCosineSimilariy( lines, documents, input_corrected )

    # Return answer. It might be an empty string.
    return answer

# Loads the corpus into an array, one element per line in the file
def loadCorpusAsArray():
    return utils.loadFileIntoArray( config.PATH_TO_CORPUS_FILE )

