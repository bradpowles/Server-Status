const button = document.getElementById("refresh");

function toggleRefresh() {
  if (button.innerText === "Refresh: On") {
    button.innerText = "Refresh: Off";
  } else {
    button.innerText = "Refresh: On";
  }
}

function updateTime() {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function() {
      if (this.readyState === 4 && this.status === 200) {
       document.getElementById("time").innerHTML = "Last Updated: " + this.responseText;
      } else if ((this.status === 200).not) {
          console.log("Error: Connecting to API.")
      }
    };
    request.open("GET", "api/time", true);
    request.send();
}

function updateStatus() {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function() {
      if (this.readyState === 4 && this.status === 200) {
       let data = JSON.parse(this.responseText);
       for (let org in data) {
           for (let url in data[org]) {
               let row = document.getElementById(data[org][url].name).childNodes;
               row[5].innerHTML = "<span class=\"status "+ data[org][url].status + "\"></span>";
           }
       }
      } else if ((this.status === 200).not) {
          console.log("Error: Connecting to API.")
      }
    };
    request.open("GET", "api/status/current", true);
    request.send();
}

setInterval(function() {
  if (button.innerText === "Refresh: On") {
    updateTime(); updateStatus();
  }
}, 10000);