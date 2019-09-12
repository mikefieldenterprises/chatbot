# CONFIGURATION VARS
import logging
import cgi

CLIENTID = cgi.FieldStorage().getvalue("cid")
SESSIONID = cgi.FieldStorage().getvalue("sid")

PATH_TO_NLTK_DATA_FOLDER = "./nltk_data"
PATH_TO_CORPUS_FILE = "./client-data/client-"+CLIENTID+"/custom-corpus.txt"
PATH_TO_USERVALUES_FILE = "./client-data/client-"+CLIENTID+"/transcripts/"+SESSIONID+"-uservalues.txt"
PATH_TO_CHANNEL_FILE = "./client-data/client-"+CLIENTID+"/channel-descriptions.txt"
PATH_TO_TRANSCRIPT_FILE = "./client-data/client-"+CLIENTID+"/transcripts/"+SESSIONID+"-transcript.txt"
PATH_TO_CLIENTCONFIG_FILE = "./client-data/client-"+CLIENTID+"/client-config.txt"
LANGUAGE = "english"
EMAIL_FROM = "mike@mikefield.ca"
LOG_LEVEL = logging.DEBUG # INFO, WARN, DEBUG, ERROR

# ONLY USED IN ALTERNATE / COMMENTED-OUT VERSION OF sendEmail(). CAN REMOVE THEM IF SENDMAIL WORKS
#EMAIL_SMTP_SERVER = "" 
#EMAIL_SMTP_PORT = ""
#EMAIL_SMTP_USER = ""
#EMAIL_SMTP_PWD = ""