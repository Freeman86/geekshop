window.onload = function () {
//    alert(); НИКОГДА для отладки!
    console.log('DOM loaded');
    $('.basket_list').on('change', 'input[type="number"]', function (event) {
//        console.log('event target:', event.target);
//        console.log('product pk', event.target.name);
//        console.log('product quantity', event.target.value);
        $.ajax({
            url: "/basket/edit/" + event.target.name + "/" + event.target.value + "/ajax/",

            success: function (data) {
                $('.basket_list').html(data.result);
            },
        });

//        event.preventDefault();
    });
}