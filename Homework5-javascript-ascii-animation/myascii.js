// Kin_sang  web2.0 2014.12.15
// 实现了Turbo 功能， stop \ start 的禁用功能   以及  动画前输入文本动画后返回文本的功能。

window.onload = function() {

    var btn = document.getElementsByTagName("input")[0];
    var btns = document.getElementsByTagName("input")[1];
    var siz = document.getElementsByName("size");

    var count = 0;
    var t;
    var content = [];
    var originText = "";
    btns.disabled = true;
    siz[1].checked = true;

    function getSize() {
        for (var i = 0; i < siz.length; i++) {
            if (siz[i].checked) {
                return siz[i].value;
            }
        }
    }

    function timedCount() {
        var anim = document.getElementsByTagName("select")[0];
        content = ANIMATIONS[anim.value].split("=====\n");
        var textArea = document.getElementById("displayarea");
        textArea.value = content[count];

        if (count < (content.length-1)) {
            count = count+1;
        } else {
            count = 0;
        }
        var textSize = getSize();
        
        if (textSize == "S") {
            textArea.style.fontSize = "7pt";
        } else if (textSize == "M") {
            textArea.style.fontSize = "12pt";
        } else {
            textArea.style.fontSize = "24pt";
        }
        var turbo = document.getElementsByName("turbo")[0];
        if (turbo.checked) {
            t=setTimeout(timedCount, 50);
        } else {
            t=setTimeout(timedCount, 200);
        }
        

    }

    btn.onclick = function() {
        originText = document.getElementById("displayarea").value;
        btn.disabled = true;
        btns.disabled = false;
        timedCount();
        console.log(siz);
    };

    btns.onclick = function() {
        clearTimeout(t);
        document.getElementById("displayarea").value = originText;
        btn.disabled = false;
    };
};
