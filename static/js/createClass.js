function generatePageForm()
{
    let selects = document.getElementsByName("pageType");
    let numAnswers;
    let answers;
    let numSelector;

    for (var i = 0; i < selects.length; i++) {
        let wrapper = document.createElement('div');
        let label = document.createElement('label');
        wrapper.className = "form-group";

        let pageForm = document.getElementById('page-' + i + '-form');
        pageForm.innerHTML = "";

        switch (selects[i].value) {
            case 'Text':
                label.innerText = "Text:";
                label.htmlFor = "text" + i;

                let textArea = document.createElement('textarea');
                textArea.name = "text" + i;
                textArea.id = "text" + i;
                textArea.rows = 10;
                textArea.cols = 80;
                textArea.className = "form-control";

                wrapper.append(label);
                wrapper.append(textArea);

                break;

            case 'Video':

            case 'Audio':
                label.innerText = "Upload a File:";
                label.htmlFor = "fileUpload" + i;

                let upload = document.createElement('input');
                upload.type = "file";
                upload.name = "fileUpload" + i;
                upload.id = "fileUpload" + i;
                upload.className = "form-control";

                wrapper.append(label);
                wrapper.append(upload);

                break;

            case 'Multiple Choice':
                numAnswers = 1;
                answers = document.createElement('div');

                let qLabel = document.createElement('label');
                qLabel.innerText = "Question:";
                qLabel.htmlFor = "McQ" + i;

                let mcQ = document.createElement('input');
                mcQ.type = 'text';
                mcQ.id = "McQ" + i;
                mcQ.name = "McQ"  + i;
                mcQ.className = 'form-control';

                label.innerText = "Number of Options"
                label.htmlFor = "numOptions" + i;

                numSelector = document.createElement("select");
                for( let k = 0; k < 10; k++ )
                {
                    let temp = document.createElement('option');
                    temp.innerText = k.toString();
                    numSelector.append(temp);
                }

                numSelector.name = "McNumAnswers" + i;
                numSelector.id = "McNumAnswers" + i;
                numSelector.onchange = function ()
                {
                    numAnswers = parseInt(numSelector.value);
                    console.log(numAnswers);
                    answers.innerHTML = "";

                    for(let j = 0; j < numAnswers; j++)
                    {
                        var tempWrap = document.createElement('div');
                        tempWrap.className = 'row';

                        var tempLabel = document.createElement("label");
                        tempLabel.htmlFor = "McA" + j;
                        tempLabel.innerText = "Answer  " + (j + 1);

                        tempWrap.append(tempLabel);

                        var tempInput = document.createElement('input');
                        tempInput.type = 'text';
                        tempInput.id = 'McA' +  i + j;
                        tempInput.name = 'McA' + i + j;

                        tempWrap.append(tempInput);

                        var tempCorrect = document.createElement('input');
                        tempCorrect.type = 'checkbox';
                        tempCorrect.id = 'McC' + i + j;
                        tempCorrect.name = "McC" + i + j;

                        tempWrap.append(tempCorrect);

                        answers.append(tempWrap);
                    }
                }

                wrapper.append(qLabel);
                wrapper.append(mcQ);
                wrapper.append(label);
                wrapper.append(numSelector);
                wrapper.append(answers);

                break;

            case 'Short Answer':
                label.innerText = "Question:"
                label.htmlFor = "SaQ" + i;

                let question = document.createElement('input');
                question.type = "text";
                question.name = "SaQ" + i;
                question.id = "SaQ" + i;
                question.className = "form-control";

                wrapper.append(label);
                wrapper.append(question);

                let label1 = document.createElement("label");

                label1.innerText = "Enter key phrases to search for(Separate entries with a semicolon):"
                label1.htmlFor = "SaKey" + i;

                let keyPhrases = document.createElement('input');
                keyPhrases.type = "text";
                keyPhrases.name = "SaKey" + i;
                keyPhrases.id = "SaKey" + i;
                keyPhrases.className = "form-control";

                wrapper.append(document.createElement("br"))
                wrapper.append(label1);
                wrapper.append(keyPhrases);

                break;

            case 'Select Answers':
                numAnswers = 1;
                let selAnswers = document.createElement('div');

                let qSelLabel = document.createElement('label');
                qSelLabel.innerText = "Question:";
                qSelLabel.htmlFor = "SelQ" + i;

                let selQ = document.createElement('input');
                selQ.type = 'text';
                selQ.id = "SelQ" + i;
                selQ.name = "SelQ"  + i;
                selQ.className = 'form-control';

                label.innerText = "Number of Options"
                label.htmlFor = "SelQ" + i;

                var selNumSelector = document.createElement("select");
                for( let j = 0; j < 10; j++ )
                {
                    let temp = document.createElement('option');
                    temp.innerText = j.toString();

                    selNumSelector.append(temp);
                }

                selNumSelector.name = "SelNumAnswers" + i;
                selNumSelector.id = "SelNumAnswers" + i;
                selNumSelector.onchange = function ()
                {
                    numAnswers = parseInt(selNumSelector.value);
                    console.log(numAnswers);
                    selAnswers.innerHTML = "";

                    for(let k = 0; k < numAnswers; k++)
                    {
                        var tempWrap = document.createElement('div');
                        tempWrap.className = 'row';

                        var tempLabel = document.createElement("label");
                        tempLabel.htmlFor = "SelA" + i + k;
                        tempLabel.innerText = "Answer  " + (k + 1);

                        var tempInput = document.createElement('input');
                        tempInput.type = 'text';
                        tempInput.id = 'SelA' + i + k;
                        tempInput.name = 'SelA' + i + k;

                        var tempCorrect = document.createElement('input');
                        tempCorrect.type = 'checkbox';
                        tempInput.id = 'SelC' + i + k;
                        tempInput.name = "SelC" + i + k;

                        tempWrap.append(tempLabel);
                        tempWrap.append(tempInput);
                        tempWrap.append(tempCorrect);

                        selAnswers.append(tempWrap);
                    }
                }

                wrapper.append(qSelLabel);
                wrapper.append(selQ);
                wrapper.append(label);
                wrapper.append(selNumSelector);
                wrapper.append(selAnswers);

                break;

            default:
                break;
        }

        pageForm.append(wrapper);
    }
}