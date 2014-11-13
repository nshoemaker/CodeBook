
/**
 * Created by nora on 11/13/2014.
 */

$('.post-repo-comment-form').on('submit', function (e) {
    e.preventDefault();
    var repo_id = $(this).attr("data-item-id");
    create_repo_comment_post(repo_id);
});

function create_repo_comment_post(repo_id) {
    $.ajax({
        type: "POST",
        url: "/codebook/comment_repo/" + repo_id,
        datatype: "html",
        data: {
            repo_id: repo_id,
            text: $('#repo-post-text-' + repo_id).val(),
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function (html){
            $('#repo-comment-list-' + repo_id).append(html);
            $('#repo-post-text-' + repo_id).val('');
        },
        error: function (xhr, textStatus, errorThrown) {
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
        }
    });
}

$('.post-file-comment-form').on('submit', function (e) {
    e.preventDefault();
    var file_id = $(this).attr("data-item-id");
    create_file_comment_post(file_id);
});

function create_file_comment_post(file_id) {
    $.ajax({
        type: "POST",
        url: "/codebook/comment_file/" + file_id,
        datatype: "html",
        data: {
            repo_id: file_id,
            text: $('#file-post-text-' + file_id).val(),
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function (html){
            $('#file-comment-list-' + file_id).append(html);
            $('#file-post-text-' + file_id).val('');
        },
        error: function (xhr, textStatus, errorThrown) {
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
        }
    });
}