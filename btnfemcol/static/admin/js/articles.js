var populate_table = function(url, selector, status, page, filter) {
    /**
     * Populate a table with articles.
     */
//    console.log(url, selector, "status:", status, "PAGE:", page, "filter:", filter);
    var table = $(selector);
    if(status == undefined) {
        status = 'any';
    }
    if(page == undefined) {
        page = 1;
    }
    var d = {
        page: page,
        status: status
    };
    if(filter != undefined) {
        d['filter'] = filter;
    }
    $('tr', table).each(function() {
        tr = $(this);
        if(!tr.hasClass('header')) {
            tr.remove();
        }
    });
    console.log(url, d);
    $.getJSON(url, d, function(data) {
        console.log(url, d);
        for(a in data['articles']) {
            a = data['articles'][a];
            tr = ich.article_row(a);
            table.append(tr);
//            console.log("ADDING,", table.parent(), tr)
        }
    }); 
}