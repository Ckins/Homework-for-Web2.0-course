$(window).ready(function(){
    function adapt_screen() {
        function change_reference_size() {
            var $reference_block = $(".reference");
            var height = $(".teacher_img").height();
            $reference_block.css("height",height+"px");
        }

        function change_background_size() {
            var height = $("#information").height();
            var width = $("#information").width();
            $("#overlay").css({"height":height+"px","width":width+"px"});
        }

        function change_logo_size() {
            var height = $(".teacher_img").width();
            $(".teacher_img").css({"height":height+"px"});
            var $teacher_img = $("#teacher_img");
            var width = $("#my_picture").width();
            var height =$("#my_picture").height();
            console.log(height);
            var size;
                if (width >height)
                    size = height
                else
                    size =width;
            $teacher_img.css({"width":size+"px","height":size+"px"});
        }
        change_logo_size();
        change_reference_size();
    }

    var $backGround = $("#background");
    $(window).resize(function() {
        resizeBackground();
    });

    function resizeBackground() {
        var height = $(window).height();
        var width = $(window).width();
        adapt_screen();
        $backGround.css({
            'width': width+'px',
            'height': height+'px'
        });
    }


    function addRemark() {
        $("#new_remark").hide();

        $("#add_remark").click(function() {
            if ($("#new_remark").css('display') == 'none') {
                $("#new_remark").fadeIn();
            } else {
                $("#new_remark").fadeOut();
            }
        });

        $("#submit_remark").click(function() {
            var text = $("#remark_text").val();
            if (text) {
                var data = $("#remark_form").serialize();
                $.ajax({
                    type: "post",
                    url: '/comment'+window.location.pathname,
                    data: data,
                    success: function(data) {
                        new_data = data.split("|");
                        $("#all_remarks").append('<li>'+new_data[0]+' ('+new_data[1]+' '+new_data[2]+')</li>');
                        $("#remark_text").val("");
                        $("#new_remark").fadeOut();
                    }
                });
            }
            
        });
    }

    function addPoint() {
        $("#new_point").hide();

        $("#add_point").click(function() {
            if ($("#new_point").css('display') == 'none') {
                $("#new_point").fadeIn();
            } else {
                $("#new_point").fadeOut();
            }
            
        });

        $("#submit_point").click(function() {
            var text = $("#point_text").val();
            if (text) {
                var data = $("#point_form").serialize();
                $.ajax({
                    type: "post",
                    url: '/point'+window.location.pathname,
                    data: data,
                    success: function(data) {
                        $("#all_points").append('<li>'+data+'</li>');
                        $("#point_text").val("");
                        $("#new_point").fadeOut();
                    }
                });
            }
        });
    }


    addRemark();
    addPoint();
    resizeBackground();

});