/**
 * Created by nora on 11/13/2014.
 */

$(document).ready(function()
{
});

    $('#base-stream').on('click', '.like-status', function()
    {
        var comment_id = $(this).attr("data-item-id");

        if ($(this).hasClass("glyphicon-ok"))
        {
            like_comment(comment_id);
        }
        else if ($(this).hasClass("glyphicon-remove"))
        {
            unlike_comment(comment_id);
        }
    });
function like_comment(comment_id)
{
    $.ajax({
        type: "POST",
        url: "/codebook/like_comment/" + comment_id,
        datatype: 'html',
        data: {
            comment_id: comment_id,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function() {
            var eye = $("#like-status-" + comment_id);
            if (eye.hasClass("glyphicon-ok"))
            {
                eye.removeClass("glyphicon-ok");
            }
            if (!eye.hasClass("glyphicon-remove"))
            {
                eye.addClass("glyphicon-remove");
            }
            eye.attr("title", "Unlike comment" );
        },
        error: function (xhr, textStatus, errorThrown) {
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
        }
    });
}


function unlike_comment(comment_id)
{
    $.ajax({
        type: "POST",
        url: "/codebook/unlike_comment/" + comment_id,
        datatype: 'html',
        data: {
            comment_id: comment_id,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function() {
            var eye = $("#like-status-" + comment_id);
            if (!eye.hasClass("glyphicon-ok"))
            {
                eye.addClass("glyphicon-ok");
            }
            if (eye.hasClass("glyphicon-remove"))
            {
                eye.removeClass("glyphicon-remove");
            }
            eye.attr("title", "Like comment" );
        },
        error: function (xhr, textStatus, errorThrown) {
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
        }
    });
}