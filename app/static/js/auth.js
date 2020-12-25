function logout(){
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/logout")
    xhr.send();

    xhr.onload = function(){
        if (xhr.status == 200){
            location.reload();
        }
    }
}