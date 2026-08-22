$(document).ready(function () {
    const csrftoken = $('[name=csrfmiddlewaretoken]').val();
    const $wrap = $('.rate');
    const blogId = $wrap.data('blog-id');

    // hover sao khi rê chuột
    $('.ratings_stars').hover(
        function () {
            $(this).prevAll('.ratings_stars').addBack().addClass('ratings_hover');
        },
        function () {
            $(this).prevAll('.ratings_stars').addBack().removeClass('ratings_hover');
        }
    );

    // click sao
    $('.ratings_stars').click(function () {
        const rate = $(this).find('input').val();

        if ($(this).hasClass('ratings_over')) {
		            $('.ratings_stars').removeClass('ratings_over');
		            $(this).prevAll().andSelf().addClass('ratings_over');
		        } else {
		        	$(this).prevAll().andSelf().addClass('ratings_over');
		        }

        $.ajax({
            type: 'POST',
            url: '/blog/' + blogId + '/rate/',
            data: { rate: rate },
            headers: { 'X-CSRFToken': csrftoken },
            success: function (data) {

                if (data.success) {
                    // cập nhật rate-count
                    $('.rate-count').text('(' + data.rate_count + ' votes)');
                    // cập nhật lại điểm trung bình
                    $wrap.data('avg', data.average_rating);

                    
                }

                alert(data.message);
            }
        });
    });
});
