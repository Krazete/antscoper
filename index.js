var data, geo;

function init() {
    load("./map.json").then(function (response) {
        geo = response;
        initMap();
    });
    load("./data.json").then(function (response) {
        database = response;
        initLegend();
    });
}

function load(path) {
    function request(resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", path, true);
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
