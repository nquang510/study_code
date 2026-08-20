$(document).ready(function(){
	$('.ratings_stars').hover(
	    function() {
	        $(this).prevAll().andSelf().addClass('ratings_hover');
	    },
	    function() {
	        $(this).prevAll().andSelf().removeClass('ratings_hover');
	    }
	);

	$('.ratings_stars').click(function(){
		var Values =  $(this).find("input").val();
		if ($(this).hasClass('ratings_over')) {
		    $('.ratings_stars').removeClass('ratings_over');
		    $(this).prevAll().andSelf().addClass('ratings_over');
		} else {
		    $(this).prevAll().andSelf().addClass('ratings_over');
		}
	});
});