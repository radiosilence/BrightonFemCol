requirejs.config({
    shim: {
        'libs/jquery': {
            exports: 'jQuery',
        },
        'libs/jquery.fancybox': {
            deps: ['libs/jquery'],
        },
    },
});
require(['libs/jquery', 'libs/jquery.fancybox', 'libs/modernizr'], function($) {
    $('.fancybox').fancybox();
});