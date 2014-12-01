/**
 * Created by nora on 11/24/2014.
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
    get_watchers();
});


$(document).ajaxComplete(function()
{
    console.log("ajax complete");
                        $('pre code').each(function (i, block) {
                            hljs.highlightBlock(block);
                        });
});

function get_watchers() {
    var target = document.getElementById('base-stream');
    var spinner = new Spinner().spin(target);

    $.ajax({
        type: "GET",
        url: "/codebook/watch_list",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function (html) {
            spinner.stop();
            $("#repo-list").replaceWith(html);
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