    var str1="";
    // str1+="<link rel='stylesheet'";
    // str1+="href='https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha.6/css/bootstrap.min.css'>";
    // str1+="<link rel='stylesheet'";
    // str1+="href='https://cdnjs.cloudflare.com/ajax/libs/bootstrap-material-design/4.0.2/bootstrap-material-design.css'>";
    str1+="<link rel='stylesheet' href='https://fonts.googleapis.com/icon?family=Material+Icons'></link>";
    
    $("head").append(str1);

    var str2="";
    str2+="<div id='body'>";

    str2+="<div id='chat-circle' class='btn btn-raised'>";
    str2+="<div id='chat-overlay'></div>";
    str2+="<i class='material-icons'>chat</i>";
    str2+="</div>";

    str2+="<div class='chat-box'>";
    str2+="<div class='chat-box-header'>";
    str2+="WrenchBot";
    str2+="<span class='chat-box-toggle'><i class='material-icons'>close</i></span>";
    str2+="</div>";
    str2+="<div class='chat-box-body'>";
    str2+="<div class='chat-box-overlay'>";
    str2+="</div>";
    str2+="<div class='chat-logs'>";
    str2+="</div>";
    str2+="<!--chat-log -->";
    str2+="</div>";
    str2+="<div class='chat-input'>";
    str2+="<form>";
    str2+="<input type='text' id='chat-input' placeholder='Send a message...' />";
    str2+="<button type='submit' class='chat-submit' id='chat-submit'><i class='material-icons'>send</i></button>";
    str2+="</form>";
    str2+="</div>" ;
    str2+="</div>";
    str2+="</div>";

    $("body").append(str2);

    var INDEX = 0; 
    var xhttp = new XMLHttpRequest();
    var msg = "";


  $("#chat-submit").click(function(e) {
    e.preventDefault();
    msg = $("#chat-input").val(); 
    if(msg.trim() == ''){
      return false;
    }
    //alert(msg);
    xhttp.open("POST","http://127.0.0.1:5000",true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange=function(){
      if (this.readyState==4 && this.status==200){
        msg=this.responseText;  
        generate_message(msg, "bot");
      }
    };
    //alert("msg="+String(msg));
    xhttp.send("msg="+String(msg));
    generate_message(msg, 'user'); 
    /*
    var buttons = [
        {
          name: 'Existing User',
          value: 'existing'
        },
        {
          name: 'New User',
          value: 'new'
        }
      ];
    */

  })
  
  function generate_message(msg, type) {
    INDEX++;
    var str="";
    str += "<div id='cm-msg-"+INDEX+"' class=\"chat-msg "+type+"\">";
    str += "          <span class=\"msg-avatar\">";
    str += "            <img src=chrome-extension://gnhcdocdlbjbhifoiegiommbghlchbgk/"+type+"-logo.png>";
    str += "          <\/span>";
    str += "          <div class=\"cm-msg-text\">";
    str += msg;
    str += "          <\/div>";
    str += "        <\/div>";
    $(".chat-logs").append(str);
    $("#cm-msg-"+INDEX).hide().fadeIn(300);
    if(type == 'self'){
     $("#chat-input").val(''); 
    }    
    $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight}, 1000);    
  }  

  $("#chat-circle").click(function() {  
    if (INDEX==0){
    generate_message("I am WrenchBot","bot");
    generate_message("Please enter your email address","bot");
    }  
    $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
  })
  
  $(".chat-box-toggle").click(function() {
    $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
  })
  