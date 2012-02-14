var makeLarge = function() {
    titleFields = $('input', $('.title'));
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