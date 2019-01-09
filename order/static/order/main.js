
(function ($) {
    "use strict";


    /*==================================================================
    [ Focus input ]*/

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
				$(".waga").val(1000).prop("readonly", false);
            $(".dlugosc").val(200).prop("readonly",true);
			$(".szerokosc").val(140).prop("readonly",true);
			$(".wysokosc").val(200).prop("readonly", false);
        } 
    });
	});
	

	
	
	$(document).ready(function() {
  $(".dlugosc").on("keydown", function(e) {
    var char = e.originalEvent.key.replace(/[^0-9^.^,]/, "");
    if (char.length == 0 && !(e.originalEvent.ctrlKey || e.originalEvent.metaKey)) {
      e.preventDefault();
    }
  });

  $(".dlugosc").bind("paste", function(e) {
    var numbers = e.originalEvent.clipboardData
      .getData("text")
      .replace(/[^0-9^.^,]/g, "");
    e.preventDefault();
    var the_val = parseFloat(numbers);
    if (the_val > 0) {
      $(this).val(the_val.toFixed(2));
    }
  });

  $(".dlugosc").focusout(function(e) {
    if (!isNaN(this.value) && this.value.length != 0) {
		if(this.value <= 0){
		this.value=1;}
      this.value = Math.abs(parseFloat(this.value)).toFixed(2);
    } else {
      this.value = 1;
    }
  });
  $(".szerokosc").on("keydown", function(e) {
    var char = e.originalEvent.key.replace(/[^0-9^.^,]/, "");
    if (char.length == 0 && !(e.originalEvent.ctrlKey || e.originalEvent.metaKey)) {
      e.preventDefault();
    }
  });

  $(".szerokosc").bind("paste", function(e) {
    var numbers = e.originalEvent.clipboardData
      .getData("text")
      .replace(/[^0-9^.^,]/g, "");
    e.preventDefault();
    var the_val = parseFloat(numbers);
    if (the_val > 0) {
      $(this).val(the_val.toFixed(2));
    }
  });

  $(".szerokosc").focusout(function(e) {
    if (!isNaN(this.value) && this.value.length != 0) {
			if(this.value <= 0){
		this.value=1;}
      this.value = Math.abs(parseFloat(this.value)).toFixed(2);
    } else {
      this.value = 1;
    }
  });
  $(".wysokosc").on("keydown", function(e) {
    var char = e.originalEvent.key.replace(/[^0-9^.^,]/, "");
    if (char.length == 0 && !(e.originalEvent.ctrlKey || e.originalEvent.metaKey)) {
      e.preventDefault();
    }
  });

  $(".wysokosc").bind("paste", function(e) {
    var numbers = e.originalEvent.clipboardData
      .getData("text")
      .replace(/[^0-9^.^,]/g, "");
    e.preventDefault();
    var the_val = parseFloat(numbers);
    if (the_val > 0) {
      $(this).val(the_val.toFixed(2));
    }
  });

  $(".wysokosc").focusout(function(e) {
    if (!isNaN(this.value) && this.value.length != 0) {
			if(this.value <= 0){
		this.value=1;}
      this.value = Math.abs(parseFloat(this.value)).toFixed(2);
    } else {
      this.value = 1;
    }
  });
  
  $(".waga").on("keydown", function(e) {
    var char = e.originalEvent.key.replace(/[^0-9^.^,]/, "");
    if (char.length == 0 && !(e.originalEvent.ctrlKey || e.originalEvent.metaKey)) {
      e.preventDefault();
    }
  });

  $(".waga").bind("paste", function(e) {
    var numbers = e.originalEvent.clipboardData
      .getData("text")
      .replace(/[^0-9^.^,]/g, "");
    e.preventDefault();
    var the_val = parseFloat(numbers);
    if (the_val > 0) {
      $(this).val(the_val.toFixed(2));
    }
  });

  $(".waga").focusout(function(e) {
    if (!isNaN(this.value) && this.value.length != 0) {
			if(this.value <= 0){
		this.value=1;}
      this.value = Math.abs(parseFloat(this.value)).toFixed(2);
    } else {
      this.value = 1;
    }
  });
});
	
	
	
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

	
	
	
	
	
	
	
})(jQuery);