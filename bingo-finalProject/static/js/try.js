$(window).ready(function(){
    adapt_screen();
	$("#information").hide();
});
$("#bf_page_menu").find("li").click(function() {
	$("#bf_page_menu").animate({left:"-=330px"});
    $(".container").fadeOut();
	$("#information").fadeIn();
    adapt_screen();
});
$("#back_bt").click(function() {
    $("#bf_page_menu").animate({left:"+=330px"});
    $("#information").fadeOut();
});
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
function adapt_screen() {
    function change_reference_size() {
        var $reference_block = $(".reference");
        var height = $reference_block.width();
        $reference_block.css("height",height+"px");
    }

    function change_background_size() {
        var height = $("#information").height();
        var width = $("#information").width();
        console.log($("#information").height());
        $("#overlay").css({"height":height+"px","width":width+"px"});
    }

    function change_side_bar() {
        var height = $(window).height();
        if ($("#bf_page_menu").height() < height)
            $("bf_page_menu").css("height",height+"px");
    }

    function change_logo_size() {
        var $teacher_img = $("#teacher_img");
        var width = $("#my_picture").width();
        var height = $(".teacher_img").width();
        console.log(height);
        $(".teacher_img").css({"height":height+"px"});
        var height =$("#my_picture").height();
        var size;
            if (width >height)
                size = height
            else
                size =width;
            $teacher_img.css({"width":size+"px","height":size+"px"});
    }
    change_side_bar();
    change_background_size();
    change_logo_size();
    change_reference_size();
}