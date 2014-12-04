/**
 * Created by nora on 11/13/2014.
 */

$(document).ready(function()
{
    prepair_file_save();
});

function prepair_file_save()
{
    $(".save-status").click(function()
    {
        var file_id = $(this).attr("data-item-id");

        if ($(this).hasClass("glyphicon-floppy-disk"))
        {
            save_file(file_id);
        }
        else if ($(this).hasClass("glyphicon-floppy-saved"))
        {
            unsave_file(file_id);
        }
    });
}

function save_file(file_id)
{
    $.ajax({
        type: "POST",
        url: "/codebook/save_file/" + file_id,
        datatype: 'html',
        data: {
            repo_id: file_id,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function() {
            var eye = $("#save-status-" + file_id);
            if (eye.hasClass("glyphicon-floppy-disk"))
            {
                eye.removeClass("glyphicon-floppy-disk");
            }
            if (!eye.hasClass("glyphicon-floppy-saved"))
            {
                eye.addClass("glyphicon-floppy-saved");
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
        }
    });
}


function unsave_file(file_id)
{
            var eye = $("#save-status-" + file_id);
            if (!eye.hasClass("glyphicon-floppy-disk"))
            {
                eye.addClass("glyphicon-floppy-disk");
            }
            if (eye.hasClass("glyphicon-floppy-saved"))
            {
                eye.removeClass("glyphicon-floppy-saved");
            }

            if (window.location.href.indexOf("codebook/saved") > -1) {
                if ($("#file" + file_id)) {
                    $("#file" + file_id).remove()
                }
            }

    $.ajax({
        type: "POST",
        url: "/codebook/unsave_file/" + file_id,
        datatype: 'html',
        data: {
            repo_id: file_id,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function() {
        },
        error: function (xhr, textStatus, errorThrown) {
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
        }
    });
}