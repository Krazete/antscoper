function init() {

var days = document.getElementsByClassName("day");
for (var i = 0; i < days.length; i++) {
    days[i].addEventListener("click", function () {
        this.classList.add("selected");
    });
}

var timeline = Array.from(document.getElementsByClassName("timeline"));
timeline.forEach(function (e) {
    for (var c = 0; c < 24; c++) {
        var timeblock = document.createElement("div");
        timeblock.className = "timeblock";
        timeblock.innerHTML = c % 12 ? c % 12 : 12;
        timeblock.innerHTML += c < 12 ? " am" : " pm";
        e.appendChild(timeblock);
    }
});

var filling = false;
var timeblocks = Array.from(document.getElementsByClassName("timeblocks"));
timeblocks.forEach(function (e) {
    for (var c = 0; c < 48; c++) {
        var timeblock = document.createElement("div");
        timeblock.className = "timeblock";
        if (filling) {
            timeblock.classList.add("filled");
        }
        if (Math.random() < 0.1) {
            filling = !filling;
        }
        e.appendChild(timeblock);
    }
});

var dynamicStyle = document.getElementById("dynamic-style");
function updateTime() {
    var date = new Date();
    var now = date.getHours() + date.getMinutes() / 60;
    var percent = 100 * now / 24;
    dynamicStyle.innerHTML = `.rooms {
        background: linear-gradient(to right, #58b ${percent}%, #7ad ${percent}%);
    }`;
    setTimeout(updateTime, 60000);
}
updateTime();

}

window.addEventListener("DOMContentLoaded", init);
