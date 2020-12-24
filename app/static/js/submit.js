function submitForm(button, value){
    //stop user from clicking twice
    button.disabled = true;
    button.value = value;

    //submit form
    button.form.submit();
}

function submitSendEmails(sendEmailButton){
    if (!confirm("Are you sure you want to send emails to all the participants with their recipients?")){
        return;
    }
    
    submitForm(sendEmailButton, "Sending...");
}

function createGroupSubmitGenerate(generateButton){
    generateButton.disabled = true;
    generateButton.value = "Generating...";
    
    let form = document.getElementById("createGroup");

    let inputType = document.createElement("input");
    inputType.type = "hidden";
    inputType.name = "type";
    inputType.value = "generate";
    form.appendChild(inputType);

    generateButton.form.submit();
}

function createGroupSubmitSendEmails(sendEmailButton){
    if (!confirm("Are you sure you want to send emails to all the participants with their recipients?")){
        return;
    }

    sendEmailButton.disabled = true;
    sendEmailButton.value = "Sending...";
    
    let form = document.getElementById("createGroup");

    let inputType = document.createElement("input");
    inputType.type = "hidden";
    inputType.name = "type";
    inputType.value = "sendEmails";
    form.appendChild(inputType);

    sendEmailButton.form.submit();
}