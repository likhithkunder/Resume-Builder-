function startLoading() {
    var button = document.getElementById("myButton");
    var loader = document.getElementById("loader");

    button.style.display = "none";
    loader.style.display = "flex";

    setTimeout(function() {
      button.style.display = "block";
      loader.style.display = "none";
    }, 5000); 
}

