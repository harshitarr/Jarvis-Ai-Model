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
})