requirejs.config({
});
require(['jquery', 'lib/jquery.murderbox', 'lib/modernizr'], function($) {
    $('ul.gallery a').murderbox({});
});