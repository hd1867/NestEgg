function showMessage( subject, message )
{
    let messageBox = document.getElementById('messageBody');
    let subjectBox = document.getElementById('messageSubject');

    messageBox.innerText = message;
    subjectBox.innerText = subject;

    return 0;
}