/**
 * Created by nora on 11/15/2014.
 */
$(document).ready( function() {
    $('#contagfhgjhkjliner_id').fileTree({ root: '/some/folder/' }, function(file) {
        alert(file);
    });
});