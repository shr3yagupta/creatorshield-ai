document.addEventListener("DOMContentLoaded", ()=>{

  const analyzeBtn = document.getElementById("analyzeBtn");
  const resultBox = document.getElementById("result");
  const input = document.getElementById("messageInput");

  analyzeBtn.onclick = ()=>{

    const text = input.value.trim();

    if(text === ""){
        alert("Please paste a message first");
        return;
    }

    fetch("/analyze",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({text:text})
    })
    .then(res=>res.json())
    .then(data=>{
        resultBox.innerHTML = `<pre>${data.ai}</pre>`;
    })
    .catch(()=>{
        resultBox.innerHTML = "Error analyzing message";
    });

  }

});
