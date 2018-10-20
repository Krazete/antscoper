var day = 1; // 0 = sunday

var scroller = document.getElementById("scroller");
var dynamicStyle = document.getElementById("dynamic-style");

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
    for (var building in database) {
        var buildingTitle = createBuildingTitle(building);
        var buildingBlock = createBuildingBlock(building);
        scroller.appendChild(buildingTitle);
        scroller.appendChild(buildingBlock);
    }
}

function createBuildingTitle(building) {
    var buildingTitle = document.createElement("div");
        buildingTitle.className = "building-title";
        buildingTitle.innerHTML = building.toUpperCase();
    return buildingTitle;
}

function createBuildingBlock(building) {
    var buildingBlock = document.createElement("div");
        buildingBlock.className = "building-block";
        var timeline = createTimeline();
        buildingBlock.appendChild(timeline);
        for (var room of database[building]) {
            var roomBlock = createRoomBlock();
            buildingBlock.appendChild(roomBlock);
        }
    return buildingBlock;
}

function createTimeline() {
    var timelines = document.createElement("div");
        timelines.className = "timelines";
        var timeline = document.createElement("div");
            timeline.className = "timeline";
            var timeblock = document.createElement("div");
                timeblock.className = "timeblock";
            timeline.appendChild(timeblock);
        timelines.appendChild(timeline);
    return timelines;
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
