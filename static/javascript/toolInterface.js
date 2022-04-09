//@ni: Function to count number of words in a textarea box
const countWords = (getId,setId)  => {
if (getId && setId){
text = document.getElementById(getId).value;
console.log(text.length)
isMatch = text.match(/\w+/g);
totalWords = isMatch ? isMatch.length : 0 ;
document.getElementById(setId).textContent = totalWords;
}
};

//@ni: Basically this will open another child window and execute javascript print on that so that the textarea
//and other things don't get printed.
const printTextArea = targetTextArea => {
        childWindow = window.open('','childWindow','location=yes, menubar=yes, toolbar=yes');
        childWindow.document.open();
        childWindow.document.write('<html><head></head><body>');
        childWindow.document.write('<center><h2>Crafted by Text Insights : NLP based toolkit</h2></center>');
        childWindow.document.write(targetTextArea.value.replace(/\n/gi,'<br>'));
        childWindow.document.write('</body></html>');
        childWindow.print();
        childWindow.document.close();
        childWindow.close();
}

//Function for sending response with input data to flask app & get respective output
const getOutputEvent  = toolName => {
       // function to handle success
       function success() {
           var data = this.responseText;
           var outputBox = document.getElementById('output-content');
           outputBox.disabled=false;
           outputBox.value=data;
           countWords('output-content','output-count');
           console.log(data);
       }
       // function to handle error
       function error(err) {
           console.log('Request Failed', err); //error details will be in the "err" object
       }
        const url = `\\toolkit\\${toolName}`
        const xhr = new XMLHttpRequest();
        xhr.onload = success; // call success function if request is successful
        xhr.onerror = error;  // call error function if request failed
        inputData =  document.getElementById('input-content').value;
        rangeValue = document.getElementById('rangeValue').innerHTML

        if ( document.getElementById("input-count").textContent ){
            console.log(` Sending Response to ${url}`);
            xhr.open('POST', url);
            xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            xhr.send(`inputData=${inputData}&rangeValue=${rangeValue}&requiredkey=key`);
        }

   }


