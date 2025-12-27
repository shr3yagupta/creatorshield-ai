document.addEventListener("DOMContentLoaded",()=>{

let latestReport="";
let activeMode="text";
let selectedLanguage="english";

const $=id=>document.getElementById(id);


/* LANGUAGE */
$("language").onchange=(e)=>{
 selectedLanguage=e.target.value;

 if(selectedLanguage==="hindi"){
  $(".logo").innerText="🛡️ क्रिएटरशील्ड AI";
  $("premiumBtn").innerText="क्रिएटरशील्ड प्रीमियम";
  $("langLabel").innerText="भाषा:";
  $("headline").innerText="ठगी होने से पहले ठगी पहचानो।";
  $("subtitle").innerText="क्रिएटर्स के लिए AI सुरक्षा सहायक — संदेश, स्क्रीनशॉट या वॉइस अपलोड करें।";
  $("panelTitle").innerText="थ्रेट इंटेलिजेंस पैनल";
 }
 else{
  $(".logo").innerText="🛡️ CreatorShield AI";
  $("premiumBtn").innerText="CreatorShield Premium";
  $("langLabel").innerText="Language:";
  $("headline").innerText="Detect scams before they detect you.";
  $("subtitle").innerText="AI security assistant — Text, Screenshot, or Voice.";
  $("panelTitle").innerText="Threat Intelligence Panel";
 }
};


/* TABS */
textTab.onclick=()=>{
 activeMode="text";
 textMode.classList.add("show");
 imageMode.classList.remove("show");
 voiceMode.classList.remove("show");

 textTab.classList.add("active");
 imgTab.classList.remove("active");
 voiceTab.classList.remove("active");
};

imgTab.onclick=()=>{
 activeMode="image";
 imageMode.classList.add("show");
 textMode.classList.remove("show");
 voiceMode.classList.remove("show");

 imgTab.classList.add("active");
 textTab.classList.remove("active");
 voiceTab.classList.remove("active");
};

voiceTab.onclick=()=>{
 activeMode="voice";
 voiceMode.classList.add("show");
 textMode.classList.remove("show");
 imageMode.classList.remove("show");

 voiceTab.classList.add("active");
 imgTab.classList.remove("active");
 textTab.classList.remove("active");
};


/* ANALYZE */
analyzeBtn.onclick=()=>{
 if(activeMode==="text") analyzeText();
 else if(activeMode==="image") analyzeImage();
 else analyzeVoice();
};


function analyzeText(){
 fetch("/analyze",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({
   text:messageInput.value,
   language:selectedLanguage
  })
 })
 .then(r=>r.json())
 .then(showResult);
}


function analyzeImage(){
 let f=new FormData();
 f.append("image",imageInput.files[0]);

 fetch("/image",{method:"POST",body:f})
 .then(r=>r.json())
 .then(showResult);
}


function analyzeVoice(){
 let f=new FormData();
 f.append("audio",voiceInput.files[0]);

 fetch("/voice",{method:"POST",body:f})
 .then(r=>r.json())
 .then(showResult);
}


function showResult(d){
 riskBox.innerText="Risk: "+d.risk_level;
 riskBox.className="risk";
 gauge.className="gauge";

 if(d.risk_level==="High"){riskBox.classList.add("high");gauge.classList.add("high")}
 else if(d.risk_level==="Medium"){riskBox.classList.add("medium");gauge.classList.add("medium")}
 else{riskBox.classList.add("low");gauge.classList.add("low")}

 attack.innerText=d.attack_type;
 platform.innerText=d.platform_detected;
 explanation.innerText=d.explanation;
 suggested_action.innerText=d.suggested_action;
 prevention.innerText=d.prevention_steps;
 flags.innerText=d.risky_elements;

 if(d.emergency_flag)
   emergencyNotice.classList.remove("hidden");

 latestReport=JSON.stringify(d,null,2);
}


/* UTILITIES */
copyBtn.onclick=()=>navigator.clipboard.writeText(latestReport);

downloadBtn.onclick=()=>{
 let a=document.createElement("a");
 a.href=URL.createObjectURL(new Blob([latestReport]));
 a.download="CreatorShield_Report.txt";
 a.click();
}

waBtn.onclick=()=>window.open(
 "https://api.whatsapp.com/send?text="+encodeURIComponent(latestReport)
);


/* RECOVERY */
recoverBtn.onclick=()=>{
 fetch("/recovery",{method:"POST"})
 .then(r=>r.json())
 .then(d=>{
  recoverySteps.innerHTML="";
  d.steps.forEach(s=>{
   let li=document.createElement("li");
   li.innerText=s;
   recoverySteps.appendChild(li);
  });
 });
};


/* TRENDING */
trendBtn.onclick=()=>{
 fetch("/trending",{method:"POST"})
 .then(r=>r.json())
 .then(d=>trendingList.innerText=d.scams);
};


/* GLOBAL THREAT RADAR */
globalBtn.onclick=()=>{
 fetch("/global-trends",{method:"POST"})
 .then(r=>r.json())
 .then(data=>{
  let html="";
  data.trends.forEach(t=>{
    html+=`
     <div class="card">
       <h3>${t.title}</h3>
       <p><strong>Platform:</strong> ${t.platform}</p>
       <p><strong>Region:</strong> ${t.region}</p>
       <p><strong>Risk:</strong> ${t.risk}</p>
       <p>${t.description}</p>
     </div>
    `;
  });

  globalList.innerHTML=html;
 });
};


/* PREMIUM POPUP */
const popup=premiumPopup;
window.openPremium=()=>popup.classList.remove("hidden");
window.closePremium=()=>popup.classList.add("hidden");
closePremiumBtn.onclick=()=>popup.classList.add("hidden");
popup.addEventListener("click",(e)=>{if(e.target===popup) popup.classList.add("hidden")});


/* CHATBOT */
chatbot.onclick=()=>chatWindow.classList.remove("hidden");
closeChat.onclick=()=>chatWindow.classList.add("hidden");

sendChat.onclick=()=>{
 let msg=chatInput.value.trim();
 if(!msg) return;

 chatMessages.innerHTML+=`<p><strong>You:</strong> ${msg}</p>`;
 chatInput.value="";

 fetch("/chat",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({message:msg})
 })
 .then(r=>r.json())
 .then(d=>{
  chatMessages.innerHTML+=`<p><strong>AI:</strong> ${d.reply}</p>`;
  chatMessages.scrollTop=chatMessages.scrollHeight;
 });
};

});

