function error(element, message){
    errorElements = element.getElementsByClassName("error");

    if (errorElements.length === 0){
        errorElement = document.createElement("p");
        errorElement.className = "error";
        element.appendChild(errorElement);
    }
    
    else{
        errorElement = element.getElementsByClassName("error")[0];
    }

    errorElement.textContent = message;
}

function removeError(element){
    errorElements = element.getElementsByClassName("error");

    if (errorElements.length === 0) return;

    element.removeChild(errorElement);
}

function validatePass(){
    let password = document.getElementById("password").value;
    
    if (password == document.getElementById("confirmPassword").value && password.length >= 8 && password.length <= 100){
        document.getElementById("submit").disabled = false;
    }

    else{
        document.getElementById("submit").disabled = true;
    }
}

function checkEmailInput(emailInput, disableButton){
    if (!emailInput.value){
        return;
    }

    emailStatus = validateEmail(emailInput.value);

    if (!emailStatus){
        error(emailInput.parentElement, "This is not a valid email.");
        disableButton.disabled = true;
        console.log(disableButton.disabled)
    }

    else{
        removeError(emailInput.parentElement);
        disableButton.disabled = false;
    }
}

function validateEmail(email){
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email.toLowerCase());
}
