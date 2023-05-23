function sendData() {
  var xhttp;
  xhttp=new XMLHttpRequest();
  xhttp.onload = function() {
      resp = JSON.parse(xhttp.responseText)
      document.getElementById("display_txt").innerHTML = resp["response"];
 };
  xhttp.open("POST", "api/generate", true);
  xhttp.setRequestHeader("Content-Type", "application/json");
  data = {};
  data.doc = document.getElementById("input_txt").value;
  xhttp.send(JSON.stringify(data));
}

function clearData() {
    document.getElementById("input_txt").value = "";
    document.getElementById("display_txt").innerHTML = "";
}