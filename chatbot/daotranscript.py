# DATA CLASS
import chatbot.config as config
import logging
import os                               # For getting environment variable such as REMOTE_HOST
import json
from datetime import datetime
import chatbot.daouservalue as daouservalue                     # Custom daouservalue module
import chatbot.messaging as messaging                       # Custom messaging module


# Emails a copy of the transcript to the given address
def emailTranscript( recipient ):
    to = daouservalue.getUserValue( "email" )
    cc = ""
    domain = os.environ.get("REMOTE_HOST")
    if to and config.SESSIONID:
        subject = "Chat Transcript from "+str(domain)
        transcriptfilepath = getTranscriptFileAndPath()
        body = ""
        with open ( transcriptfilepath, "r" ) as transcriptfile:
            body = transcriptfile.readlines()
        messaging.sendEmail( to, cc, subject, body )
        logging.debug("Sent transcript to "+to)
    elif not to:
        logging.error("Unable to send transcript because we don't have the user's email address")
    else:
        logging.error("Unable to send transcript because we don't have a current session id")
  
def getTranscriptFileAndPath():
    return config.PATH_TO_TRANSCRIPT_FILE

# Adds two lines to the transcript file
# input_raw     str
# output        dict
def updateTranscript( input_raw, output ):
    # Get timestamp
    dt = datetime.now()
    timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")

    # Open transcript file (create one if not exists)
    transcriptfilepath = getTranscriptFileAndPath()
    transcriptfile = open( transcriptfilepath, "a+" )

    # Append line to end of file
    if str(input_raw) != "None":
        transcriptfile.write( "["+timestamp+"] You: "+str(input_raw)+"\n" )
    transcriptfile.write( "["+timestamp+"] Chatbot: "+str(output["content"])+"\n" )

    # Close file
    transcriptfile.close()