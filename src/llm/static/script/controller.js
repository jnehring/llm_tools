// Function to show the loading icon
function showLoadingIcon() {
  document.body.classList.add('disabled');
  document.getElementById('loader-container').style.display = 'flex';
}

// Function to hide the loading icon
function hideLoadingIcon() {
  document.body.classList.remove('disabled');
  document.getElementById('loader-container').style.display = 'none';
}

function sendData() {
  showLoadingIcon()
  var xhttp;
  xhttp=new XMLHttpRequest();
  xhttp.onload = function() {
      hideLoadingIcon()
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