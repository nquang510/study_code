$(document).ready(function(){
	$('form#up').submit(function(){
		var mail = $.trim($('#up_mail').val());
		var pass = $.trim($('#up_pass').val());
		var confirm = $.trim($('#up_pass_confirm').val());
		var flag = true;
		var check_mail = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;

		console.log(check_mail.test(mail));
		if(mail == ''){
			$('p.mail_error').text("Please enter your email !");
			$("input#up_mail").css({"background" : "rgba(255, 147, 146, 0.3)", "border" : "2px solid rgb(255, 0, 0, 0.3)"});
			flag = false;
		} else if(!check_mail.test(mail)) {
			$('p.mail_error').text("Please enter the email in valid format !");
			$("input#up_mail").css({"background" : "rgba(255, 147, 146, 0.3)", "border" : "2px solid rgb(255, 0, 0, 0.3)"});
			flag = false;
		} else {
			flag = true;
			$('p.mail_error').text("");
			$("input#up_mail").css({"background" : "none" , "border" : "2px solid #ddd"});
		}

		if(pass ==''){
			$('p.pass_error').text("Please enter your password !");
			$("input#up_pass").css({"background" : "rgba(255, 147, 146, 0.3)", "border" : "2px solid rgb(255, 0, 0, 0.3)"});
			flag = false;
		} else {
			$('p.pass_error').text("");
			$("input#up_pass").css({"background" : "none" , "border" : "2px solid #ddd"});
		}
		if(confirm == '') {
			$('p.confirm_error').text("Please confirm your password !");
			$("input#up_pass_confirm").css({"background" : "rgba(255, 147, 146, 0.3)", "border" : "2px solid rgb(255, 0, 0, 0.3)"});
			flag = false;
		} else if(confirm != pass) {
			$('p.pass_error').text("Please enter same password !");
			$('p.confirm_error').text("Please enter same password !");
			$("input#up_pass_confirm").css({"background" : "rgba(255, 147, 146, 0.3)", "border" : "2px solid rgb(255, 0, 0, 0.3)"});
			$("input#up_pass").css({"background" : "rgba(255, 147, 146, 0.3)", "border" : "2px solid rgb(255, 0, 0, 0.3)"});
			flag = false;
		} else {
			$('p.confirm_error').text("");
			$("input#up_pass_confirm").css({"background" : "none" , "border" : "2px solid #ddd"});
		}



		if($('input.check').is(':checked')) {
			console.log('ok');
			$('p#agree').text("");
		} else {
			$('p#agree').text("Please agree our Terms and Policy");
			$('p#agree').css({"color" : "red"})
			flag = false;
		}



		if (flag == true) {
			$('p#success').text("✔ You have successfully registered");
			$('p#success').css({'color' : 'green'})
		} else {
			$('p#success').text("");
		}

		return false;

	})
	$('form#in').submit(function(){
		var mail = $.trim($('#in_mail').val());
		var pass = $.trim($('#in_pass').val());
		flag = true;



		if (mail == 'ut@gmail.com' && pass == '123456') {
			$('p.enter_mail').text('');
			$('p.enter_pass').text('');
		} else {
			$('p.enter_mail').text('Please enter correct email');
			$("input#in_mail").css({"background" : "rgba(255, 147, 146, 0.3)", "border" : "2px solid rgb(255, 0, 0, 0.3)"});
			$('p.enter_pass').text('Please enter correct password');
			$("input#in_pass").css({"background" : "rgba(255, 147, 146, 0.3)", "border" : "2px solid rgb(255, 0, 0, 0.3)"});
			flag = false;
		}


		return flag;
	});
});