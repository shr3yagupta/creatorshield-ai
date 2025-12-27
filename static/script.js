document.addEventListener("DOMContentLoaded", ()=>{

let latestReport = "";
let selectedLanguage = "english";

document.getElementById("language").onchange = (e)=>{
  selectedLanguage = e.target.value;

  if(selectedLanguage==="hindi"){
    document.getElementById("titleText").innerText="क्रिएटरशील्ड AI 🛡️";
    document.getElementById("panelTitle").innerText="थ्रेट इंटेलिजेंस पैनल";
  } else {
    document.getElementById("titleText").innerText="CreatorShield AI 🛡️";
    document.getElementById("panelTitle").innerText="Threat Intelligence Panel";
  }
};

document.getElementById("analyzeBtn").onclick = ()=>{
  
  const msg = messageInput.value.trim();
  if(msg===""){ alert("Enter message"); return; }

  resultPanel.style.display="block";
  explanation.innerText="Analyzing…";

  fetch("/analyze",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
      text:msg,
      language:selectedLanguage
    })
  })
  .then(r=>r.json())
  .then(showResult);
};

function showResult(d){

  riskBox.innerText = "Risk: "+d.risk_level;
  riskBox.className="risk";

  gauge.className="gauge";

  if(d.risk_level==="High"){riskBox.classList.add("high");gauge.classList.add("high")}
  else if(d.risk_level==="Medium"){riskBox.classList.add("medium");gauge.classList.add("medium")}
  else{riskBox.classList.add("low");gauge.classList.add("low")}

  attack.innerText = d.attack_type;
  platform.innerText = d.platform_detected;
  explanation.innerText = d.explanation;
  suggested_action.innerText = d.suggested_action;
  prevention.innerText = d.prevention_steps;
  flags.innerText = d.risky_elements;

  if(d.emergency_flag)
    emergency.classList.remove("hidden");

  latestReport = JSON.stringify(d,null,2);
}


// COPY
copyBtn.onclick=()=>{
  navigator.clipboard.writeText(latestReport);
  alert("Copied!");
}

// DOWNLOAD
downloadBtn.onclick=()=>{
  let a=document.createElement("a");
  a.href=URL.createObjectURL(new Blob([latestReport]));
  a.download="CreatorShield_Report.txt";
  a.click();
}

// WHATSAPP
waBtn.onclick=()=>{
  window.open("https://api.whatsapp.com/send?text="+encodeURIComponent(latestReport));
}

});

