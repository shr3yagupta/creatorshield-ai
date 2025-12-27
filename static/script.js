const btn = document.getElementById("analyzeBtn");
const result = document.getElementById("result");

btn.onclick = () => {
    fetch("/analyze",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            text:document.getElementById("messageInput").value
        })
    })
    .then(r=>r.json())
    .then(d=>{
        result.innerText = JSON.stringify(d,null,2);
    });
};

// Screenshot
document.getElementById("imageBtn").onclick = ()=>{
    let file = document.getElementById("imageInput").files[0];
    let f = new FormData();
    f.append("image",file);

    fetch("/image",{method:"POST",body:f})
    .then(r=>r.json())
    .then(d=>{
        result.innerText = JSON.stringify(d,null,2);
    });
};

// Recovery
const recoverBtn = document.getElementById("recoverBtn");
const recoverySteps = document.getElementById("recoverySteps");

recoverBtn.onclick = ()=>{
    fetch("/recovery",{method:"POST"})
    .then(r=>r.json())
    .then(d=>{
        recoverySteps.innerHTML = "";
        d.steps.forEach(s=>{
            let li = document.createElement("li");
            li.textContent = s;
            recoverySteps.appendChild(li);
        });
    });
};

function scanLink(){
 fetch("/link",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({url:document.getElementById("urlInput").value})
 })
 .then(r=>r.json())
 .then(d=>{
   document.getElementById("urlResult").innerText =
    `Risk: ${d.risk_level} | ${d.explanation}`;
 });
}
