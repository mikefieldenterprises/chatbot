#!/usr/local/bin/python3

# Import required modules
import traceback
import cgi
import logging
import string
import chatbot.config as config                     # Loads custom config vars
import chatbot.daochannel as daochannel                        # Loads custom DAO
import chatbot.daotranscript as daotranscript          # Loads custom transcripts module
import chatbot.daocorpus as daocorpus               # Loads custom dao for coropora module
import chatbot.nlp as nlp                           # Loads custom nlp module
import chatbot.outputformatter as outputformatter   # Loads custom outputformatter module


# Set logging level
logging.basicConfig(level=config.LOG_LEVEL)

# Calculate answer based on "input"
def main():

    # Setup vars
    output = ""

    # Get data input from form/querystring           
    input_raw = cgi.FieldStorage().getvalue("q")
    input_corrected = input_raw # Default value
    input_lower = input_raw # Default value
    channel = cgi.FieldStorage().getvalue("cn")
    step = cgi.FieldStorage().getvalue("sn")

    logging.debug("raw: "+str(input_raw))
    logging.debug("channel="+str(channel))
    logging.debug("step="+str(step))

    if input_raw:
        # Change all input to lower case
        input_lower = input_raw.lower()

        # Remove punctuation
        input_nopunkt = input_lower.translate(str.maketrans('', '', string.punctuation))

        # Correct spelling
        input_corrected = nlp.correctSpelling( input_nopunkt )
        logging.debug("corrected: "+input_corrected)
    else:
        logging.debug("No input from user")

    # If no channel is set yet, look for a channel/step with the given trigger words
    if not channel and not step:
        logging.debug("Channel and step were empty, so we'll lookup a channel with that trigger")
        stepdata = daochannel.getStepByTriggerWord( input_lower, input_corrected )
        if stepdata:
            channel = stepdata["channel"]
            step = stepdata["step"]
            output = daochannel.getResponseFromChannelAndStep( input_lower, input_corrected, channel, step ) 
            # This works for jumping into single-step channels. But when jumping into multi-step channels, it immediately runs that channel's action
            # Need to figure out how to avoid that

    # Get output from channel
    elif channel and step:
        logging.debug("Channel and step were set to channel="+channel+" and step="+step)
        output = daochannel.getResponseFromChannelAndStep( input_lower, input_corrected, channel, step )

    # If nothing was found in the scripts, then search the corpus
    else:
        output = daocorpus.getResponseFromCorpus( input_lower, input_corrected )

    # If nothing found, say so.
    if output == "":
        logging.debug("No answer found at all. Showing an i-don't-understand message.")
        output = daochannel.getResponseFromChannelAndStep( "", "", "100", "1" )

    # Record response in transcript
    daotranscript.updateTranscript( input_raw, output )

    # Convert output dictionary to appropriate output for this implementation (in most cases, use JSON for Web layer)
    formattedoutput = outputformatter.formatAsJSONForWeb( output )

    print("",end="")
    print( formattedoutput )




def showAndLogError( e ):
    # Log the exception
    logging.exception("An exception occurred while processing your request:")

    # Output a friendly error message
    print("",end="")
    print( outputformatter.formatWithJSON( "Oops, something went wrong. Please try again." ) )


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