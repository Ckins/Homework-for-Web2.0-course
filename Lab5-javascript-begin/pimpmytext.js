window.onload = function(){
    function changeText() {
        var textbox = document.getElementById('Text');
        textbox.style.fontSize = "24pt";
        var chbox = document.getElementById("cb");
        if (chbox.checked) {
            addClass('Text', 'green');
        }
    }
    function hasClass(element, className) {
        var ele = document.getElementById(element);
        if (ele.hasAttribute("class")) {
            return true;
        } else {
            return false;
        }
    }
    function addClass(element, className) {
        var ele = document.getElementById(element);
        if (hasClass(element, className)) {
            ele.className += ' '+className;
        } else {
            ele.setAttribute("class", className);
        }
    }
    var btn = document.getElementsByTagName("button")[0];
    btn.onclick = changeText;

}
