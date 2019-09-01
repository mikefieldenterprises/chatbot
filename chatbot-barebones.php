<html>
<head>
<script>
function calculateResponse( userinput ) {
    var know = {
        "hello" : "hi",
        "how are you?" : "good",
        "ok" : ":)"
    };
    if (userinput in know) {
        showResponse( know[userinput] );
    } else {
        showResponse( "I don't understand ... ");
    }
}


function showUserInput( userinput ) {

    document.getElementById("userBox1").value = "";
    document.getElementById("chatLog").innerHTML += "<div class=\"userinput\">"+userinput+"</div><div class=\"break\">&nbsp;</div>";
}

function showResponse(responsetext) {

    document.getElementById("chatLog").innerHTML += "<div class=\"response\">"+responsetext+"</div><div class=\"break\">&nbsp;</div>";

}

function talk() {
    var userinput = document.getElementById("userBox1").value;
    showUserInput( userinput );
    calculateResponse( userinput );
    scrollToBottom();
} 


</script>
</head>
<body>
    <h1>Welcome to the Chatbot test</h1>

    <p id="chatLog"></p>
    <input id="userBox1" type="text" onkeydown="if (event.keyCode == 13) {talk()}" placeholder="Type your message here"/>
    <input id="userBoxHidden" type="hidden" value=""/>


</body>
</html>