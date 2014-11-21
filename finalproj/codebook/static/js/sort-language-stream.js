/**
 * Created by nora on 11/21/2014.
 */

$(document).ready(function () {
    recent_sort();
});

$('#lang-recent').click(function () {
    recent_sort();
});

$('#lang-popular').click(function () {
    popular_sort();
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