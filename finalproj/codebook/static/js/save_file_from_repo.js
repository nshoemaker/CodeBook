/**
 * Created by nora on 11/25/2014.
 */
$("#base-stream").on("click", ".current-file-save", function() {
    var repo_id = $(this).attr("data-item-id");
    var $obj = $('#current-file-' + repo_id);
    var file_path = $obj.attr("data-item-id");
    console.log("repo_id" + repo_id);
    console.log($obj);
    console.log("file_path " + file_path);

    $('#saved-notification-' + repo_id).text($(this).data('text')).fadeIn(400).delay(2000).fadeOut(400);

    $.ajax({
        type: "POST",
        url: "/codebook/save_file_from_repo",
        datatype: 'html',
        data: {
            repo_id: repo_id,
            file_path: file_path,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function() {
            console.log("successful file save");
        },
        error: function (xhr, textStatus, errorThrown) {
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
        }
    });
});