/**
 * Created by nora on 11/21/2014.
 */
$('#lang-recent').click(function () {
            $("#lang-recent").css('background-color', '#77DDAA');
            $("#lang-popular").css('background-color', '#FFFFFF');
    $.ajax({
        type: "GET",
        url: "/codebook/sort_lang_stream_recent",
        data: {},
        success: function (html) {
            $("#repo-list").replaceWith(html);
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log("made it to repo comment function FAIL");
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
        }
    });
});

$('#lang-popular').click(function () {
            $("#lang-popular").css('background-color', '#77DDAA');
            $("#lang-recent").css('background-color', '#FFFFFF');
    $.ajax({
        type: "GET",
        url: "/codebook/sort_lang_stream_popular",
        data: {},
        success: function (html) {
            $("#repo-list").replaceWith(html);
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log("made it to repo comment function FAIL");
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
        }
    });
});