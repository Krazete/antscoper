var day = 1; // 0 = sunday

var scroller;
var dynamicStyle;

function init() {
    initDays();
    initTimeline();
    updateTime();
}

function initDays() { // TODO: fix days
    var days = document.getElementsByClassName("day");
    for (var day of days) {
        day.addEventListener("click", toggle);
    }
}

function toggle() { // TODO: delete this crap and put in an actual day switcher
    if (this.classList.contains("selected")) {
        this.classList.remove("selected");
    }
    else {
        this.classList.add("selected");
    }
}

function initTimeline() {
    scroller = document.getElementById("scroller");
    dynamicStyle = document.getElementById("dynamic-style");
    for (var building in database) {
        scroller.appendChild(createBuildingTitle(building));
        scroller.appendChild(createBuildingBlock(building));
    }
}

function createBuildingTitle(building) {
    var buildingTitle = document.createElement("div");
        buildingTitle.className = "building";
        buildingTitle.innerHTML = building.toUpperCase();
    return buildingTitle;
}

function createBuildingBlock(building) {
    var buildingTable = document.createElement("div");
        buildingTable.className = "timetable";
        buildingTable.dataset.building = building; // TODO: weigh this vs createBuildingTitle
        buildingTable.appendChild(createTimeline(building));
        buildingTable.appendChild(createSchedule(building));
    return buildingTable;
}

function createTimeline(building) {
    var timeline = document.createElement("div");
        timeline.className = "timeline";
        timeline.dataset.building = building.toUpperCase();
        for (var i = 0; i < 24; i++) {
            timeline.appendChild(createTimeBlock(i));
        }
    return timeline;
}

function createTimeBlock(i) {
    var timeblock = document.createElement("div");
        timeblock.className = "timeblock";
        timeblock.innerHTML = (i % 12 ? i : 12) + (i < 12 ? "am" : "pm");
    return timeblock;
}

function createSchedule(building) {
    var scheduleSet = document.createElement("div");
        scheduleSet.className = "scheduleNOT";
        for (var room in database[building]) {
            scheduleSet.appendChild(createRoomBlock(building, room));
        }
    return scheduleSet;
}

function createRoomBlock(building, room) {
    var schedule = document.createElement("div");
        schedule.className = "schedule";
        schedule.dataset.room = room.toUpperCase();
        for (var hours of database[building][room].schedule[day]) {
            schedule.appendChild(createTimeBubble(hours[0], hours[1]));
        }
    return schedule;
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
    dynamicStyle.innerHTML = `.scrollbox {
        background: linear-gradient(to right, #58b ${percent}%, #7ad ${percent}%);
    }`;
    setTimeout(updateTime, 60000);
}

window.addEventListener("DOMContentLoaded", init);
