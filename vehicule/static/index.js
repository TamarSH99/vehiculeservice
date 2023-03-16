document.getElementById("submit").addEventListener("click", function(event) {
    event.preventDefault();
    var city1 = document.getElementById("city1").value;
    var city2 = document.getElementById("city2").value;
    var carId = document.getElementById("carId").value;
    if (city1 != city2 && (carId <=9 && carId >=0 ))
      showMap(city1, city2, carId);
    else
      alert("Veuillez entrer des données valides")
  });

  function showMap(city1, city2, carId) {
    $.ajax({
      type: "POST",
      contentType: "application/json",
      url: "/input",
      data: JSON.stringify({ "city1": city1, "city2": city2  ,"carId": carId}),
      dataType: "json",
      success: function(result) {
        //   $('.right').load('/main.html');
        location.reload();
      },
      error: function(xhr, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  }
  

 