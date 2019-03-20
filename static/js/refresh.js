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
    if (window.location.href.indexOf("?update=") > -1) {
      location.reload();
    } else {
      window.location.href = window.location.href + "?update=" + update;
    }
  }
}, 30000);