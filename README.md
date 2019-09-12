# chatbot


PURPOSE

Adds a basic slot-and-answer chatbot to a website
Conversations (aka "channels") are defined in the ./chatbot/channels.py module


TO RUN THIS APPLICATION

Add to httpd.conf ".py" as a handler. Look for this line:
    AddHandler cgi-script .cgi .pl .py
Restart Apache
Top of .py script should show the location of the python intepreter, like this:
	#!/usr/local/bin/python3
	(use which python3 to get the path)
Make sure your .py script is executable (chmod 777)

Copy the nltk_data folder to the webserver. Or, run this script from the command line, but it opens up a Python app in a new window, so you have to be able to view it. Or run it locally and then copy the local nltk_data folder (about 4GB) to the server

Create a subfolder /client-data/client-<clientid>/transcripts/
	Make sure the /transcripts/ folder is writeable (chmod 777)
	The clientid is specified in the chatbot's .php file in the cliendid hidden input
	e.g.	<input id="clientid" value="010150" name="clientid" type="hidden"/>


#!/usr/local/bin/python3

# Run this script the first time only
import nltk
nltk.download()
nltk.download('punkt')
nltk.download('wordnet')
