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
            let answerList;
            answerList = forms[i].elements[1].value;


            for(let j = 0; j < answerList.length; answerList++)
            {
                if (!(correctAnswer.trim().includes(answerList[j])))
                {
                    console.log("Question Incorrect")
                    totalWrong++;
                    break;
                }
            }
        }
        else
        {
            let answerString = "";
            correctAnswer = forms[i].elements[0].value;

            for(let j = 0; j < forms[i].elements.length; j++)
            {
                if(i >= 1 && forms[i].elements[j].checked)
                {
                    answerString += (j - 1);
                }
            }

            if(answerString !== correctAnswer)
            {
                console.log("Question Incorrect");
                totalWrong++;
            }
        }
    }

    let classid = document.getElementById('classId').value;
    let score = (1 - totalWrong/totalQuestions).toString();

    window.location.href = "/submitClass?score=" + score +"&classid=" + classid;
}