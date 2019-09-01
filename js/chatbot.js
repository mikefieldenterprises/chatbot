function calculateResponse( userinput ) {
    var thisurl = "./chatbot-engine.py?q="+userinput;
    $.ajax({url: thisurl, success: function(result){
        removeDOMElement( "thinking-wrapper" );
        var jsonobj = JSON.parse(result);
        showResponse( jsonobj.content );
        console.log( jsonobj );
        if ( jsonobj.links != null ) {
            showResponseAddOn( jsonobj.links );
        }
    }});
}

function getFormattedDate(date) {
    return months[date.getMonth()]+" "+date.getDate()+", "+date.getFullYear();
}

function getFormattedTime(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}

function getFormattedTimestamp() {
    var today = new Date();
    var date = getFormattedDate(today);
    var time = getFormattedTime(today);
    return date+' '+time;
}

function removeDOMElement( id ) {
    var domelement = document.getElementById( id );
    domelement.parentNode.removeChild( domelement );
}

function scrollToBottom(){
    var objid = "conversation";
    var obj = document.getElementById(objid);
    if (typeof($) !== "undefined") {
        $('#' + objid).animate({
        scrollTop: obj.scrollHeight - obj.clientHeight
        }, 500);
    } else {
        obj.scrollTop = obj.scrollHeight;
    }
}

function showResponse(responsetext) {

    var timestamp = getFormattedTimestamp();
    var responseTemplate = '<div class="response">'+
'                                        <div class="response-date" style="color: rgba(255, 255, 255, 0.7);">'+timestamp+'</div>'+
'                                        <div bot="" class="response-wrapper avatar-offset">'+
'                                            <div class="avatar"></div>'+
'                                            <div class="text response-content">'+
'                                                <div class="message" style="background: rgb(233, 238, 244); border-color: rgb(233, 238, 244); color: rgb(100, 100, 100);">'+responsetext+'</div>'+
'                                            </div>'+
'                                        </div>'+
'                                    </div>';
    document.getElementById("conversation-wrapper").innerHTML += responseTemplate;
    scrollToBottom();
    updateChatTranscript( "bot", timestamp, responsetext );

}

function showResponseAddOn(responsetext) {

    var timestamp = getFormattedTimestamp();
    var responseTemplate = '<div class="response">'+
'                                        <div bot="" class="response-wrapper avatar-offset">'+
'                                            <div class="text response-content">'+
'                                                <div class="message" style="background: rgb(233, 238, 244); border-color: rgb(233, 238, 244); color: rgb(100, 100, 100);">'+responsetext+'</div>'+
'                                            </div>'+
'                                        </div>'+
'                                    </div>';
    document.getElementById("conversation-wrapper").innerHTML += responseTemplate;
    scrollToBottom();
    updateChatTranscript( "bot", timestamp, responsetext );

}

function showUserInput( userinput ) {

    var timestamp = getFormattedTimestamp();
    var userInputTemplate = '<div class="response">'+
'                                        <div class="response-date" style="color: rgba(255, 255, 255, 0.7);">'+timestamp+'</div>'+
'                                        <div user="" class="response-wrapper">'+
'                                            <div class="user response-content">'+
'                                                <div class="message" style="color: rgb(250, 250, 250); background: rgb(31, 140, 235); border-color: rgb(31, 140, 235);">'+userinput+'</div>'+
'                                                <div class="info" style="color: rgb(100, 100, 100);"><!----></div>'+
'                                            </div>'+
'                                        </div>'+
'                                    </div>';
    document.getElementById("userBoxNew").value = "";
    document.getElementById("conversation-wrapper").innerHTML += userInputTemplate;
    scrollToBottom();
    updateChatTranscript( "You", timestamp, userinput ); 
}

function showThinking() {

    var timestamp = getFormattedTimestamp();
    var responseTemplate = '<div class="response" id="thinking-wrapper">'+
'                                        <div class="response-date" style="color: rgba(255, 255, 255, 0.7);">'+timestamp+'</div>'+
'                                        <div bot="" class="response-wrapper avatar-offset">'+
'                                            <div class="avatar"></div>'+
'                                            <div class="text response-content">'+
'                                                <div class="message" style="background: rgb(233, 238, 244); border-color: rgb(233, 238, 244); color: rgb(100, 100, 100);" id="thinking-body">...</div>'+
'                                            </div>'+
'                                        </div>'+
'                                    </div>';
    document.getElementById("conversation-wrapper").innerHTML += responseTemplate;
    showThinkingDots();
    scrollToBottom();

}

function showThinkingDots() {
    var divid = "thinking-body"
    setTimeout( function() {
        updateInnerHTML( divid, ". &nbsp;");
        setTimeout( function() {
                updateInnerHTML( divid, ".. ");
                setTimeout( function() {
                    updateInnerHTML( divid, "...");
                    showThinkingDots();
                }, 500);
        }, 500);
    }, 500);
}

function showWelcomeMessage() {
    showResponse(welcomemessage);
}

function talk() {
    var userinput = document.getElementById("userBoxNew").value;
    if ( userinput != "" ) {
        showUserInput( userinput );
        showThinking();
        calculateResponse( userinput );
    }
} 

function toggleChat() {
    if ( document.getElementById("chatbot-chat").style.display == "none" ) {
        // Open chat
        document.getElementById("chatbot-chat").style.display = "block";
        document.getElementById("chatbot-button").style.display = "none";
        document.getElementById("chatbot-chat").style.visibility = "visible";
        document.getElementById("chatbot-button").style.visibility = "hidden";
        if ( document.getElementById("chat-started").value != "true" ) {
            showWelcomeMessage();
            document.getElementById("chat-started").value = "true";
        }
    } else {
        // Close chat
        document.getElementById("chatbot-chat").style.display = "none";
        document.getElementById("chatbot-button").style.display = "block";
        document.getElementById("chatbot-chat").style.visibility = "hidden";
        document.getElementById("chatbot-button").style.visibility = "visible";
    }
}

function updateChatTranscript( user, timestamp, inputtext ) {
    var obj = new Object();
    obj.user = user;
    obj.timestamp = timestamp;
    obj.text = inputtext;
    var existingvals = document.getElementById("chat-transcript").value;
    var existingobjs = [];
    if ( existingvals != "" ) {
        existingvals += ",";
    }
    existingvals += JSON.stringify(obj);
    document.getElementById("chat-transcript").value = existingvals;
}

function updateInnerHTML( divid, content ) {
    var obj = document.getElementById(divid);
    if ( obj != null ) {
        obj.innerHTML = content;
    }
}