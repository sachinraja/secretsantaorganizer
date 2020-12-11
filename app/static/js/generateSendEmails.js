function makeRequest(organizers, matches){
    let xhr = new XMLHttpRequest();

    xhr.open("POST", "/send-email");

    xhr.onreadystatechange = function(){
        if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            window.location.href = xhr.responseText;
        }
    }
    
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({
        "generateSendEmails" : true,
        "organizers" : organizers,
        "matches" : matches
    }));
}
