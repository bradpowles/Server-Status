const button = document.getElementById("refresh");
const table = document.getElementById("status_table");

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
       while(table.hasChildNodes()) {table.removeChild(table.firstChild)}
       table.innerHTML += "<tr><th>Org</th><th>URL</th><th>Status</th></tr>";
       for (let org in data) {
           for (let url in data[org]) {
               let tr = "<tr>";
               tr += "<td>" + data[org][url].group + "</td><td>" + data[org][url].name + "</td>";
               if (data[org][url].status === "up") {
                   tr += "<td style=\"color:green\">" + data[org][url].status + "</td>";
               } else {
                 tr += "<td style=\"color:red\">" + data[org][url].status + "</td>";
               }
               tr += "</tr>";
               table.innerHTML += tr;
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