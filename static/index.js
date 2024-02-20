var query;
var database = {};
var geo = [];
var myatlascms = "https://www.myatlascms.com/map/api/v2/locations?map=463&api_key=3715298bef4e8732196adf0b95254dd5";
var geo_backup = "/static/geo_backup.json";

function init() {
    query = document.getElementById("query");
    load("GET", myatlascms).then(initMapData).catch(function (error) {
        console.warn(error);
        console.log('Using backup map data.');
        load("GET", geo_backup).then(initMapData);
    });
    initLegend();
    initSearch();
    history.replaceState("", document.title, window.location.pathname); /* remove hash */
}

function initMapData(response) {
    for (var item of response) {
        geo.push(item);
    }
    initMap();
}

function search() {
    var lower = query.value.toLowerCase();
    function updateResults() {
        if (!lower || lower in database) {
            legend.classList.remove("noclass");
        }
        else {
            legend.classList.add("noclass");
        }
        for (var building in database) {
            var block = document.getElementById(building);
            block.classList.add("hidden");
            if (building.includes(lower)) {
                block.classList.remove("hidden");
            }
        }
    }
    if (lower in database) {
        initTimeline(today);
        updateResults();
    }
    else {
        load("POST", "/data.json?building=" + lower).then(function (response) {
            for (var key in response) {
                database[key] = response[key];
            }
            initTimeline(today);
            updateResults();
        });
    }
}

function initSearch() {
    function exitSearch(e) {
        if (e.keyCode == 13) {
            this.blur();
        }
    }
    function hashSearch() {
        query.value = decodeURIComponent(location.hash.slice(1));
        search();
    }
    query.addEventListener("change", search);
    query.addEventListener("keydown", exitSearch);
    window.addEventListener("hashchange", hashSearch);
}

function load(method, path) {
    function request(resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open(method, path, true);
        xhr.onload = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                resolve(JSON.parse(this.response));
    		}
            else {
                reject(new Error("Could not load '" + path + "'."));
            }
    	};
        xhr.onerror = function() {
            reject(new Error("Could not load '" + path + "'."));
        };
        xhr.send();
    }
    return new Promise(request);
}

window.addEventListener("DOMContentLoaded", init);
