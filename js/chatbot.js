function calculateResponse( userinput ) {
    var step = document.getElementById("step").value;
    var channel = document.getElementById("channel").value;
    var clientid = window.__client.id;
    var sessionid = document.getElementById("sessionid").value;
    var thisurl = "//cdn.mikefield.ca/chatbot/chatbot-main.py?q="+userinput+"&cn="+channel+"&sn="+step+"&cid="+clientid+"&sid="+sessionid;
    $.ajax({url: thisurl, success: function(result){
        removeDOMElement( "thinking-wrapper" );
        var jsonobj = JSON.parse(result);
        showResponse( jsonobj.content );
        if ( jsonobj.links != null ) {
            showResponseAddOn( jsonobj.links );
        }
        if ( jsonobj.buttonoptions != null && jsonobj.buttonoptions.length > 0 ) {
            showButtonOptions( jsonobj.buttonoptions );
            disableTextInput();
        } else {
            enableTextInput();
            flashCursor();
        }
        document.getElementById("step").value = jsonobj.step;
        document.getElementById("channel").value = jsonobj.channel;
        if ( jsonobj.closechat ) {
            pauseThenCloseChat();
        }
    }});
}

function setChatbotNameAndAvatar() {
    var clientid = window.__client.id;
    setChatbotName( clientid );
    setChatbotAvatar();
 }

function setChatbotName( clientid ) {
    var thisurl = "//cdn.mikefield.ca/chatbot/client-data/client-"+clientid+"/client-config.json";
    $.ajax({url: thisurl, success: function(result){
        var jsonobj = result;
        var chatbotfullname = jsonobj.chatbot_fullname;
        updateInnerHTML( "chatbotfullname", chatbotfullname );
    }});
}

function setChatbotAvatar() {
    var chatbotavatar = getChatbotAvatarUrl();
    document.getElementById("chatbotavatar").style.backgroundImage = "url('"+chatbotavatar+"')";;
}

function getChatbotAvatarUrl() {
    return "//cdn.mikefield.ca/chatbot/client-data/client-"+window.__client.id+"/avatar.jpg";
}

function disableTextInput() {
    document.getElementById("userBoxNew").disabled = true;
    document.getElementById("userBoxNew").placeholder = "";
}

function enableTextInput() {
    document.getElementById("userBoxNew").disabled = false;
    document.getElementById("userBoxNew").placeholder = "Type your message here";
}

function flashCursor() {
    var div = document.getElementById("userBoxNew");
    if ( div.value == "" ) {
        div.style.color = '#999999';
        setTimeout( function() {
            document.getElementById("userBoxNew").style.color = '#FFFFFF';
            setTimeout( function() {
                flashCursor();
            }, 1000 );
        }, 1000 );
    } else {
        div.style.color = "#FFFFFF";
    }
}

function formatNumberToTwoDigits( num ) {
    return (num<10) ? "0"+(num) : num;
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

// Returns timestamp like 20190930-145802
function getNewSessionId() {
    var date = new Date();
    return date.getFullYear()+""+
        formatNumberToTwoDigits(date.getMonth()+1)+""+
        formatNumberToTwoDigits(date.getDate())+"-"+
        formatNumberToTwoDigits(date.getHours())+
        formatNumberToTwoDigits(date.getMinutes())+
        formatNumberToTwoDigits(date.getSeconds());
}

function pauseThenCloseChat() {
    setTimeout( function() {
        disableTextInput();
        document.getElementById("step").value = "1";
        document.getElementById("channel").value = "1";
        document.getElementById("sessionid").value = "";
        document.getElementById("chat-started").value = "false";
        document.getElementById("conversation-wrapper").innerHTML = "";
        toggleChat();        
    }, 5000 );
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

function showButtonOptions( buttonoptions ) {

    var responseTemplate = '<div class="response" id="buttondiv">'+
'                                        <div bot="" class="response-wrapper avatar-offset">'+
'                                            <div class="text response-content">';
    for ( var i=0; i<buttonoptions.length; i++ ) {
        optiontext = buttonoptions[i].replace("'", "\\'");
        responseTemplate += '                        <div class="buttonoption" onclick="talkWithInput(\''+optiontext+'\'); removeDOMElement(\'buttondiv\');" style="background: rgb(233, 238, 244); border-color: rgb(233, 238, 244); color: rgb(100, 100, 100);">'+buttonoptions[i]+'</div>';
    }
    responseTemplate += '                    </div>'+
'                                        </div>'+
'                                    </div>';
    document.getElementById("conversation-wrapper").innerHTML += responseTemplate;
    scrollToBottom();

}

function showResponse(responsetext) {

    var timestamp = getFormattedTimestamp();
    var responseTemplate = '<div class="response">'+
'                                        <div class="response-date" style="color: rgba(255, 255, 255, 0.7);">'+timestamp+'</div>'+
'                                        <div bot="" class="response-wrapper avatar-offset">'+
'                                            <div class="avatar" style="background-image:url(\''+getChatbotAvatarUrl()+'\')"></div>'+
'                                            <div class="text response-content">'+
'                                                <div class="message" style="background: rgb(233, 238, 244); border-color: rgb(233, 238, 244); color: rgb(100, 100, 100);">'+responsetext+'</div>'+
'                                            </div>'+
'                                        </div>'+
'                                    </div>';
    document.getElementById("conversation-wrapper").innerHTML += responseTemplate;
    scrollToBottom();

}

function showResponseAddOn(responsetext) {

    var responseTemplate = '<div class="response">'+
'                                        <div bot="" class="response-wrapper avatar-offset">'+
'                                            <div class="text response-content">'+
'                                                <div class="message" style="background: rgb(233, 238, 244); border-color: rgb(233, 238, 244); color: rgb(100, 100, 100);">'+responsetext+'</div>'+
'                                            </div>'+
'                                        </div>'+
'                                    </div>';
    document.getElementById("conversation-wrapper").innerHTML += responseTemplate;
    scrollToBottom();

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
}

function showThinking() {

    var timestamp = getFormattedTimestamp();
    var responseTemplate = '<div class="response" id="thinking-wrapper">'+
'                                        <div class="response-date" style="color: rgba(255, 255, 255, 0.7);">'+timestamp+'</div>'+
'                                        <div bot="" class="response-wrapper avatar-offset">'+
'                                            <div class="avatar" style="background-image:url(\''+getChatbotAvatarUrl()+'\')"></div>'+
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

function startChat() {
    document.getElementById("chat-started").value = "true";
    document.getElementById("sessionid").value = getNewSessionId();
    showThinking();
    setChatbotNameAndAvatar();
    calculateResponse( "" ); // Load channel 1 step 1
}

function talk() {
    var userinput = document.getElementById("userBoxNew").value;
    talkWithInput( userinput );
} 

function talkWithInput( userinput ) {
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
            startChat();
        }
    } else {
        // Close chat
        document.getElementById("chatbot-chat").style.display = "none";
        document.getElementById("chatbot-button").style.display = "block";
        document.getElementById("chatbot-chat").style.visibility = "hidden";
        document.getElementById("chatbot-button").style.visibility = "visible";
    }
}

function updateInnerHTML( divid, content ) {
    var obj = document.getElementById(divid);
    if ( obj != null ) {
        obj.innerHTML = content;
    }
}