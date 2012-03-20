/* Author: James Cleveland
*/
var add_www = function() {
    if(window.domain_name !== window.location.host) {
        proper_url = window.location.protocol + '//' + window.domain_name + window.location.pathname;
        //window.location = proper_url;
    }
}
add_www();
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