$("#country").change(function () {
    var url = $("#search").attr("data-cities-url");  // get the url of the `load_cities` view
    var countryId = $(country).val();  // get the selected country ID from the HTML input
    $.ajax({                       // initialize an AJAX request
      url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
      data: {
        'country': countryId       // add the country id to the GET parameters
      },
      success: function (data) {   // `data` is the return of the `load_cities` view function
        $("#id_city").html(data);  // replace the contents of the city input with the data that came from the server
      }
    });
  });

  $(document).ready(function(){
      
    $('#button-search').click(function(){
      $('.search-navbar').fadeToggle(100);
    })
  });