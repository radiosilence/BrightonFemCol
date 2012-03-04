var remove_flash = function(flash, duration) {
    /**
     * Hide a flash.
     */
    if(duration == undefined) {
        duration = 500;
    };
    flash.stop(true, true).animate({left: '100%', 'margin-left': '20px'}, duration, function() {
        flash.remove();
        fade_first_flash();
    });
}

var fade_first_flash = function() {
    /**
     * Hide the first flash then call the next one.
     */
    $('ul.flashes li:first-child').animate({display: 'block'}, 3000, function() {
        remove_flash($(this));
    });
}

var string_to_slug = function(str) {
  str = str.replace(/^\s+|\s+$/g, ''); // trim
  str = str.toLowerCase();
  
  // remove accents, swap ñ for n, etc
  var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
  var to   = "aaaaeeeeiiiioooouuuunc------";
  for (var i=0, l=from.length ; i<l ; i++) {
    str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
  }

  str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
    .replace(/\s+/g, '-') // collapse whitespace and replace by -
    .replace(/-+/g, '-'); // collapse dashes

  return str;
}

var populate_table = function(url, selector, status, page, filter) {
    /**
     * Populate a table with articles.
     */
//    console.log(url, selector, "status:", status, "PAGE:", page, "filter:", filter);
    var table = $(selector);
    if(status == undefined) {
        status = 'any';
    }
    if(page == undefined) {
        page = 1;
    }
    var d = {
        page: page,
        status: status
    };
    if(filter != undefined) {
        d['filter'] = filter;
    }
    $('tr', table).each(function() {
        tr = $(this);
        if(!tr.hasClass('header')) {
            tr.remove();
        }
    });
    $.getJSON(url, d, function(data) {
        for(a in data['items']) {
            a = data['items'][a];
            tr = ich.table_row(a);
            table.append(tr);
//            console.log("ADDING,", table.parent(), tr)
        }
    }); 
}
$(function() {
    // Slug autogeneration
    if($('input#slug').val() == '') {
        $('input#slug').attr('auto', 'auto');
    }
    $('input#title').on('keyup', function() {
        if($('input#slug').attr('auto') == 'auto') {
            $('input#slug').val(string_to_slug($(this).val()));
        };
    });

    $('input#slug').on('change', function() {
        $('input#slug').attr('auto', 'no');
    });
});

$(function() {
    // Slowly disappear the flashes
    fade_first_flash();
    $('ul.flashes li').on('click', function() {
        remove_flash($(this), 200);
    })
});

$(function() {
    // Full row selection
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


$(function() {
    // Advanced / Basic form hiding parts.
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