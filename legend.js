var days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
var today, legend, scroller, dynamicStyle;

function initLegend() {
    today = new Date().getDay();
    legend = document.getElementById("legend");
    scroller = document.getElementById("scroller");
    dynamicStyle = document.getElementById("dynamic-style");
    if (databaseIsEmpty()) {
        legend.classList.add("noclass");
    }
    initScanline();
    initSearch();
    initDays();
    initTime();
}

function databaseIsEmpty() {
    for (building in database) {
        for (room in database[building]) {
            for (sch of database[building][room].schedule) {
                if (sch.length > 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

function initScanline() {
    var scanline = document.getElementById("scanline");
    function followMouse(e) {
        var legendBox = legend.getBoundingClientRect();
        scanline.style.left = (e.x - legendBox.x) + "px";
    }
    legend.addEventListener("mousemove", followMouse);
}

function initSearch() {
    var query = document.getElementById("query");
    function search() {
        var lower = query.value.toLowerCase();
        for (var building in database) {
            var block = document.getElementById(building);
            block.classList.add("hidden");
            if (building.includes(lower)) {
                block.classList.remove("hidden");
            }
        }
    }
    function exitSearch(e) {
        if (e.keyCode == 13) {
            this.blur();
        }
    }
    function hashSearch() {
        query.value = decodeURIComponent(location.hash.slice(1));
        search();
    }
    query.addEventListener("input", search);
    query.addEventListener("keydown", exitSearch);
    window.addEventListener("hashchange", hashSearch);
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
        scroller.innerHTML = "";
        initTimeline(day);
    }
    for (var id of days) {
        var dayButton = document.getElementById(id);
        dayButton.addEventListener("click", clickDay);
    }
    selectDay(today);
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
    scroller.scrollTo((time - 1) * 1500/24, 0);
}

function initTimeline(day) {
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
                    timeline.appendChild(newTimespan(building, room, hours[0], hours[1]));
                }
            }
        return timeline;
    }
    function newTimeunit(i) {
        var timeunit = document.createElement("div");
            timeunit.className = "timeunit";
        return timeunit;
    }
    function newTimespan(building, room, a, b) {
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
    for (var building of sortedKeys(database)) {
        scroller.appendChild(newTimeheader(building));
        scroller.appendChild(newTimetable(building, day));
    }
}
