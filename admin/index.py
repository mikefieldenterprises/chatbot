#!/usr/bin/python3

# Gets contents of the client-data folder (relative to current script, it's back one level, 
# then up one level in the /client-data/ folder).
# Each folder in the client-data folder has the clientid. This script lets you drill into each of the client's history to
# view the chat transcripts and saved values.

# Import required modules
import logging
import cgi
import os

# Set logging level
logging.basicConfig(level=logging.ERROR)

# Calculate answer based on "input"
def main():

    # Setup vars
    output = ""

    # Get data input from form/querystring           
    clientid = cgi.FieldStorage().getvalue("c")
    transcriptfile = cgi.FieldStorage().getvalue("t")

    if not clientid and not transcriptfile:
        # Show contents of client-data folder
        output = "<h1>Clients On Server:</h1>"
        clientdatafolder = getClientDataFolder()
        output += getClientFolderContentsAsHTMLLinks( clientdatafolder )

    elif clientid and not transcriptfile:
        # Show contents of client folder
        output = "<h1>Client ID: "+clientid+"</h1>"
        transcriptsfolder = getTranscriptsFolder( clientid )
        output += getTranscriptFilesAsHTMLLinks( clientid, transcriptsfolder )

    elif clientid and transcriptfile:
        path = getTranscriptFilePath( clientid, transcriptfile )
        output = getContentsOfFileWithBR( path )

    print("",end="")
    print( output )


def getClientDataFolder():
    return os.path.dirname(os.path.abspath(__file__)) + "/../client-data/"

def getClientFolderContentsAsHTMLLinks( foldername ):
    retval = ""
    for folder in sorted(os.listdir( foldername ) ):
        if "client-" in folder:
            clientid = folder.split("-")[1]
            retval += "<a href=\"?c="+clientid+"\">" + clientid + "</a><br/>"
    return retval

def getContentsOfFileWithBR( path ):
    retval = ""
    f = open( path , "r")
    for line in f:
        retval += line + "<br/>"
    return retval

def getTranscriptFilePath( clientid, transcriptfile ):
    return getTranscriptsFolder( clientid ) + transcriptfile

def getTranscriptsFolder( clientid ):
    return getClientDataFolder() + "client-" + clientid + "/transcripts/"

def getTranscriptFilesAsHTMLLinks( clientid, foldername ):
    retval = ""
    for f in sorted( os.listdir( foldername ) , reverse=True):
        if ".DS_Store" not in f:
            retval += "<a href=\"?c="+clientid+"&t="+f+"\">" + f + "</a><br/>"
    return retval


def showAndLogError( e ):
    # Log the exception
    logging.exception("An exception occurred while processing your request:"+str(e))

    # Output a friendly error message
    print("",end="")
    print( "Oops, something went wrong. Please try again." )


# Main code entry point
# Output html header then run main()
# If there's an error, show the error
try:
    print("Content-type: text/html\n")
    main() 
except Exception as e:
    # Show an error message
    # No need to start with the content-type header, since it already went out during the "try"
    showAndLogError( e )
