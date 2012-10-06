requirejs.config({
    paths: {
        jquery: 'lib/jquery',
        'jquery.fancybox': 'lib/jquery.fancybox',
        modernizr: 'lib/modernizr',
    },
    shim: {
        'jquery.fancybox': {
            deps: ['jquery'],
        },
    },
});
require(['jquery', 'jquery.fancybox', 'modernizr'], function($) {
    $('.fancybox').fancybox();
});