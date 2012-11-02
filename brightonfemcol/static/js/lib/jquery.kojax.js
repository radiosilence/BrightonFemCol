(function( window, undefined ) {

var kojax = function($, History) {

    // Private
    function modifyHistory(data, context, options) {
        var state = {
          id: (new Date).getTime(),
          url: context.url,
          title: 'NOT A TITLE YET',
        };
        var History = window.History;
        if (!History.enabled) {
            return false;
        }
        History.pushState(state, state.title, state.url)
    }

    // Private
    function update(data, context, options) {
        modifyHistory(data, context, options);
    }

    // Private
    function handle(event) {
        var $this = $(this);
    }

    // Private
    function request(context, options, callback) {
        var o = {
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-KOJAX', 'true');
            },
            success: function(data, status, xhr) {
                callback(data, context, options);
            }
        }
        $.extend(o, options);
        $.ajax(context.url, o);
    }

    // Public
    function kojax(url, options) {
        var context = {
            url: url
        };
        request(context, options, update);
    }

    $.kojax = kojax;
    $.kojaxBind = function(selector, options) {
        var o = {
            event: 'click'
        };
        $.extend(o, options);
        $('body').on(o.event, selector, function(event) {
            event.preventDefault();
            var $this = $(this);
            kojax($this.attr('href'), o);
        });
    }
}

// Option AMD support.
if (typeof define === 'function' && define.amd) {
    define([ 'jquery'
           , 'history'
           , 'history.adapter.jquery'
           , 'history.html4'
           ], kojax);
} else if (
    typeof jQuery === 'function'
        && jQuery.fn.jquery
        && typeof History == 'function') {
    kojax(jQuery, History);
} else {
    console.log("Error: Dependencies not loaded.");
}

})( window );