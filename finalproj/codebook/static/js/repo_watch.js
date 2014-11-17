/**
 * Created by nora on 11/13/2014.
 */

$(document).ready(function()
{
    $(".watch-status").click(function()
    {
        var repo_id = $(this).attr("data-item-id");

        if ($(this).hasClass("glyphicon-eye-open"))
        {
            watch_repository(repo_id);
        }
        else if ($(this).hasClass("glyphicon-eye-close"))
        {
            unwatch_repository(repo_id);
        }
    });
});

function watch_repository(repo_id)
{
    $.ajax({
        type: "POST",
        url: "/codebook/watch_repo/" + repo_id,
        datatype: 'html',
        data: {
            repo_id: repo_id,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function() {
            var eye = $("#watch-status-" + repo_id);
            if (eye.hasClass("glyphicon-eye-open"))
            {
                eye.removeClass("glyphicon-eye-open");
            }
            if (!eye.hasClass("glyphicon-eye-close"))
            {
                eye.addClass("glyphicon-eye-close");
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
        }
    });
}


function unwatch_repository(repo_id)
{
    $.ajax({
        type: "POST",
        url: "/codebook/unwatch_repo/" + repo_id,
        datatype: 'html',
        data: {
            repo_id: repo_id,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function() {
            var eye = $("#watch-status-" + repo_id);
            if (!eye.hasClass("glyphicon-eye-open"))
            {
                eye.addClass("glyphicon-eye-open");
            }
            if (eye.hasClass("glyphicon-eye-close"))
            {
                eye.removeClass("glyphicon-eye-close");
            }

            if ($("#watching").length)
            {
                $("#repo-list").remove($("#repo" + repo_id));
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
        }
    });
}