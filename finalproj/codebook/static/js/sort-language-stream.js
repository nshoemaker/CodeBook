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
    var $active = $('.lang-icon').first();
    $active.addClass("active-lang");
    var language = $active.attr("data-item-id");
    console.log("ACTIVE LANGUAGE: ");
    console.log(language);
    recent_sort(language);
});

$('#lang-recent').click(function () {
    var $active = $('.active-lang').first();
    var language = $active.attr("data-item-id");
    recent_sort(language);
});

$('#lang-popular').click(function () {
    var $active = $('.active-lang').first();
    var language = $active.attr("data-item-id");
    popular_sort(language);
});

$('.lang-icon').click(function () {
    var $this = $(this);
    if (!$this.hasClass("active-lang")) {
        $('.lang-icon').each(function() {
            $(this).removeClass("active-lang");
        });
        $this.addClass("active-lang");
        var language = $this.attr("data-item-id");

        if ($('#lang-recent').hasClass("active-lang-filter")) {
            recent_sort(language);
        }
        else if ($('#lang-popular').hasClass("active-lang-filter")) {
            popular_sort(language);
        }
    }
});

$(document).ajaxComplete(function()
{
    console.log("ajax complete");
                        $('pre code').each(function (i, block) {
                            hljs.highlightBlock(block);
                        });
});

function recent_sort(language) {
    var target = document.getElementById('base-stream');
    var spinner = new Spinner().spin(target);

    var $recent = $("#lang-recent");
    $recent.css('background-color', '#77DDAA');
    var $popular = $("#lang-popular");
    $popular.css('background-color', '#FFFFFF');

    if ($popular.hasClass("active-lang-filter"))
    {
        $popular.removeClass("active-lang-filter");
    }
    if (!$recent.hasClass("active-lang-filter"))
    {
        $recent.addClass("active-lang-filter");
    }

    $.ajax({
        type: "GET",
        url: "/codebook/sort_lang_stream_recent",
        data: {
            language: language
        },
        success: function (html) {
            spinner.stop();
            $("#repository-list-container").replaceWith(html);
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

function popular_sort(language) {
    var target = document.getElementById('base-stream');
    var spinner = new Spinner().spin(target);

    var $popular = $("#lang-popular");
    $popular.css('background-color', '#77DDAA');
    var $recent = $("#lang-recent");
    $recent.css('background-color', '#FFFFFF');

    if ($recent.hasClass("active-lang-filter"))
    {
        $recent.removeClass("active-lang-filter");
    }
    if (!$popular.hasClass("active-lang-filter"))
    {
        $popular.addClass("active-lang-filter");
    }

    $.ajax({
        type: "GET",
        url: "/codebook/sort_lang_stream_popular",
        data: {
            language: language
        },
        success: function (html) {
            spinner.stop();
            $("#repository-list-container").replaceWith(html);
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