/**
 * Created by nora on 11/23/2014.
 */
function load_trees() {
    console.log("IN LOAD TRESS");
    var list = $(document.getElementsByClassName('rep-file-explorer'));
    var listCount = list.length;
    console.log(listCount);
    console.log($('.rep-file-explorer').length);
    // $('.rep-file-explorer').bind('ajaxComplete', load_tree());
    $('.rep-file-explorer').each(function (index, data) {
        console.log(index);
        var id = $(this).attr("data-item-id");
        console.log(id);
        var elem = $(this);
        load_tree(elem, id);
    });
}

function load_tree(elem, id) {
    console.log("IN LOAD TREE");
    elem.dynatree({
        fx: {height: "toggle", duration: 200},
        autoFocus: false,
        initAjax: {
            url: '/codebook/get_top_level',
            data: {
                repo_id: id
            },
            error: function (xhr, textStatus, errorThrown) {
                if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                    alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

                }
            }
        },
        onActivate: function (node) {
            console.log("ACTIVATE: " + node + " (" + node.getKeyPath() + ")");

            if (!node.data.isFolder) {
                var key = node.data.key;
                var parts = key.split('---');
                var repo_id = parts[0];
                var sha = parts[1];
                var path = parts[2];

                $.ajax({
                    type: "GET",
                    url: '/codebook/get_file_contents',
                    data: {
                        repo_id: repo_id,
                        sha: sha,
                        path: path
                    },
                    success: function (html) {
                        $('#file-content-' + repo_id).replaceWith(html);
                        prepair_repo_scroll();
                    }
                });
            }
        },
        onLazyRead: function (node) {
            console.log("LAZY READ: " + node + " (" + node.getKeyPath() + ")");
            var key = node.data.key;
            var parts = key.split('---');
            var repo_id = parts[0];
            var sha = parts[1];
            var path = parts[2];
            $.ajax({
                type: "GET",
                url: '/codebook/expand_folder',
                data: {
                    repo_id: repo_id,
                    sha: sha,
                    path: path
                },
                success: function (json) {
                    /*
                     //if (data.status == 'ok')
                     //{
                     var list = data.result;
                     for (var i = 0, l = list.length; i < l; i++) {
                     var e = list[i];
                     res.push({title: "" + i + ": " + e.fcurr + "-" + e.tcurr + ":" + e.ukurs,
                     icon: false});
                     }
                     node.setLazyNodeStatus(DTNodeStatus_Ok);
                     node.addChild(res);
                     console.log("LAZY READ: " + node + " (" + node.getKeyPath() + ")");
                     //}
                     /*
                     else {
                     // Server returned an error condition: set node status accordingly
                     node.setLazyNodeStatus(DTNodeStatus_Error, {
                     tooltip: data.faultDetails,
                     info: data.faultString
                     });
                     }*/
                    node.setLazyNodeStatus(DTNodeStatus_Ok);
                    node.addChild(json);
                }
            });
        }
    });
}
