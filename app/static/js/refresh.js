const button = document.getElementById("refresh");
const table = document.getElementById("status_table");
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

function updateTime() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState === 4 && this.status === 200) {
       document.getElementById("time").innerHTML = "Last Updated: " + this.responseText;
      } else {
          console.log("Error: Connecting to API.")
      }
    };
    xhttp.open("GET", "api/time", true);
    xhttp.send();
}

function updateStatus() {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState === 4 && this.status === 200) {
       let data = JSON.parse(this.responseText);
       while(table.hasChildNodes()) {table.removeChild(table.firstChild)}
       table.innerHTML += "<tr><th>Org</th><th>URL</th><th>Code</th></tr>";
       for (let org in data) {
           for (let url in data[org]) {
               let tr = "<tr>";
               tr += "<td>" + data[org][url].group + "</td><td>" + data[org][url].name + "</td>";
               if (data[org][url].status_code === "200") {
                   tr += "<td style=\"color:green\">" + data[org][url].status_code + "</td>";
               } else {
                 tr += "<td style=\"color:red\">" + data[org][url].status_code + "</td>";
               }
               tr += "</tr>";
               table.innerHTML += tr;
           }
       }
      } else {
          console.log("Error: Connecting to API.")
      }
    };
    xhttp.open("GET", "api/status/current", true);
    xhttp.send();
}

setInterval(function() {
  if (button.innerText === "Refresh: On") {
    updateTime();
    updateStatus();
  }
}, 10000);