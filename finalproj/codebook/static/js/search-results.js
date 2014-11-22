/**
 * Created by nora on 11/22/2014.
 */

function prepair_results()
{
    prepair_file_save();
    prepair_like_comment();
    prepair_repo_scroll();
    prepair_repo_star();
    prepair_repo_toggle_buttons();
    prepair_repo_watch();
}

$(document).ready(function() {
   search_results();
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
            spinner.stop();
            $("#repo-list").replaceWith(html);
            prepair_results();
        },
        error: function (xhr, textStatus, errorThrown) {
            spinner.stop();
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
        }
    });
}