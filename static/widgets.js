var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
output.innerHTML = slider.value;

slider.oninput = function() {
  output.innerHTML = this.value/100;
}

function filter_out() {
  document.getElementById("search_filter").submit();
}
function search_for() {
  document.getElementById("search_filter").submit();
}