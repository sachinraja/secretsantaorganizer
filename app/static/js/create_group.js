function addOrganizer(){
    let inputs = document.getElementById("organizers");
    let inputsLength = inputs.children.length;

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
        newInputEmail.onchange = function(){checkEmailInput(this);};
        newInputEmail.maxLength = 200;
        
        newInputDiv.appendChild(newInputEmail);
        inputs.appendChild(newInputDiv);

        inputsLength++;
    }
}

function addParticipant(){
    let inputs = document.getElementById("participants");
    let inputsLength = inputs.children.length;

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
        newInput.className = "participantName";
        newInput.onchange = function(){updateRestrictions(this.parentElement);};
        newInput.maxLength = 50;
        newInputDiv.appendChild(newInput);
        
        let newInputEmail = document.createElement("input");
        newInputEmail.name = `participant${inputsLength}`;
        newInputEmail.type = "text";
        newInputEmail.placeholder = "Email";
        newInputEmail.className = "emailInput";
        newInputEmail.onchange = function(){checkEmailInput(this);};
        newInputEmail.maxLength = 200;
        newInputDiv.appendChild(newInputEmail);

        //restrictions
        let restrictionsHeader = document.createElement("h4");
        restrictionsHeader.textContent = "Restrictions";
        restrictionsHeader.className = "restrictionsHeader";
        newInputDiv.appendChild(restrictionsHeader);

        let restrictionsDiv = document.createElement("div");
        let newInputRestriction = document.createElement("select");
        newInputRestriction.name = `participant${inputsLength}restriction`;
        newInputRestriction.className = "restrictionsInput";
        newInputRestriction.cols = 50;
        restrictionsDiv.appendChild(newInputRestriction);

        restrictionsDiv.innerHTML += `<i onclick="addRestriction(this.parentElement);" class="addButton fas fa-plus fa-lg"></i>`;
        newInputDiv.appendChild(restrictionsDiv);

        inputs.appendChild(newInputDiv);

        inputsLength++;
    }
}

function addRestriction(restrictionsDiv){
    let newInputRestriction = restrictionsDiv.getElementsByClassName("restrictionsInput")[0].cloneNode(deep=true);
    newInputRestriction.value = "";
    restrictionsDiv.insertBefore(newInputRestriction, restrictionsDiv.children[restrictionsDiv.children.length - 1]);
}

function getAllOptions(){
    //generate options
    options = [];

    let option = document.createElement("option");
    option.text = "";
    option.value = "";
    options.push([option, ""]);

    for (let participantName of document.getElementsByClassName("participantName")){
        if (!participantName.value)  continue;

        let option = document.createElement("option");
        option.text = participantName.value;
        option.value = participantName.value;
        options.push([option, option.textContent]);
    }

    return options;
}

function addOptionsToRestriction(inputRestriction, options){
    let value = inputRestriction.value;
    inputRestriction.innerHTML = "";
    
    for (let [optionElement, optionText] of options){
        let newOption = optionElement.cloneNode();
        newOption.textContent = optionText;
        inputRestriction.add(newOption);
    }

    inputRestriction.value = value;
}

function updateRestrictions(){
    let options = getAllOptions();

    let inputRestrictions = document.getElementsByClassName("restrictionsInput");

    for (let inputRestriction of inputRestrictions){
        addOptionsToRestriction(inputRestriction, options);
    }
}