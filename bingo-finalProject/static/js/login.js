$(function() {
    var $backGround = $("#background");
    $(window).resize(function() {
        resizeBackground();
    }); 
    function resizeBackground() {
        var height = $(window).height();
        var width = $(window).width();
        $backGround.css({
            'width': width+'px',
            'height': height+'px'
        });
    } 
    resizeBackground();
});