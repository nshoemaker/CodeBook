$(document).ready(function () {
    prepair_repo_toggle_buttons();
});

function prepair_repo_toggle_buttons() {
    $(".repo-toggle-button").click(function () {
        var repo_id = $(this).attr("data-item-id");
        toggle_repository_view(repo_id);
    });
    $("#collapse-all").click(function () {
        $(".repo-body").slideUp();
        $(".repo-toggle-button").removeClass("glyphicon-collapse-down");
        $(".repo-toggle-button").addClass("glyphicon-expand");
    });
}

function toggle_repository_view(repo_id) {
    if ($("#repo-toggle-button-" + repo_id).hasClass("glyphicon-expand")) {
        $("#repo-toggle-button-" + repo_id).removeClass("glyphicon-expand");
        $("#repo-toggle-button-" + repo_id).addClass("glyphicon-collapse-down");

    }
    else if ($("#repo-toggle-button-" + repo_id).hasClass("glyphicon-collapse-down")) {
        $("#repo-toggle-button-" + repo_id).removeClass("glyphicon-collapse-down");
        $("#repo-toggle-button-" + repo_id).addClass("glyphicon-expand");
    }

    $("#repo-body-" + repo_id).slideToggle();
}