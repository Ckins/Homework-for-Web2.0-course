//Web2.0 hw6  
// Kin_sang 2014.12.24

window.onload = function(){
        var shuffleBtn = document.getElementById("shufflebutton");
        var puzzleArea = document.getElementById("puzzlearea");
        var puzzlePieces = puzzleArea.getElementsByTagName("div");
        var isMoving = false;
        var step = 20;
        var blank = {
            top : (Math.floor(puzzlePieces.length/4)*100)+'px',
            left : (puzzlePieces.length%4*100)+'px'
        }
        var totalStep = 0;
        function hasClass(ele, className) {
            if (ele.hasAttribute("class")) {
                return true;
            }
            return false;
        }
        function addClass(ele, className) {
            if (hasClass(ele, className)) {
              ele.className += ' '+className;
              console.log(className);
            } else {
              ele.setAttribute("class", className);
            }
        }
        
        function initialPieces() {
            // 使用函数闭包
            for (var i = 0; i < puzzlePieces.length; i++) {
                puzzlePieces[i].style.top = (Math.floor(i/4)*100)+'px';
                puzzlePieces[i].style.left = (i%4*100)+'px';
                puzzlePieces[i].style.backgroundPosition = -1*(i%4*100)+'px '+(-1)*(Math.floor(i/4)*100)+'px';
                puzzlePieces[i].onclick = function(index){
                    return function() {
                        swapPosition(index, blank, true);
                    };
                }(i);
                addClass(puzzlePieces[i], 'puzzlepiece');
                if (isMovable(puzzlePieces[i])) {
                    console.log(i);
                    addClass(puzzlePieces[i], 'movablepiece');
                }
            }
        }

        function hasFinished() {
            for (var i = 0; i < puzzlePieces.length; i++) {
                if (parseInt(puzzlePieces[i].style.top) != -parseInt(puzzlePieces[i].style.backgroundPositionY)) {
                    return false;
                }
                if (parseInt(puzzlePieces[i].style.left) != -parseInt(puzzlePieces[i].style.backgroundPositionX)) {
                    return false;
                }
            }
            return true;
        }

        function cateChange(element) {
            element.style.left = parseInt(element.style.left)+getSign(element).x*step+'px';
            element.style.top = parseInt(element.style.top)+getSign(element).y*step+'px';
        }

        function movePiece(i, delay, tt, tl) {

            var element = puzzlePieces[i];
            if (element.style.top != blank.top || element.style.left != blank.left) {
                cateChange(element);              
                isMoving = true;
                timer = setTimeout(function(){movePiece(i,delay,tt,tl);}, delay);
            } else {
                clearTimeout(timer);
                isMoving = false;
                blank.top = tt;
                blank.left = tl;
                if (hasFinished() && totalStep) {
                    alert("You Win");
                }
            }
            for (var index = 0; index < puzzlePieces.length; index++) {
                            puzzlePieces[index].className = 'puzzlepiece';
                            if (isMovable(puzzlePieces[index])) {
                            console.log(index);
                            addClass(puzzlePieces[index], 'movablepiece');
                            }
            }
        }

        function swapPosition(i, blank, delay) {
            totalStep += 1;
            
            var element = puzzlePieces[i];
            var tmpTop = element.style.top;
            var tmpLeft = element.style.left;

            if (!isMovable(element) || isMoving == true) {
                return;
            }    
            if (!delay) {
                element.style.left = blank.left;
                element.style.top = blank.top;
                blank.top = tmpTop;
                blank.left = tmpLeft;
            } else {      
                movePiece(i, delay, tmpTop, tmpLeft);

            }
        }

        function isMovable(element) {
            var dist = {
                y : Math.abs(parseInt(element.style.top)-parseInt(blank.top)),
                x  : Math.abs(parseInt(element.style.left)-parseInt(blank.left))
            }
            if ((dist.y + dist.x) == 100) {
                return true;
            }
            return false;
        }

        function getSign(element) {
            var tmpY = parseInt(element.style.top)-parseInt(blank.top),
            tmpX = (parseInt(element.style.left)-parseInt(blank.left));
            return {
                y : -(tmpY)/Math.abs(tmpY),
                x  : -(tmpX)/Math.abs(tmpX)
            }
        }
        function reLoad() {

        }

        shuffleBtn.onclick = function() {
            totalStep = 0;
            var num = 888;
            while (num--) {
                for (var i = 0; i < puzzlePieces.length; i++) {
                    swapPosition(i, blank, false);
                }
            }
            for (var index = 0; index < puzzlePieces.length; index++) {
                            puzzlePieces[index].className = 'puzzlepiece';
                            if (isMovable(puzzlePieces[index])) {
                            console.log(index);
                            addClass(puzzlePieces[index], 'movablepiece');
                            }
            }
        }
        initialPieces();
};
