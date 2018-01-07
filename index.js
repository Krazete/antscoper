/* Leaflet */
var leafletmap = L.map("map", {
    "center": [33.64625, -117.84215],
    "zoom": 16,
    "worldCopyJump": true
});
var myRenderer = L.svg({
	"padding": 2
});
var tiles = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw", {
	"maxZoom": 18,
	"id": "mapbox.streets",
	"worldCopyJump": true
});
tiles.addTo(leafletmap);

var watcherBubble = L.circle([90, 180]);
watcherBubble.addTo(leafletmap);

var watcherMarker = L.marker([90, 180]);
watcherMarker.on("click", function() {
	leafletmap.setView(watcherMarker.getLatLng(), 16);
});
watcherMarker.addTo(leafletmap);

geo.filter(e => e.name.includes("(")).forEach(function(bldg) {
	bldg.latlng = L.latLng(bldg.lat, bldg.lng);
	bldg.watcherBubble = L.circle(bldg.latlng, 15, {
		"weight": 1,
		"color": "#0064a4",
		"fillOpacity": 0,
		"renderer": myRenderer
	});
	bldg.watcherBubble.bindPopup(bldg.name);
	bldg.watcherBubble.addTo(leafletmap);
});

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

	geo.filter(e => e.name.includes("(")).forEach(function(bldg) {
		bldg.distance = leafletmap.distance(location.latlng, bldg.latlng);
		bldg.watcherBubble.setStyle({
			"fillOpacity": 1 / Math.pow(Math.E, bldg.distance / 272)
		});

        database.filter(e => bldg.name.includes(e.id.split(" ")[0]))
        .forEach(e => e.distance = bldg.distance);
	});
    //timetable.sortByProperty("distance");
}

function onLeafletLocateError(e) {
	console.log(e.message);
}

var watcher = leafletmap.locate({"watch": true});
watcher.on("locationfound", onLeafletLocate);
watcher.on("locationerror", onLeafletLocateError);

/* Table */

yearterm = "2017-92";
for(var x, i = 0; x = database[i]; i++) {
    x.id = "<a href=\"https://www.reg.uci.edu/perl/WebSoc?YearTerm=" + yearterm + "&ShowFinals=0&ShowComments=0&Days=" + "UMTWHFS"[new Date().getDay()] + "&Bldg=" + x.id.split(" ")[0] + "&Room=" + x.id.split(" ")[1] + "\" target=\"_blank\">" + x.id + "</a>";
}
var timetable = TimeTable.new(database, ["room", "distance", "last_active"]);
document.getElementById("list").appendChild(timetable.table);

newChronolog(database);

// Major
// optimize database requests (for quota limit)
// change last_active to active_quarters
// only request last four quarters from database
// keep copy of mapbox data
// only request rooms database with building abbreviations found in mapbox data
// verify that Array.prototype.filter causes a problem in mobile Safari
//
// Minor
// change data retrieval methods (use codes directly instead of checking websoc form)
// stop retrieval methods from requesting COM quarter data
