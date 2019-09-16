# chatbot

PURPOSE

Adds a basic slot-and-answer chatbot to a website
Conversations (aka "channels") are defined in the ./client-data/client-<clientid>/channel-descriptions.txt file


TO RUN THIS APPLICATION

Add to httpd.conf ".py" as a handler. Look for this line:
    AddHandler cgi-script .cgi .pl .py
Allow htaccess Override in httpd.conf. Look for this line:
	AllowOverride All
Restart Apache
Top of .py script should show the location of the python intepreter, like this:
	#!/usr/local/bin/python3
	(use which python3 to get the path)
Make sure your chatbot-main.py script is executable (chmod 777)

Copy the nltk_data/tokenizers folder to the webserver (about 50MB), or run these two python commands the first time only:
	import nltk
	nltk.download('punkt')

Create a subfolder /client-data/client-<clientid>/transcripts/
	Make sure the /transcripts/ folder is writeable (chmod 777)

Create a .htaccess file in the root folder of the chatbot, with the following line:
Header set Access-Control-Allow-Origin: "*"



TO INCLUDE THE CHATBOT IN YOUR WEBSITE

Copy the following code into your webpage, just before your closing </body> tag. (Be sure to specify the correct client id)

<script type="text/javascript">
    window.__client = window.__client || {};
    window.__client.id = "010150";
    (function() {
        var c = document.createElement('script'); c.type = 'text/javascript'; c.async = true;
        c.src = ('https:' == document.location.protocol ? 'https://' : 'http://') + 'cdn.mikefield.ca/chatbot/js/plugin.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(c, s);
    })();
</script>