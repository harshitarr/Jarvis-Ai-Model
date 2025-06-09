$(document).ready(function(){

    $('.text').textillate({

        loop:true,
        sync:true,
        in:{
            effect:"bounceIn",
        },
        out:{
            effect:"bounceOut",
        },
    })

    //siri configuration

    var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 840,
    height: 200,
    style:"ios9",
    amplitude:"1",
    speed:"0.30",
    autostart:true
  });

  //siri message - animations

      $('.siri-message').textillate({

        loop:true,
        sync:true,
        in:{
            effect:"fadeInUp",
            sync:true
        },
        out:{
            effect:"fadeOutUp",
            sync:true
        },
    })

    // mic button click event

    $("#MicBtn").click(function (e) { 
        
        eel.playAssistantSound()
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()()
    });

function doc_keyup(e) {
    if (e.key === 'j' && e.metaKey) {  // also fixed 'metakey' to 'metaKey'
        eel.playAssistantSound();
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()();  // double () is okay if allCommands returns a function
    }
}

document.addEventListener('keyup', doc_keyup, false);

    // to play assisatnt 
    function PlayAssistant(message) {

        if (message != "") {

            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);

        }

    }

        // toogle fucntion to hide and display mic and send button 
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

        // key up event handler on text box
    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)
    
    });
    
    // send button event handler
    $("#SendBtn").click(function () {
    
        let message = $("#chatbox").val()
        PlayAssistant(message)

    })

    $("#chatbox").keypress(function (e) {
    key = e.which;
    if (key == 13) {
        let message = $("#chatbox").val();
        PlayAssistant(message);
    }
  });
})