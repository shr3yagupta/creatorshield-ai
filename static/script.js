document.addEventListener("DOMContentLoaded", ()=>{

  const analyzeBtn = document.getElementById("analyzeBtn");
  const input = document.getElementById("messageInput");
  const resultBox = document.getElementById("result");

  analyzeBtn.onclick = ()=>{

    const text = input.value.trim();
    if(text === ""){
      alert("Paste a message first");
      return;
    }

    resultBox.innerHTML = "⏳ Analyzing with AI...";

    fetch("/analyze",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({text:text})
    })
    .then(res=>res.json())
    .then(data=>{

      resultBox.innerHTML = `
      <b>Risk Level:</b> ${data.risk_level}<br>
      <b>Type:</b> ${data.attack_type}<br>
      <b>Platform:</b> ${data.platform_detected}<br>
      <b>Explanation:</b> ${data.explanation}<br>
      <b>Suggested Action:</b> ${data.suggested_action}<br>
      <b>Prevention:</b> ${data.prevention_steps}<br>
      <b>Emergency:</b> ${data.emergency_flag}
      `;
    })
    .catch(()=>{
      resultBox.innerHTML = "Error analyzing message!";
    });

  };

});
