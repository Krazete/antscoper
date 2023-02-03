var query;
var database = {};
var geo = [];

function init() {
    query = document.getElementById("query");
    load("GET", "/map.json").then(function (response) {
        for (var item of response) {
            geo.push(item);
        }
        initMap();
    });
    initLegend();
    initSearch();
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
    	};
        xhr.onerror = function() {
            reject(new Error("Could not load '" + path + "'."));
        };
        xhr.send();
    }
    return new Promise(request);
}

window.addEventListener("DOMContentLoaded", init);
