var day = 1; // 0 = sunday

var scroller, dynamicStyle;

function init() {
    scroller = document.getElementById("scroller");
    dynamicStyle = document.getElementById("dynamic-style");
    initDays();
    initTimeline();
    updateTime();
}

function initDays() { // TODO: fix days
    var days = document.getElementsByClassName("day");
    for (var day of days) {
        day.addEventListener("click", toggleDay);
    }
}

function toggleDay() { // TODO: delete this crap and put in an actual day switcher
    if (this.classList.contains("selected")) {
        this.classList.remove("selected");
    }
    else {
        this.classList.add("selected");
    }
}

function initTimeline() {
    for (var building in database) {
        scroller.appendChild(newTitle(building));
        scroller.appendChild(newTimetable(building));
    }
}

function newTitle(building) {
    var title = document.createElement("div");
        title.className = "building-name";
        title.dataset.label = building;
    return title;
}

function newTimetable(building) {
    var timetable = document.createElement("div");
        timetable.className = "timetable";
        timetable.appendChild(newTimeline(building));
        for (var room in database[building]) {
            timetable.appendChild(newTimeline(building, room));
        }
    return timetable;
}

function newTimeline(building, room) {
    var timeline = document.createElement("div");
        timeline.className = "timeline";
        for (var i = 0; i < 24; i++) {
            timeline.appendChild(newTimeunit(i));
        }
        if (typeof room != "undefined") {
            timeline.dataset.label = room;
            for (var hours of database[building][room].schedule[day]) {
                timeline.appendChild(newTimespan(hours[0], hours[1]));
            }
        }
    return timeline;
}

function newTimeunit(i) {
    var timeunit = document.createElement("div");
        timeunit.className = "timeunit";
    return timeunit;
}

function newTimespan(a, b) {
    var timespan = document.createElement("div");
        timespan.className = "timespan";
        timespan.style.left = (100 * a / 24) + "%";
        timespan.style.width = (100 * (b - a) / 24) + "%";
    return timespan;
}

function updateTime() {
    var date = new Date();
    var now = date.getHours() + date.getMinutes() / 60;
    var percent = 100 * now / 24;
    dynamicStyle.innerHTML = `.timeline {
        background: linear-gradient(to right, #024 ${percent}%, #024 ${percent}%);
    }`;
    setTimeout(updateTime, 60000);
}

window.addEventListener("DOMContentLoaded", init);
