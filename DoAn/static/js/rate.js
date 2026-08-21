$(document).ready(function () {
    const csrftoken = $('[name=csrfmiddlewaretoken]').val();

    // hover sao khi rê chuột
    $('.fa-star').hover(function () {
        const hoverValue = $(this).data('value');
        $('.fa-star').each(function () {
            $(this).toggleClass('color', $(this).data('value') <= hoverValue);
        });
    });


    // click sao
    $('.fa-star').click(function () {

        const rate = $(this).data('value');
        const $wrap = $(this).closest('.rate-stars');
        const blogId = $wrap.data('blog-id');

        $.ajax({
            type: 'POST',
            url: '/blog/' + blogId + '/rate/',
            data: { rate: rate },
            headers: { 'X-CSRFToken': csrftoken },
            success: function (data) {

                if (data.success) {
					//cập nhật rate-count
                    $('.rate-count').text('(' + data.rate_count + ' votes)');
					//cập nhật lại điểm trung bình
                    $wrap.data('avg', data.average_rating);

                    $('.fa-star').each(function () {
                        $(this).toggleClass('color', $(this).data('value') <= Math.round(data.average_rating));
                    });
                }

                alert(data.message);
            }
        });

    });

});
