# USER VALUE MODULE
import configparser                     # Saves and retrieves key=value pairs in a text file
import chatbot.config as config                           # Custom config module
import chatbot.messaging as messaging   # Custom messaging module
import chatbot.utils as utils           # Custom utils module
import chatbot.daoclientconfig as daoclientconfig # Custom client config values module
import logging
import os

# Emails a copy of the uservalues to the given address
def emailUserValues():
    to = daoclientconfig.getEmailBCC()
    cc = ""
    domain = os.environ.get("REMOTE_HOST")
    if config.SESSIONID:
        subject = "Request and Chat Transcript from "+str(domain)
        body = ""
        with open ( config.PATH_TO_USERVALUES_FILE, "r" ) as uservaluesfile:
            body += utils.convertArrayToLinesWithBreaks(uservaluesfile.readlines())
        body += "\n\nTranscript:\n\n"
        with open ( config.PATH_TO_TRANSCRIPT_FILE, "r" ) as transcriptfile:
            body += utils.convertArrayToLinesWithBreaks(transcriptfile.readlines())
        messaging.sendEmail( to, cc, subject, body )
        logging.debug("Sent user values and transcript to "+to)
    else:
        logging.error("Unable to send uservalues and transcript because we don't have a current session id")

def getAllUserValues():
    uservalues = configparser.ConfigParser()
    uservalues.read( config.PATH_TO_USERVALUES_FILE )
    return uservalues["DEFAULT"]

def getUserValue( key ):
    uservalues = configparser.ConfigParser()
    uservalues.read( config.PATH_TO_USERVALUES_FILE )
    return uservalues["DEFAULT"][key]

def saveUserValue( key, value ):
    uservalues = configparser.ConfigParser()
    uservalues.read( config.PATH_TO_USERVALUES_FILE )
    uservalues["DEFAULT"][key] = value
    with open( config.PATH_TO_USERVALUES_FILE, "w+") as uservaluesfile:
        uservalues.write(uservaluesfile)
    logging.debug("Saved uservalue "+key+"="+value)

