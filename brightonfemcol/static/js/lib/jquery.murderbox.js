(function( window, undefined ) {

var murderbox = function ($, Mousetrap) {
    $.fn.murderbox = function(options) {
        var active = false;
        var close_all = function() {
            $shade.animate({
                opacity: 0,
            }, 500, function() {
                $shade.hide();
            });
            Mousetrap.unbind('left');
            Mousetrap.unbind('right');
        }
        var optimal_size = function($img) {
            var img = $img.get(0);
            var max = {
                width: $(window).width(),
                height: $(window).height(),
            }
            max.aspect = max.width / max.height;
            img.aspect = img.width / img.height;
            if (img.aspect == max.aspect) {
                // Easy, they're the same dimensions (unlikely)
                return {
                    width: max.width - (o.padding * 2),
                    height: max.height - (o.padding * 2),
                }
            } else if (img.aspect > max.aspect) {
                // Image is wider
                var width = max.width - (o.padding * 2);
                if (img.width < width) {
                    return {
                        width: img.width,
                        height: img.height
                    }
                }
                return {
                    width: width,
                    height: width / img.aspect,
                }
            } else {
                // Image is taller
                var height = max.height - (o.padding * 2);
                if (img.height < width) {
                    return {
                        width: img.width,
                        height: img.height,
                    }
                }
                return {
                    width: height * img.aspect,
                    height: height,
                }
            }
        }
        var display = function(image) {
            active = image;
            var $img = $('<img/>', {
                src: image.src,
                css: {
                    position: 'fixed',
                    left: '50%',
                    top: '50%',
                }
            });
            var $div = $('<div/>', {
                class: 'murderbox image-box',
                html: $img,
            });
            if (group.length > 1) {
                var $prev = $('<a/>', {
                    class: 'murderbox prev',
                    href: 'javascript:void(0)',
                });
                $prev.on('click', function(event) {
                    event.preventDefault();
                    event.stopPropagation()
                    display_prev();
                });
                $div.append($prev);
                var $next = $('<a/>', {
                    class: 'murderbox next',
                    href: 'javascript:void(0)',
                });
                $next.on('click', function(event) {
                    event.preventDefault();
                    event.stopPropagation()
                    display_next();
                });
                $div.append($next);
            }

            $img.on('load', function(event) {
                var size = optimal_size($img);
                $img.css({
                    width: size.width,
                    height: size.height,
                    'margin-left': -(size.width / 2),
                    'margin-top': -(size.height / 2),
                });
                $shade.html($div);
                $shade.show().animate({
                    opacity: 1,
                }, 1000);
            });

            Mousetrap.bind('left', display_next);
            Mousetrap.bind('right', display_prev);
        }
        var display_next = function() {
            if (!active) {
                return false;
            }
            display(active.next());
        }
        var display_prev = function() {
            if (!active) {
                return false;
            }
            display(active.prev());
        }
        var image = function(e, g, i) {
            var $e = $(e);
            var src = $e.attr('href');
            $e.on('click', function(event) {
                event.preventDefault();
                display(g[i]);
            });
            return {
                i: i,
                $e: $e,
                src: src,
                next: function() {
                    if (i == g.length - 1) {
                       if (o.cycle) {
                            return g[0];
                       } else {
                            return false;
                       }
                    } else {
                        return g[i + 1];
                    }
                },
                prev: function() {
                    if (i == 0) {
                        if (o.cycle) {
                            return g[g.length - 1];
                        } else {
                            return false;
                        }
                    } else {
                        return g[i - 1];
                    }
                },
                me: function() {
                    return g[i]
                },
            }
        }
        var $this = $(this);
        var group = [];
        var $shade = $('<div/>', {
            class: 'murderbox shade',
            css: {
                display: 'none',
            }
        })
        $shade.on('click', function(event) {
            event.preventDefault();
            var $this = $(this);
            if (!$this.is('a')) {
                close_all();
            }
        });
        $('body').append($shade);

        var o = {
            cycle: true,
            padding: 10,
        };
        $.extend(o, options);
        $this.each(function() {
            group.push(image(this, group, group.length));
        });
    };

};

if (typeof define === 'function' && define.amd) {
    define(['jquery', 'mousetrap'], murderbox);
} else if (
    typeof jQuery === 'function'
        && jQuery.fn.jquery
        && typeof Mousetrap == 'function') {
    murderbox(jQuery, Mousetrap);
} else {
    console.log("Error: Could not find jQuery.");
}

})( window );