/**
 * Created by nora on 11/16/2014.
 */
$(document).ready(function(){
    prepair_repo_scroll();
});

function prepair_repo_scroll()
{
    console.log("SCROLLLLLLLLLLLLLLLLLLLLLLLL");
    $('.file-content').slimScroll({
        height: '300px'
    });

    $('.rep-file-explorer').slimScroll({
        height: '300px'
    });

    $('.tab-content').slimScroll({
        height: '400px'
    });
}