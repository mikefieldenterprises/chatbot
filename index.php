<?php include("conf/chatbot.conf.php"); ?>
<html>
<head>
<link href="css/chat.css" rel="stylesheet">
</head>
<body style="background-color:#000000; color:#FFFFFF;">
    <h1>Welcome to the Sample Chatbot</h1>

    Try the chatbot in the bottom-right corner.

<div id="chatbot-chat" style="display:none;">

    <div id="app">
        <div id="chat">
            <div class="chat-window">
                <div class="chat-window-wrapper" style="background: rgba(33, 38, 46, 0.95);">
                    <div class="window-content-wrapper">
                        <div class="head avatar-offset" style="background: rgb(31, 140, 235); color: rgb(250, 250, 250); height: 90px;">
                            <div class="company" style="opacity: 1;">
                                <div class="avatar-outer-wrapper">
                                    <div class="avatar-wrapper">
                                        <div class="avatar">
                                            <div class="avatar-default"></div>
                                        </div> 
                                        <div class="avatar-status" style="border-color: rgb(31, 140, 235);"></div>
                                    </div>
                                </div>
                                <div class="name"><?php echo $botusername; ?></div>
                                <div class="status">Online</div>
                                <div class="social"><!----> <!----> <!----></div>
                            </div>
                        </div>
                        <div class="window-content"style="height: calc(100% - 90px);">

                            <!-- Begin Conversation -->
                            <div class="conversation" id="conversation">
                                <div class="conversation-wrapper" id="conversation-wrapper">
                                    <!--<div class="response">
                                        <div class="response-date" style="color: rgba(255, 255, 255, 0.7);">Today 4:42 PM</div>
                                        <div bot="" class="response-wrapper avatar-offset">
                                            <div class="avatar"></div>
                                            <div class="text response-content">
                                                <div class="message" style="background: rgb(233, 238, 244); border-color: rgb(233, 238, 244); color: rgb(100, 100, 100);">Welcome to the coffee shop! What can I get you?</div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="response">
                                        <div class="response-date" style="color: rgba(255, 255, 255, 0.7);">Today 4:42 PM</div> 
                                        <div bot="" class="response-wrapper avatar-offset">
                                            <div class="avatar"></div>
                                            <div class="button response-content">
                                                <div class="item">
                                                    <div class="message" style="background: rgb(233, 238, 244); border-color: rgb(233, 238, 244); color: rgb(100, 100, 100);">Check out our menu!</div>
                                                    <div class="buttons" style="background: rgb(233, 238, 244); border-color: rgb(233, 238, 244);">
                                                        <div class="button" style="border-top-color: rgba(100, 100, 100, 0.2); color: rgb(31, 140, 235);">Go to the menu</div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="response">
                                        <div class="response-date" style="color: rgba(255, 255, 255, 0.7);">Today 4:50 PM</div> 
                                        <div user="" class="response-wrapper">
                                            <div class="user response-content">
                                                <div class="message" style="color: rgb(250, 250, 250); background: rgb(31, 140, 235); border-color: rgb(31, 140, 235);">Hi</div>
                                                <div class="info" style="color: rgb(100, 100, 100);"></div>
                                            </div>
                                        </div>
                                    </div>
            
                                    <div class="response">
                                        <div class="response-date" style="color: rgba(255, 255, 255, 0.7);">Today 4:50 PM</div>
                                        <div bot="" class="response-wrapper avatar-offset">
                                            <div class="avatar"></div>
                                            <div class="text response-content">
                                                <div class="message" style="background: rgb(233, 238, 244); border-color: rgb(233, 238, 244); color: rgb(100, 100, 100);">I missed what you said. Say it again?</div>
                                            </div>
                                        </div>
                                    </div>-->
                                </div>
                            </div> <!-- end Conversation -->

                            <!-- Begin User Input -->
                            <div class="typing" style="background: rgb(33, 38, 46); opacity: 0.6;">
                                <input id="userBoxNew" type="text" maxlength="256" placeholder="Type your message here" style="color: rgb(255, 255, 255);" onkeydown="if (event.keyCode == 13) {talk()}"> 
                                <div class="actions"><div class="send" onclick="talk();">
                                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 24 24" xml:space="preserve" class="" style="fill: rgb(255, 255, 255);"><path d="M22,11.7V12h-0.1c-0.1,1-17.7,9.5-18.8,9.1c-1.1-0.4,2.4-6.7,3-7.5C6.8,12.9,17.1,12,17.1,12H17c0,0,0-0.2,0-0.2c0,0,0,0,0,0c0-0.4-10.2-1-10.8-1.7c-0.6-0.7-4-7.1-3-7.5C4.3,2.1,22,10.5,22,11.7z"></path></svg>
                                </div></div>
                            </div>
                            <!-- End User Input -->

                        </div> <!-- end window-content -->
                    </div> <!-- end window-content-wrapper -->
        
                    <div class="window-close" style="background: rgb(31, 140, 235);" onclick="toggleChat();">
                        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" title="close the chat" style="fill: rgb(250, 250, 250);"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path> <path d="M0 0h24v24H0z" fill="none"></path></svg>
                    </div> 

                </div> <!-- end chat-window-wrapper -->
                <a target="_blank" href="http://www.mikefield.ca" class="powered">Powered by <span>Mike Field Enterprises</span></a>
            </div> <!-- end chat-window -->
        </div> <!-- end chat -->
    </div> <!-- end app -->
    
</div> <!-- end chatbot-chat -->

<div id="chatbot-button" onclick="toggleChat();">
    <div class="chat-button-theme-bubble">
    <div class="chat-button" style="background: rgb(31, 140, 235); color: rgb(250, 250, 250);">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" class="chat-icon" style="stroke: rgb(250, 250, 250);"><path d="M9.37,1.34H10.8a8.2,8.2,0,0,1,0,16.39H9.37a10,10,0,0,1-2.68-.45c-.55-.15-2.23,1.81-2.63,1.36s.05-2.79-.41-3.23q-.28-.27-.54-.57A8.2,8.2,0,0,1,9.37,1.34Z" style="fill: none;"></path> <line x1="6.37" y1="7.04" x2="12.58" y2="7.04" style="fill: none; stroke-linecap: round;"></line> <line x1="6.37" y1="9.66" x2="14.31" y2="9.66" style="fill: none; stroke-linecap: round;"></line> <line x1="6.37" y1="12.28" x2="11.42" y2="12.28" style="fill: none; stroke-linecap: round;"></line></svg>
    </div>
    </div>
</div> <!-- end chatbot-button -->

<input id="chat-started" value="false" name="chat-started" type="hidden"/>
<input id="channel" value="1" name="channel" type="hidden"/>
<input id="step" value="1" name="step" type="hidden"/>
<input id="clientid" value="010150" name="clientid" type="hidden"/>
<input id="sessionid" value="" name="sessionid" type="hidden"/>


<script src="conf/chatbot.conf.js"></script>
<script src="js/chatbot.js"></script>
<script src="js/jquery-3.4.1.min.js"></script>

</body>
</html>