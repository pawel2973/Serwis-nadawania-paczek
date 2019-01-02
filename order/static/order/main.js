
(function ($) {
    "use strict";


    /*==================================================================
    [ Focus input ]*/
      $('.inputPaka').each(function(){
        $(this).on('blur', function(){
            if($(this).val().trim() != "") {
                $(this).addClass('has-val');
            }
            else {
                $(this).removeClass('has-val');
            }
        })    
    });
  $(document).ready(function() {
    $("#show_hide_password a").on('click', function(event) {
        event.preventDefault();
        if($('#show_hide_password input').attr("type") == "text"){
            $('#show_hide_password input').attr('type', 'password');
            $('#show_hide_password i').addClass( "fa-eye-slash" );
            $('#show_hide_password i').removeClass( "fa-eye" );
        }else if($('#show_hide_password input').attr("type") == "password"){
            $('#show_hide_password input').attr('type', 'text');
            $('#show_hide_password i').removeClass( "fa-eye-slash" );
            $('#show_hide_password i').addClass( "fa-eye" );
        }
    });
});

$(document).ready(function(){
    $("#id_type_2").on("click", function () {
        if ($(this).is(":checked")) {
				$(".waga").val(1).prop("readonly", false);
            $(".dlugosc").val(9).prop("readonly", false);
			$(".szerokosc").val(14).prop("readonly", false);
			$(".wysokosc").val(7).prop("readonly", false);
        } 
		
    });
})
$(document).ready(function(){
    $("#id_type_0").on("click", function () {
        if ($(this).is(":checked")) {
			$(".waga").val(1).prop("readonly", true);
            $(".dlugosc").val(35).prop("readonly", true);
			$(".szerokosc").val(25).prop("readonly", true);
			$(".wysokosc").val(5).prop("readonly", true);
        } 
    });
});


	$(document).ready(function(){
    $("#id_type_1").on("click", function () {
        if ($(this).is(":checked")) {
				$(".waga").val(1000).prop("readonly", true);
            $(".dlugosc").val(200).prop("readonly",false);
			$(".szerokosc").val(140).prop("readonly",false);
			$(".wysokosc").val(200).prop("readonly", true);
        } 
    });
	});
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
})(jQuery);