# OUTPUT FORMATTER MODULE
import json

def formatAsJSONForWeb( mydict ):
    return json.dumps( mydict )

# Surround plain text answer with JSON string
def formatWithJSON( msg ):
    return "{\"content\":\""+msg+"\", \"channel\":\"\", \"step\":\"\"}"