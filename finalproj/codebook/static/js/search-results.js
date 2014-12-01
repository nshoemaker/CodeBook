/**
 * Created by nora on 11/22/2014.
 */

function prepair_results()
{
    prepair_file_save();
    prepair_repo_scroll();
    prepair_repo_star();
    prepair_repo_toggle_buttons();
    prepair_repo_watch();
    prepair_comments();
}

$(document).ready(function() {
   search_results();
});

$(document).ajaxComplete(function()
{
    console.log("ajax complete");
                        $('pre code').each(function (i, block) {
                            hljs.highlightBlock(block);
                        });
    //prepair_results();
    //load_trees();
});

function search_results() {
    var target = document.getElementById('base-stream');
    var spinner = new Spinner().spin(target);

    var currentURL = document.URL;
    var parts = currentURL.split("/");
    if (parts[4] == "search") {
        console.log(parts);
        var newURL = "/codebook/repo_search_list";
        var text = parts[5];
        var types = "Lang";
    }
    else{
        var newURL = "/codebook/repo_search_list";
        var form_fields = currentURL.split("?")[1];
        var fields = form_fields.split("&");
        var text = fields[0].split("=")[1];
        var types = fields[1].split("=")[1];

    }
    console.log(newURL);
    console.log(text);
    console.log(types);

    $.ajax({
        type: "GET",
        url: newURL,
        datatype: 'html',
        data:{
            text: text,
            types: types,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function(html) {
            console.log("success");
            spinner.stop();
            console.log("4");
            $("#repository-list-container").replaceWith(html);
            console.log("5");
            prepair_results();
            load_trees();
        },
        error: function (xhr, textStatus, errorThrown) {
            spinner.stop();
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
        }
    });
}