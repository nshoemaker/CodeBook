/**
 * Created by nora on 11/13/2014.
 */

$(document).ready(function () {
    prepair_repo_star();
});

function prepair_repo_star()
{
    $(".star-status").click(function () {
        var repo_id = $(this).attr("data-item-id");

        if ($(this).hasClass("glyphicon-star-empty")) {
            star_repository(repo_id);
        }
        else if ($(this).hasClass("glyphicon-star")) {
            unstar_repository(repo_id);
        }
    });
}

function star_repository(repo_id) {
    var star = $("#star-status-" + repo_id);
    if (star.hasClass("glyphicon-star-empty")) {
        star.removeClass("glyphicon-star-empty");
    }
    if (!star.hasClass("glyphicon-star")) {
        star.addClass("glyphicon-star");
    }
    $.ajax({
        type: "POST",
        url: "/codebook/star_repo/" + repo_id,
        datatype: 'html',
        data: {
            repo_id: repo_id,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function () {
            console.log("successful star");
        },
        error: function (xhr, textStatus, errorThrown) {
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
            var star = $("#star-status-" + repo_id);
            if (!star.hasClass("glyphicon-star-empty")) {
                star.addClass("glyphicon-star-empty");
            }
            if (star.hasClass("glyphicon-star")) {
                star.removeClass("glyphicon-star");
            }
        }
    });
}


function unstar_repository(repo_id) {
    var star = $("#star-status-" + repo_id);
    if (!star.hasClass("glyphicon-star-empty")) {
        star.addClass("glyphicon-star-empty");
    }
    if (star.hasClass("glyphicon-star")) {
        star.removeClass("glyphicon-star");
    }
    $.ajax({
        type: "POST",
        url: "/codebook/unstar_repo/" + repo_id,
        datatype: 'html',
        data: {
            repo_id: repo_id,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function () {
            console.log("successful unstar");
        },
        error: function (xhr, textStatus, errorThrown) {
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
            var star = $("#star-status-" + repo_id);
            if (star.hasClass("glyphicon-star-empty")) {
                star.removeClass("glyphicon-star-empty");
            }
            if (!star.hasClass("glyphicon-star")) {
                star.addClass("glyphicon-star");
            }
        }
    });
}