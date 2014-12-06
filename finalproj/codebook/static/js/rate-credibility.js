/**
 * Created by nora on 11/16/2014.
 */

$(document).ready(function () {
    var currentURL = document.URL;
    if (currentURL.indexOf("profile" > -1))
    {
        rate_credibility();
    }
    else {
        $("#edit_my_profile_tab").click(function () {
            rate_credibility();
        });
    }
});

function rate_credibility() {
        $.ajax({
            type: "POST",
            url: "/codebook/rate_credibility",
            datatype: 'html',
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success: function () {
            },
            error: function (xhr, textStatus, errorThrown) {
                if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                    alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

                }
            }
        });

}