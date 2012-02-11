/* Author: James Cleveland
*/

$(function() {
    $("#twitter").tweet({
            username: [
                "littlespy",
                'BrightonFemCol',
                'ntihero',
                'MrsEmBH',
                'waywardtapper',
                'squeamishbikini',
                'frau_bh',
            ],
            join_text: "auto",
            avatar_size: 50,
            count: 10,
            auto_join_text_default: "", 
            auto_join_text_ed: "we",
            auto_join_text_ing: "we were",
            auto_join_text_reply: "in reply to",
            auto_join_text_url: "we were checking out",
            loading_text: "loading tweets..."
        });
});
