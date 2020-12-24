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

        let newInputEmail = document.createElement("input");
        newInputEmail.name = "organizer";
        newInputEmail.type = "text";
        newInputEmail.placeholder = "Email";
        newInputEmail.onchange = function(){checkEmailInput(this, document.getElementById("generate"));};
        newInputEmail.maxLength = 200;
        
        newInputDiv.appendChild(newInputEmail);
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
        newInputEmail.onchange = function(){checkEmailInput(this, document.getElementById("generate"));};
        newInputEmail.maxLength = 200;

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
