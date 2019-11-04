// Load styleshets, supporting JS files, and then add the html to the document

window.onload = function() {
    var hostname = "//cdn.mikefield.ca"; // or cdn.mikefield.ca
    this.loadCssByHref( hostname+"/chatbot/css/chat.css");
    this.loadJSBySrc( hostname+"/chatbot/js/chatbot.js");
    this.loadJSBySrc( hostname+"/chatbot/conf/chatbot.conf.js");
    this.loadJSBySrc( hostname+"/chatbot/js/jquery-3.4.1.min.js");
    this.loadHtmlWithAjax( hostname+"/chatbot/plugin.html");
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

