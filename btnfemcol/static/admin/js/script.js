/* Author:

*/
var remove_flash = function(flash, duration) {
    if(duration == undefined) {
        duration = 500;
    };
    flash.stop(true, true).animate({left: '100%', 'margin-left': '20px'}, duration, function() {
        flash.remove();
        fade_first_flash();
    });
}

var fade_first_flash = function() {
    $('ul.flashes li:first-child').animate({display: 'block'}, 3000, function() {
        remove_flash($(this));
    });
}

$(function() {
    fade_first_flash();
    $('ul.flashes li').on('click', function() {
        remove_flash($(this), 200);
    })
});

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

// Advanced / Basic form hiding parts.
$(function() {
    $('fieldset.advanced').before('<a href="#" class="advanced_hider">Advanced +</a>');
    $('fieldset.advanced').hide();
    $('a.advanced_hider').on('click', function(event) {
        event.preventDefault();
        t = $(this);
        if($(this).attr('vis') == 'shown') {
            t.next().slideToggle();
            t.attr('vis', 'hidden');
            t.text('Advanced +');
        } else {
            t.next().slideToggle();
            t.attr('vis', 'shown');
            t.text('Advanced -');          
        }
    });
});