/**
 * Created by nora on 11/19/2014.
 */
  $(function() {
    $( "#slider" ).slider({
      value:5,
      min: 0,
      max: 10,
      step: 1,
      slide: function( event, ui ) {
        $( "#amount" ).val( ui.value );
          //$("#amount").innerText().replaceWith("$" + ui.value);
      }
    });
    $( "#amount" ).val( $( "#slider" ).slider( "value" ) );
    //$( "#amount" ).innerText().replaceWith( "$" + $( "#slider" ).slider( "value" ) );
  });