/* Author: James Cleveland
*/

$(function() {
    $('.main-column').equalHeights();
    $("#twitter").tweet({
            username: "ntihero",
            join_text: "auto",
            avatar_size: 50,
            count: 5,
            auto_join_text_default: "we said,", 
            auto_join_text_ed: "we",
            auto_join_text_ing: "we were",
            auto_join_text_reply: "we replied to",
            auto_join_text_url: "we were checking out",
            loading_text: "loading tweets..."
        });
});
