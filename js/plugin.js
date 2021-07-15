// Load styleshets, supporting JS files, and then add the html to the document

window.onload = function() {
    window.__hostname = "cdn.mikefield.ca"; // or localhost
    window.__default_colour = "#1F8CEB";
    this.loadCssByHref( "//"+window.__hostname+"/chatbot/css/chat.css");
    this.loadJSBySrc( "//"+window.__hostname+"/chatbot/js/chatbot.js");
    this.loadJSBySrc( "//"+window.__hostname+"/chatbot/conf/chatbot.conf.js");
    this.loadJSBySrc( "//"+window.__hostname+"/chatbot/js/jquery-3.4.1.min.js");
    this.loadHtmlWithAjax( "//"+window.__hostname+"/chatbot/plugin.html");
}

function createDivById( divid ) {
    var elem = document.createElement("div");
    elem.id = divid;
    document.body.appendChild( elem );
}

function loadCssByHref( fullurl ) {
    var link = document.createElement( "link" );
    link.href = fullurl;
    link.type = "text/css";
    link.rel = "stylesheet";
    link.media = "screen,print";
    document.getElementsByTagName( "head" )[0].appendChild( link );
}

function loadHtmlWithAjax( fullurl ) {
    divid = "chatbot-plugin";
    createDivById( divid );
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        document.getElementById( divid ).innerHTML = this.responseText;
        setChatbotColours();
        }
    };
    xhttp.open("GET", fullurl, true);
    xhttp.send();   
}

function loadJSBySrc( fullurl ) {
    var script = document.createElement("script");
    script.src = fullurl;
    document.head.appendChild(script);
}

function setChatbotColours() {
    var fullurl = "//"+window.__hostname+"/chatbot/client-data/client-"+window.__client.id+"/client-config.json";
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var jsonobj = JSON.parse(this.responseText);
            setColours(jsonobj);
        }
    };
    xhttp.open("GET", fullurl, true);
    xhttp.send();
}

function setColours( jsonobj ) {
    window.__colour_bubble = (typeof jsonobj.colour_bubble !== "undefined") ? jsonobj.colour_bubble : window.__default_colour;
    window.__colour_title = (typeof jsonobj.colour_bubble !== "undefined") ? jsonobj.colour_title : window.__default_colour;
    window.__colour_buttons = (typeof jsonobj.colour_bubble !== "undefined") ? jsonobj.colour_buttons : window.__default_colour;
    setBackgroundColorByDiv("chat-button", window.__colour_bubble);
    setBackgroundColorByDiv("window-close", window.__colour_title);
    setBackgroundColorByDiv("avatar-offset", window.__colour_title);
    setBorderColorByDiv("avatar-status", window.__colour_title);
    let root = document.documentElement;
    root.style.setProperty("--button-color",window.__colour_buttons);
}

function setBackgroundColorByDiv( divid, thiscolour ) {
    document.getElementById(divid).style.backgroundColor = thiscolour;
}

function setBorderColorByDiv( divid, thiscolour ) {
    document.getElementById(divid).style.borderColor = thiscolour;
}