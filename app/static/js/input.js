function addOrganizer(){
    let inputs = document.getElementById("organizers");
    let inputsLength = inputs.getElementsByTagName("div").length;

    if (inputsLength >= 15){
        error(inputs, "Too many organizers. The limit is 15.");
        return;
    }

    let newInputsCount = 15 - inputsLength;

    if (newInputsCount > 3){
        newInputsCount = 3;
    }

    for (let i=0; i < newInputsCount; i++){
        let newInputDiv = document.createElement("div");

        let newInputID = document.createElement("input");
        newInputID.name = `organizer${inputsLength}`;
        newInputID.type = "text";
        newInputID.placeholder = "ID";
        newInputID.maxLength = 10;

        newInputDiv.appendChild(newInputID);
        inputs.appendChild(newInputDiv);

        inputsLength++;
    }
}

function addParticipant(){
    let inputs = document.getElementById("participants");
    let inputsLength = inputs.getElementsByTagName("div").length;

    if (inputsLength >= 100){
        error(inputs, "Too many participants. The limit is 100.");
        return;
    }

    let newInputsCount = 100 - inputsLength;

    if (newInputsCount > 3){
        newInputsCount = 3;
    }

    for (let i=0; i < newInputsCount; i++){
        let newInputDiv = document.createElement("div");

        let newInput = document.createElement("input");
        newInput.name = `participant${inputsLength}`;
        newInput.type = "text";
        newInput.placeholder = `Participant ${inputsLength+1}`;
        newInput.maxLength = 50;
        
        let newInputEmail = document.createElement("input");
        newInputEmail.name = `participant${inputsLength}`;
        newInputEmail.type = "text";
        newInputEmail.placeholder = "Email";
        newInputEmail.className = "emailInput";
        newInputEmail.onchange = function(){checkEmailInput(this);};
        newInputEmail.maxLength = 100;

        let newInputRestrictions = document.createElement("textarea");
        newInputRestrictions.name = `participant${inputsLength}`;
        newInputRestrictions.placeholder = "Enter restrictions separated by line.";
        newInputRestrictions.className = "restrictionsInput";
        newInputRestrictions.cols = 50;

        newInputDiv.appendChild(newInput);
        newInputDiv.appendChild(newInputEmail);
        newInputDiv.appendChild(newInputRestrictions);
        inputs.appendChild(newInputDiv);

        inputsLength++;
    }
}

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

function checkEmailInput(emailInput){
    if (!emailInput.value){
        return;
    }

    emailStatus = validateEmail(emailInput.value);

    if (!emailStatus){
        error(emailInput.parentElement, "This is not a valid email.");
    }

    else{
        removeError(emailInput.parentElement);
    }
}

function validateEmail(email){
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email.toLowerCase());
}

function submitGenerateForm(){
    let form = document.getElementById("secretSanta");
    let hiddenInput = document.createElement("input");
    hiddenInput.name = "generate";
    form.appendChild(hiddenInput);
    form.action = "/send-email";
    form.submit();
}