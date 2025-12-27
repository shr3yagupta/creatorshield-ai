const analyzeBtn = document.getElementById("analyzeBtn");
const result = document.getElementById("result");

// ========== TEXT ANALYSIS ==========
analyzeBtn.onclick = () => {
    result.textContent = "Analyzing...";

    fetch("/analyze",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            text: messageInput.value
        })
    })
    .then(r=>r.json())
    .then(d=>{
        result.textContent = JSON.stringify(d,null,2);
    });
};


// ========== IMAGE ANALYSIS ==========
const imageBtn = document.getElementById("analyzeImageBtn");
const imgResult = document.getElementById("imgResult");

imageBtn.onclick = () => {

    imgResult.textContent = "Analyzing Screenshot...";

    let form = new FormData();
    form.append("image", imageInput.files[0]);

    fetch("/image",{
        method:"POST",
        body: form
    })
    .then(r=>r.json())
    .then(d=>{
        imgResult.textContent = JSON.stringify(d,null,2);
    });
};
