var days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
var today, legend, scroller, dynamicStyle;

function initLegend() {
    today = new Date().getDay();
    legend = document.getElementById("legend");
    scroller = document.getElementById("scroller");
    dynamicStyle = document.getElementById("dynamic-style");
    initScanline();
    initDays();
    initTime();
}

function initScanline() {
    var scanline = document.getElementById("scanline");
    function followMouse(e) {
        var legendBox = legend.getBoundingClientRect();
        scanline.style.left = (e.x - legendBox.x) + "px";
    }
    legend.addEventListener("mousemove", followMouse);
}

function initDays() {
    function clickDay() {
        today = days.indexOf(this.id);
        selectDay(today);
    }
    function selectDay(day) {
        var todayButton = document.getElementById(days[day]);
        for (var id of days) {
            var dayButton = document.getElementById(id);
            dayButton.classList.remove("selected");
        }
        todayButton.classList.add("selected");
        search();
    }
    for (var id of days) {
        var dayButton = document.getElementById(id);
        dayButton.addEventListener("click", clickDay);
    }
    selectDay(today);
}

function getTime() {
    var date = new Date();
    var time = date.getHours() + date.getMinutes() / 60;
    return time;
}

function initTime() {
    var time = getTime();
    var percent = 100 * time / 24;
    dynamicStyle.innerHTML = `.timetable {
        background: linear-gradient(to right, gray ${percent}%, white ${percent}%);
        background: linear-gradient(to right, var(--color-2) ${percent}%, var(--color-3) ${percent}%);
    }`;
    setTimeout(initTime, 60000);
}

function initTimeline() {
    function newTimeheader(building) {
        var timeheader = document.createElement("div");
            timeheader.className = "timeheader";
            timeheader.id = building;
        return timeheader;
    }
    function newTimetable(building, day) {
        var timetable = document.createElement("div");
            timetable.className = "timetable";
            timetable.appendChild(newTimeline(building));
            for (var room of sortedKeys(database[building])) {
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
                    timeline.appendChild(newTimespan(building, room, hours[0], hours[1], day));
                }
            }
        return timeline;
    }
    function newTimeunit(i) {
        var timeunit = document.createElement("div");
            timeunit.className = "timeunit";
        return timeunit;
    }
    function newTimespan(building, room, a, b, day) {
        var timespan = document.createElement("div");
            timespan.className = "timespan";
            timespan.style.left = (100 * a / 24) + "%";
            timespan.style.width = (100 * (b - a) / 24) + "%";
            var anchor = document.createElement("a");
                anchor.target = "_blank";
                anchor.href = "https://www.reg.uci.edu/perl/WebSoc?" + [
                    "YearTerm=" + database[building][room].yearterm,
                    "Bldg=" + building,
                    "Room=" + room,
                    "Days=" + (day == 5 ? "f" : days[day]),
                    "StartTime=" + formatTime(a),
                    "EndTime=" + formatTime(b),
                    "ShowFinals=1"
                ].join("&");
            timespan.appendChild(anchor);
        return timespan;
    }
    function formatTime(t) {
        var meridiem = "am";
        var hour = Math.floor(t);
        var minute = Math.floor(60 * (t - hour));
        if (hour >= 12) {
            meridiem = "pm";
            if (hour > 12) {
                hour -= 12;
            }
        }
        if (hour <= 0 || hour >= 24) { // will probably never happen
            meridiem = "am";
            hour = "12";
        }
        return hour + ":" + (minute < 10 ? "0" : "") + minute + meridiem;
    }
    function sortedKeys(dict) {
        var keys = Object.keys(dict);
        keys.sort(byAlpha);
        return keys;
    }
    function byAlpha(a, b) {
        return a < b ? -1 : a > b ? 1 : 0;
    }
    scroller.innerHTML = "";
    for (var building of sortedKeys(database)) {
        scroller.appendChild(newTimeheader(building));
        scroller.appendChild(newTimetable(building, today));
    }
    var time = getTime();
    scroller.scrollTo((time - 1) * 1500/24, 0);
}
