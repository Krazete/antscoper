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
        scroller.appendChild(createTitle(building));
        scroller.appendChild(createBuildingBlock(building));
    }
}

function createBuildingBlock(building) {
    var buildingTable = document.createElement("div");
        buildingTable.className = "timetable";
        buildingTable.appendChild(createTimeline(building));
        for (var room in database[building]) {
            buildingTable.appendChild(createTimerule(building, room));
        }
    return buildingTable;
}

function createTitle(building) {
    var bb = document.createElement("div");
        bb.className = "topper";
        bb.dataset.label = building;
    return bb;
}

function createTimeline(building) {
    var timeline = document.createElement("div");
        timeline.className = "timeline";
        timeline.dataset.label = building;
        for (var i = 0; i < 24; i++) {
            timeline.appendChild(createTimeBlock(i));
        }
    return timeline;
}

function createTimerule(building, room) {
    var schedule = document.createElement("div");
        schedule.className = "timeline";
        schedule.dataset.label = room;
        for (var i = 0; i < 24; i++) {
            schedule.appendChild(createTimeBlock(i));
        }
        for (var hours of database[building][room].schedule[day]) {
            schedule.appendChild(createTimeBubble(hours[0], hours[1]));
        }
    return schedule;
}

function createTimeBlock(i) {
    var timeblock = document.createElement("div");
        timeblock.className = "timeblock";
    return timeblock;
}

function createTimeBubble(a, b) {
    var timebubble = document.createElement("div");
        timebubble.className = "timebubble";
        timebubble.style.left = (100 * a / 24) + "%";
        timebubble.style.width = (100 * (b - a) / 24) + "%";
    return timebubble;
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
