/**
 * Created by nora on 11/16/2014.
 */
$(document).ready(function(){
    prepair_repo_scroll();
});

function prepair_repo_scroll()
{
    $('.file-content').slimScroll({
        height: '250px'
    });
    $('.tab-content').slimScroll({
        height: '400px'
    });
}