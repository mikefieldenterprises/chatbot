# CLIENT CONFIG VALUE MODULE
import configparser                     # Saves and retrieves key=value pairs in a text file
import chatbot.config as config                           # Custom config module
import logging

def getEmailBCC():
    return getClientConfigValue( "email_bcc" )

def getRemoteHost():
    return getClientConfigValue( "web_domain" )

def getClientConfigValue( key ):
    clientconfigvalues = configparser.ConfigParser()
    clientconfigvalues.read( config.PATH_TO_CLIENTCONFIG_FILE )
    return clientconfigvalues["DEFAULT"][key]

def saveClientConfigValue( key, value ):
    clientconfigvalues = configparser.ConfigParser()
    clientconfigvalues.read( config.PATH_TO_CLIENTCONFIG_FILE )
    clientconfigvalues["DEFAULT"][key] = value
    with open( config.PATH_TO_CLIENTCONFIG_FILE, "w+") as clientconfigvaluesfile:
        clientconfigvalues.write(clientconfigvaluesfile)
    logging.debug("Saved clientconfigvalue "+key+"="+value)

