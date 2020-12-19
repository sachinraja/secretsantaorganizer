function submitSendEmails(sendEmailButton){
    if (!confirm("Are you sure you want to send emails to all the participants with their recipients?")){
        return
    }
    
    //stop user from clicking twice
    sendEmailButton.disabled = true;
    sendEmailButton.value = "Sending...";

    //submit form
    document.getElementById("sendEmails").submit();
}