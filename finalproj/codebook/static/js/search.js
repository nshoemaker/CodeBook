/**
 * Created by nora on 11/8/2014.
 */

$(".dropdown-menu li a").click(function(e){
    e.preventDefault();

  $(this).parents(".btn-group").find('.selection').text($(this).text());
  $(this).parents(".btn-group").find('.selection').val($(this).text());

});