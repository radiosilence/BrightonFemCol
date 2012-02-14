var makeLarge = function() {
    titleFields = $('div input, div select, div textarea, div buttom');
    titleFields.each(function() {
        t = $(this);
        w = t.parent().width();
        p = 10;
        t.width(w-p);
        console.log(p);
    })
}

var autoSlug = function() {
    if($('#slug').val() == '') {
        $('#slug').attr('auto', true);
    }
    $('#title').on('keyup', function() {
        title = $(this).val();
        if($('#slug').attr('auto') == 'true') {
            $('#slug').val(calculate_slug(title));   
        }
    });

    $('#slug').on('keyup', function() {
        $(this).attr('auto', false);
    });
}
$(function() {

    makeLarge();
    autoSlug();
})