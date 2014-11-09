/**
 * Created by nora on 11/8/2014.
 */
/*
$(".search_type_menu").on(function()
{
    $(".dropdown-menu").on('click', 'li a', function()
    {
      $(".btn:first-child").text($(this).text());
      $(".btn:first-child").val($(this).text());
   });

});
*/

$(".dropdown-menu li a").click(function(e){
    e.preventDefault();

  $(this).parents(".btn-group").find('.selection').text($(this).text());
  $(this).parents(".btn-group").find('.selection').val($(this).text());

});