define(['jquery', 'lib/jquery.transit'], function ($) {
    $.fn.murderbox = function(options) {
        var close_all = function() {
            $shade.transition({
                opacity: 0,
            }, 500, function() {
                $shade.hide();
            });
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
                return {
                    width: width,
                    height: width / img.aspect,
                }
            } else {
                // Image is taller
                var height = max.height - (o.padding * 2);
                return {
                    width: height * img.aspect,
                    height: height,
                }
            }
        }
        var display = function(image) {
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
            $img.on('load', function(event) {
                var size = optimal_size($img);
                $img.css({
                    width: size.width,
                    height: size.height,
                    'margin-left': -(size.width / 2),
                    'margin-top': -(size.height / 2),
                });
                $shade.html($div);
                $shade.show().transition({
                    opacity: 1,
                }, 500);
            });
        }
        var display_next = function() {
            // TODO
        }
        var display_previous = function() {
            // TODO
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
        $shade.on('click', close_all);
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

});