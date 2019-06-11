const button = document.getElementById("refresh");
let update;

function toggleRefresh() {
  if (button.innerText === "Refresh: On") {
    button.innerText = "Refresh: Off";
    update = false
  } else {
    button.innerText = "Refresh: On";
    update = true
  }
}

setInterval(function() {
  if (button.innerText === "Refresh: On") {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState === 4 && this.status === 200) {
       document.getElementById("time").innerHTML = "Last Updated: " + this.responseText;
       console.log("Updated Time" + this.responseText)
      }
    };
    xhttp.open("GET", "api/time", true);
    xhttp.send();
  }
}, 10000);