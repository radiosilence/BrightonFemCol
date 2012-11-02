requirejs.config({
    shim: {
        'history': {
            exports: 'History',
        },
        'history.html4': {
            deps: ['history']
        },
        'history.adapter.jquery': {
            deps: ['history']
        },
    },
});
require([ 'jquery'
        , 'lib/jquery.murderbox'
        , 'lib/modernizr'
        , 'lib/jquery.kojax'
        ], function($) {
    $('ul.gallery a').murderbox({});
    $.kojaxBind('nav a');
});