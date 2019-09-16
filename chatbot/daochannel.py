# CUSTOM DAO CLASS
import chatbot.config as config
import json
import logging
import chatbot.daotranscript as daotranscript     # Custom transcripts module
import chatbot.daouservalue as daouservalue # Custom module
import chatbot.outputformatter as outputformatter   # Custom output formatter module
import chatbot.messaging as messaging # Custom messenger module
import chatbot.utils as utils # Custom utils module
import random

def getAllChannelData():
    return utils.loadFileIntoArray( config.PATH_TO_CHANNEL_FILE )

# Parses out the appropriate action from a string in the format
# Conditional|Buyer:goto-channel-2-step-1,Seller:goto-channel-3-step-1
# Any|validateemail,goto-channel-3-step-1-thenend
# Returns an array of strings
def getActionsFromFullActionValue( userinput, fullactionvalue ):
    retval = []
    # Normalize the json string for easier matching
    fullactionvalue = fullactionvalue.lower()
    actionparts = fullactionvalue.split("|")
    logging.debug("actionparts: "+str(actionparts))
    actions = ""
    if actionparts[0] != "|":
        actiontype = actionparts[0]
        actiondetail = actionparts[1]
        if actiontype == "any":
            actions = actiondetail
        elif actiontype == "conditional":
            parts = actiondetail.split(";")
            for part in parts:
                value = part.split(":")[0]
                if userinput == value:
                    actions = part.split(":")[1]
                    #actions = allactionsforcondition.split(",")
                    break
        for action in actions.split(","):
            retval.append(action)
    return retval

# Returns a dictionary object
def getOutputFromActions( channel, step, actions, input_raw, stepdata ):
    retval = {}
    for a in actions:
        if a.startswith("goto-"):
            channel = a.split("-")[2]
            step = a.split("-")[4]
            retval = getResponseFromChannelAndStep( "", "", channel, step )
            logging.debug("Found action to goto channel " + channel + " and step "+step)
            if a.endswith("thenclosechat"):
                retval["step"]=""
                retval["channel"]=""
                retval["closechat"]="true"
                daouservalue.emailUserValues()
                logging.debug("Closing chat")
            if a.endswith("thenexitchannel"):
                retval["step"]=""
                retval["channel"]=""
                logging.debug("Exiting channel")
        elif a == "validateemail":
            if not messaging.isValidEmail( input_raw ):
                retval["content"] = random.choice(["Oh sorry, that email address doesn't look valid. Can you please try again?","Hmm, that doesn't look like a proper email address. Can you try again?"])
                retval["step"] = step
                retval["channel"] = channel
                break
        elif a.startswith("save-"):
            key = a.split("-")[1]
            daouservalue.saveUserValue( key, input_raw )
        elif a == "emailtranscript":
            daotranscript.emailTranscript( input_raw )
        elif a == "exitchannel":
            retval["content"] = random.choice(stepdata["bottext"])
            retval["step"]=""
            retval["channel"]=""
        elif a == "closechat":
            retval["step"]=""
            retval["channel"]=""
            retval["closechat"]="true"
            daouservalue.emailUserValues()
            logging.debug("Closing chat")
        else:
            retval["content"] = "Sorry, I'm not sure what to say"
            retval["step"]=""
            retval["channel"]=""
            logging.error("No action named \""+a+"\" found. Didn't know what to say to the user.")
    return retval


# Returns a dictionary object
def getResponseFromChannelAndStep( input_raw, input_corrected, channel, step ):

    # Load the step data from the channel description file
    stepdata = getStepAsDict( channel, step )
    output = {}
    logging.debug("Inside getResponseFromChannelAndStep(), input_raw: "+str(input_raw))

    # If there isn't yet any input, it means we need to load the right buttons and chatbot text
    if not input_raw:
        output["content"] = random.choice(stepdata["bottext"])
        output["step"] = stepdata["step"]
        output["channel"] = stepdata["channel"]
        output["buttonoptions"] = stepdata["buttonoptions"]
        logging.debug("No input when getting channel and step, so we loaded the channel/step info and get this output: "+str(output))
    
    # If there is input, then load the appropriate action from this step
    else:
        actions = getActionsFromFullActionValue( input_raw, stepdata["action"] )
        logging.debug("Input text was found, so we loaded the following actions: "+str(actions))
        output = getOutputFromActions( channel, step, actions, input_raw, stepdata )

    # Replace placeholders with uservalues, if any
    output["content"] = replaceStringWithUserValues( output["content"] )
    logging.debug("output: "+str(output))
    return output  

def getStepAsDict( channelid, stepid ):
    retval = json.loads( "{}" )
    lines = getAllChannelData()
    for line in lines:
        jsonobj = json.loads( line )
        if jsonobj["channel"] == channelid and jsonobj["step"] == stepid:
            retval = json.loads( line )
            break
    return retval

def getStepByTriggerWord( input_raw, input_corrected ):
    retval = json.loads( "{}" )
    lines = getAllChannelData()
    for line in lines:
        jsonobj = json.loads( line )
        if input_raw in jsonobj["triggers"] or input_corrected in jsonobj["triggers"]:
                retval = json.loads( line )
                break
    return retval

# Replaces occurrences of %key% in a string with the given user value
# E.g. Hello %name% becomes Hello Mike
def replaceStringWithUserValues( mystring ):
    uservals = daouservalue.getAllUserValues()
    for key in uservals.keys():
        val = uservals[key]
        if key == "name":
            val = val.title()   # Convert name to title case. Our configparser always saves as lowercase
        mystring = mystring.replace( "%"+key+"%", val )
    return mystring