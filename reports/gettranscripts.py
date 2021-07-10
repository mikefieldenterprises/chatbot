#!/usr/local/bin/python3
#/usr/bin/python3

# Gets contents of the client-data folder (relative to current script, it's back one level, 
# then up one level in the /client-data/ folder).
# Each folder in the client-data folder has the clientid. This script lets you drill into each of the client's history to
# view the chat transcripts and saved values.

# Import required modules
import logging
import cgi
import os
import datetime as dt

# Set logging level
logging.basicConfig(level=logging.ERROR)

# Calculate answer based on "input"
def main():

    # Setup vars
    output = ""

    # Get data input from form/querystring           
    clientid = cgi.FieldStorage().getvalue("c")
    transcriptfile = cgi.FieldStorage().getvalue("t")
    minutes_ago = cgi.FieldStorage().getvalue("m")

    if not minutes_ago:
        minutes_ago = int(0)

    if not clientid and not transcriptfile:
        # Show error
        output = "Error. clientid must be passed into the querystring."

    elif clientid and not transcriptfile:
        # Show contents of client folder
        transcriptsfolder = getTranscriptsFolder( clientid )
        output = getTranscriptFilesAsNewLines( clientid, transcriptsfolder, minutes_ago )

    elif clientid and transcriptfile:
        path = getTranscriptFilePath( clientid, transcriptfile )
        output = getContentsOfFileWithNewLines( path )

    print("",end="")
    print( output )


def getClientDataFolder():
    return os.path.dirname(os.path.abspath(__file__)) + "/../client-data/"

def getContentsOfFileWithNewLines( path ):
    retval = ""
    f = open( path , "r")
    for line in f:
        retval += line
    return retval

def getTranscriptFilePath( clientid, transcriptfile ):
    return getTranscriptsFolder( clientid ) + transcriptfile

def getTranscriptsFolder( clientid ):
    return getClientDataFolder() + "client-" + clientid + "/transcripts/"

def getTranscriptFilesAsNewLines( clientid, foldername, minutes_ago ):
    retval = ""
    interval = int(minutes_ago)
    start_time = dt.datetime.now() - dt.timedelta(minutes=interval)
    for f in sorted( os.listdir( foldername ) , reverse=True):
        if ".DS_Store" not in f and "uservalues" not in f:
            if minutes_ago == 0:
                retval += f + "\n"
            else:
                filetime = dt.datetime.fromtimestamp( os.path.getctime( foldername + f) )
                if filetime >= start_time:
                    retval += f + "\n"
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
