$(document).ready(function () {

	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = cookies[i].trim();
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');

	function paintStars($wrap, value) {
		$wrap.find('.fa-star').each(function () {
			var starValue = parseInt($(this).attr('data-value'), 10);
			$(this).toggleClass('color', starValue <= value);
		});
	}

	// Tô màu các sao khi rê chuột vào
	$('.rate-stars').on('mouseenter', '.fa-star', function () {
		var hoverValue = parseInt($(this).attr('data-value'), 10);
		paintStars($(this).closest('.rate-stars'), hoverValue);
	});

	// khi rê chuột ra khỏi các sao, tô màu lại theo điểm trung bình
	$('.rate-stars').on('mouseleave', function () {
		var avg = parseInt($(this).attr('data-avg'), 10) || 0;
		paintStars($(this), avg);
	});

	// click vào sao để đánh giá
	$('.rate-stars').on('click', '.fa-star', function () {
		var $star = $(this);
		var $wrap = $star.closest('.rate-stars');

		if ($wrap.attr('data-user-rated') === '1') {
			alert('Bạn đã đánh giá bài viết này rồi.');
			return;
		}

		var blogId = $wrap.attr('data-blog-id');
		var rateValue = $star.attr('data-value');

		$.ajax({
			url: '/blog/' + blogId + '/rate/',
			type: 'POST',
			data: {
				rate: rateValue
			},
			headers: {
				'X-CSRFToken': csrftoken
			},
			success: function (res) {
				if (res.success) {
					$wrap.attr('data-avg', res.average_rating);
					$wrap.attr('data-user-rated', '1');
					paintStars($wrap, res.average_rating);
					$wrap.closest('.ratings').find('.rate-count').text('(' + res.rate_count + ' votes)');
				}
				alert(res.message);
			},
			error: function (xhr) {
				if (xhr.status === 403) {
					alert('Phiên đăng nhập đã hết hạn, vui lòng tải lại trang.');
				} else {
					alert('Có lỗi xảy ra, vui lòng thử lại.');
				}
			}
		});
	});

});
