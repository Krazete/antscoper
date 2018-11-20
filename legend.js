var days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
var scroller, dynamicStyle;

function initLegend() {
    scroller = document.getElementById("scroller");
    dynamicStyle = document.getElementById("dynamic-style");
    initDays();
    initScanline();
    initTime();
    initTimeline();
}

function initDays() {
    var today = new Date().getDay();
    function clickDay() {
        var today = days.indexOf(this.id);
        selectDay(today);
    }
    function selectDay(day) {
        var todayButton = document.getElementById(days[day]);
        for (var id of days) {
            var dayButton = document.getElementById(id);
            dayButton.classList.remove("selected");
        }
        todayButton.classList.add("selected");
        scroller.innerHTML = "";
        initTimeline(day);
    }
    for (var id of days) {
        var dayButton = document.getElementById(id);
        dayButton.addEventListener("click", clickDay);
    }
    selectDay(today);
}

function initScanline() {
    var legend = document.getElementById("legend");
    var scanline = document.getElementById("scanline");
    function followMouse(e) {
        var legendBox = legend.getBoundingClientRect();
        scanline.style.left = (e.x - legendBox.x) + "px";
    }
    legend.addEventListener("mousemove", followMouse);
}

function initTime() {
    function updateTime() {
        var date = new Date();
        var time = date.getHours() + date.getMinutes() / 60;
        var percent = 100 * time / 24;
        dynamicStyle.innerHTML = `.timetable {
            background: linear-gradient(to right, gray ${percent}%, white ${percent}%);
            background: linear-gradient(to right, var(--color-2) ${percent}%, var(--color-3) ${percent}%);
        }`;
        setTimeout(updateTime, 60000);
        return time;
    }
    var time = updateTime();
    scroller.scrollTo(time * 1500/24, 0);
}

function initTimeline(day) {
    function newTimeheader(building) {
        var timeheader = document.createElement("div");
            timeheader.className = "timeheader";
            timeheader.dataset.building = building;
        return timeheader;
    }
    function newTimetable(building, day) {
        var timetable = document.createElement("div");
            timetable.className = "timetable";
            timetable.appendChild(newTimeline(building));
            for (var room in database[building]) {
                timetable.appendChild(newTimeline(building, room, day));
            }
        return timetable;
    }
    function newTimeline(building, room, day) {
        var timeline = document.createElement("div");
            timeline.className = "timeline";
            for (var i = 0; i < 24; i++) {
                timeline.appendChild(newTimeunit(i));
            }
            if (typeof room != "undefined") {
                timeline.dataset.room = room;
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
    for (var building in database) {
        scroller.appendChild(newTimeheader(building));
        scroller.appendChild(newTimetable(building, day));
    }
}
