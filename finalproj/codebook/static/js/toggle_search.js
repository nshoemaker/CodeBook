$(document).ready(function()
{
    //$(".repo-body").slideUp();
$(".repo-toggle-button").click(function()
{
    var repo_id = $(this).attr("data-item-id");
    toggle_repository_view(repo_id);
});
});


function toggle_repository_view(repo_id)
{
    if ($("#repo-toggle-button-" + repo_id).hasClass("glyphicon-expand"))
    {
        $("#repo-toggle-button-" + repo_id).removeClass("glyphicon-expand");
        $("#repo-toggle-button-" + repo_id).addClass("glyphicon-collapse-down");

    }
    else if ($("#repo-toggle-button-" + repo_id).hasClass("glyphicon-collapse-down"))
    {
        $("#repo-toggle-button-" + repo_id).removeClass("glyphicon-collapse-down");
        $("#repo-toggle-button-" + repo_id).addClass("glyphicon-expand");
    }

    $("#repo-body-" + repo_id).slideToggle();
}