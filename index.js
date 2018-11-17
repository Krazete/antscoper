var data, geo;

function init() {
    function callback(responses) {
        geo = responses[0];
        database = responses[1];
        initMap();
        initLegend();
    }

    Promise.all([
        load("./map.json"),
        load("./data.json")
    ]).then(callback);
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
