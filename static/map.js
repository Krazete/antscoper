function initMap() {
    /* Leaflet */
    var leafletmap = L.map("map", {
        "center": [33.64625, -117.84215],
        "zoom": 17,
        "worldCopyJump": true
    });
    var myRenderer = L.svg({
        "padding": 2
    });
    /* This is the TileLayer used by map.uci.edu. They finally changed and privated their access_token, making this unusable as of 2023.
    var tiles = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        "maxZoom": 18,
        "tileSize": 512,
        "zoomOffset": -1,
        "id": "mapbox/streets-v11",
        "accessToken": "pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw"
    });
    */
    var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        "maxZoom": 18,
        "attribution": '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });
    tiles.addTo(leafletmap);

    var watcherBubble = L.circle([90, 180]);
    watcherBubble.addTo(leafletmap);

    var watcherMarker = L.marker([90, 180]);
    watcherMarker.on("click", function() {
        leafletmap.setView(watcherMarker.getLatLng(), 16);
    });
    watcherMarker.addTo(leafletmap);

    for (var bldg of geo) {
        (function (bldg) {
            var inParen = bldg.name.match(/\((\w+)\)/);
            if (inParen) {
                bldg.latlng = L.latLng(bldg.lat, bldg.lng);
                bldg.watcherBubble = L.circle(bldg.latlng, 15, {
                    "weight": 2,
                    "color": "#0064a4",
                    "fillOpacity": 0,
                    "renderer": myRenderer
                });
                bldg.watcherBubble.bindPopup(function () {
                    var anchor = document.createElement("a");
                    anchor.href = "#" + inParen[1].toLowerCase();
                    anchor.innerHTML = bldg.name;
                    return anchor;
                });
                bldg.watcherBubble.addTo(leafletmap);
            }
        })(bldg);
    }

    function onLeafletLocate(location) {
        watcherBubble.setLatLng(location.latlng);
        watcherBubble.setRadius(location.accuracy);
        watcherBubble.setStyle({
            "stroke": false,
            "color": "#6aa2b8",
            "opacity": 0.75
        });
        watcherBubble.redraw();

        watcherMarker.setLatLng(location.latlng);

        for (var bldg of geo) {
            if (bldg.name.includes("(")) {
                try {
                    bldg.distance = leafletmap.distance(location.latlng, bldg.latlng);
                    bldg.watcherBubble.setStyle({
                        "fillOpacity": 1 / Math.pow(Math.E, bldg.distance / 272)
                    });
                }
                catch (e) {
                    console.log("Skipping \"" + bldg.name + "\" (malformed building data).", bldg);
                }
            }
        }
    }

    function onLeafletLocateError(e) {
        console.log(e.message);
    }

    var watcher = leafletmap.locate({"watch": true});
    watcher.on("locationfound", onLeafletLocate);
    watcher.on("locationerror", onLeafletLocateError);
}
