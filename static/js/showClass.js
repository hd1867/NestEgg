function submitAnswers()
{
    let i; 
    let totalQuestions, totalWrong = 0;
    let correctAnswer;
    //console.log( document.forms );
    forms = document.forms;
    
    
    for(i = 0; i < forms.length; i++)
    {
        let formId = forms[i].id;
        totalQuestions = forms.length;
        if(formId.includes('mc'))
        {
            console.log("Multiple Choice");
            let correctIndex = parseInt(forms[i].elements[0].value) + 1;
            correctAnswer = forms[i].elements[correctIndex];
            
            if (!(correctAnswer.checked))
            {
                console.log("Question Incorrect")
                totalWrong++;
            }
        }
        else if(formId.includes('sa')) 
        {
            console.log("Short Answer");
            correctAnswer = forms[i].elements[0].value; 
            
            if(!(forms[i].elements[1].value.includes(correctAnswer)))
            {
                console.log("Question Incorrect")
                totalWrong++;
            }
        }
        else
        {
            console.log("Select Answer");
            correctAnswers = forms[i].elements[0].value;
            console.log(forms[i].elements);
        }
    }
    return (1 - totalWrong/totalQuestions);
}