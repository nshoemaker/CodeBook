/**
 * Created by nora on 11/20/2014.
 */

$('#add-proficiency-btn').click(function () {
    var language = $('#language-prof').val();
    var proficiency = $('#amount').val();
    console.log("lang: " + language + " proficiency: " + proficiency);
    if (language == "") {
        alert("Must select a language.");
    }
    else {
        $.ajax({
            type: "POST",
            url: "/codebook/add_proficiency",
            data: {
                language: language,
                proficiency: proficiency,
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success: function (html) {
                $('#proficiency-list').prepend(html);
                $('#language-choice').val('');
                $('#slider').value(5);
            },
            error: function (xhr, textStatus, errorThrown) {
                console.log("made it to repo comment function FAIL");
                if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                    alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

                }
            }
        });
    }
});