/* Author: James Cleveland
*/

$(function() {
    $("#twitter").tweet({
            username: [
                'BrightonFemCol',
            ],
            join_text: "auto",
            avatar_size: 50,
            count: 5,
            auto_join_text_default: "", 
            auto_join_text_ed: "we",
            auto_join_text_ing: "we were",
            auto_join_text_reply: "in reply to",
            auto_join_text_url: "",
            loading_text: "loading tweets..."
        });
});

$(function() {
    $('#main>div h1, #main>div h2, #main>div h3, #main>div h4, #main>div h5').each(function() {
        t = $(this);
        $('code', t).each(function(){
            var c = $(this);
            if(c.text() == '_') {
                c.replaceWith('_');
            }
        });

        t.html(t.html().replace(/_/g, '<code>_</code>'));
    });
});