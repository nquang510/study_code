$(document).ready(function(){
	$('li.popular').click(function(){
		$('div.category').hide();
		$('div.one').show();
	})
	$('li.new-arrivals').click(function(){
		$('div.category').hide();
		$('div.two').show();
	})
	$('li.best-seller').click(function(){
		$('div.category').hide();
		$('div.one').show();
	})
	$('li.offer').click(function(){
		$('div.category').hide();
		$('div.two').show();
	})
	$('li.coming').click(function(){
		$('div.category').hide();
		$('div.one').show();
	})
	$('ul.menu-content li a').click(function(){
		$('ul.menu-content li a').css('color' , '#333333');
		$(this).css('color' , '#00c8c8');
	})
})