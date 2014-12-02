/**
 * Created by nora on 11/21/2014.
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


$(document).ready(function () {
    recent_sort();
});

$('#lang-recent').click(function () {
    recent_sort();
});

$('#lang-popular').click(function () {
    popular_sort();
});


$(document).ajaxComplete(function()
{
    console.log("ajax complete");
                        $('pre code').each(function (i, block) {
                            hljs.highlightBlock(block);
                        });
});

function recent_sort() {
    var target = document.getElementById('base-stream');
    var spinner = new Spinner().spin(target);
    $("#lang-recent").css('background-color', '#77DDAA');
    $("#lang-popular").css('background-color', '#FFFFFF');
    $.ajax({
        type: "GET",
        url: "/codebook/sort_lang_stream_recent",
        data: {},
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

function popular_sort() {
    var target = document.getElementById('base-stream');
    var spinner = new Spinner().spin(target);
    $("#lang-popular").css('background-color', '#77DDAA');
    $("#lang-recent").css('background-color', '#FFFFFF');
    $.ajax({
        type: "GET",
        url: "/codebook/sort_lang_stream_popular",
        data: {},
        success: function (html) {
            spinner.stop();
            $("#repo-list").replaceWith(html);
            prepair_results();
            load_trees();
        },
        error: function (xhr, textStatus, errorThrown) {
            spinner.stop();
            console.log("made it to repo comment function FAIL");
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
        }
    });

}