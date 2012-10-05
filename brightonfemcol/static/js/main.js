requirejs.config({
    shim: {
        'lib/jquery.fancybox': {
            deps: ['jquery'],
        },
    },
});
require(['jquery', 'lib/jquery.fancybox', 'lib/modernizr'], function($) {
    $('.fancybox').fancybox();
});