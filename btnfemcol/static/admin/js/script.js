/* Author:

*/
$(function() {
    $('table tr').on('click', function() {
        if($(this).hasClass('selected')) {
            $(this).removeClass('selected')
        } else if(!$(this).hasClass('header')) {
            $(this).addClass('selected');
        }
    });

    $('h2').on('click', function() {
        $(this).animate({
            height: '200px'
        });
    })
});




