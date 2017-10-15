/* Building Information */
// var geo = {
// 	BS3:  {"latlng": L.latLng(33.64532, -117.84608), "distance": Infinity, "bubble": null, "name": "Biological Sciences III"},
// 	DBH:  {"latlng": L.latLng(33.64326, -117.84198), "distance": Infinity, "bubble": null, "name": "Donald Bren Hall"},
// 	EH:   {"latlng": L.latLng(33.64376, -117.84101), "distance": Infinity, "bubble": null, "name": "Engineering Hall"},
// 	ELH:  {"latlng": L.latLng(33.64447, -117.84071), "distance": Infinity, "bubble": null, "name": "Engineering Lecture Hall"},
// 	HG:   {"latlng": L.latLng(33.64825, -117.84451), "distance": Infinity, "bubble": null, "name": "Humanities Gateway"},
// 	HH:   {"latlng": L.latLng(33.64733, -117.84398), "distance": Infinity, "bubble": null, "name": "Humanities Hall"},
// 	HIB:  {"latlng": L.latLng(33.64841, -117.84383), "distance": Infinity, "bubble": null, "name": "Humanities Instructional Building"},
// 	HICF: {"latlng": L.latLng(33.64687, -117.84680), "distance": Infinity, "bubble": null, "name": "Humanities Interim Classroom Facility"},
// 	HSLH: {"latlng": L.latLng(33.64559, -117.84466), "distance": Infinity, "bubble": null, "name": "Howard Schneiderman Lecture Hall"},
// 	IAB:  {"latlng": L.latLng(33.64822, -117.84534), "distance": Infinity, "bubble": null, "name": "Intercollegiate Athletics Building"},
// 	ICF:  {"latlng": L.latLng(33.64443, -117.83997), "distance": Infinity, "bubble": null, "name": "Interim Classroom Facility"},
// 	ICS:  {"latlng": L.latLng(33.64428, -117.84180), "distance": Infinity, "bubble": null, "name": "Information & Computer Science"},
// 	LLIB: {"latlng": L.latLng(33.64713, -117.84109), "distance": Infinity, "bubble": null, "name": "Langson Library"},
// 	MM:   {"latlng": L.latLng(33.64933, -117.84445), "distance": Infinity, "bubble": null, "name": "Music & Media Building"},
// 	MPAA: {"latlng": L.latLng(33.64707, -117.83695), "distance": Infinity, "bubble": null, "name": "Multipurpose Academic & Administrative Building"},
// 	MSTB: {"latlng": L.latLng(33.64208, -117.84442), "distance": Infinity, "bubble": null, "name": "Multipurpose Science & Technology Building"},
// 	PCB:  {"latlng": L.latLng(33.64451, -117.84281), "distance": Infinity, "bubble": null, "name": "Parkview Classroom Building"},
// 	PSCB: {"latlng": L.latLng(33.64341, -117.84349), "distance": Infinity, "bubble": null, "name": "Physical Sciences Classroom Building"},
// 	PSLH: {"latlng": L.latLng(33.64340, -117.84396), "distance": Infinity, "bubble": null, "name": "Physical Sciences Lecture Hall"},
// 	RH:   {"latlng": L.latLng(33.64451, -117.84412), "distance": Infinity, "bubble": null, "name": "Rowland Hall"},
// 	SBSG: {"latlng": L.latLng(33.64737, -117.83909), "distance": Infinity, "bubble": null, "name": "Social & Behavioral Sciences Gateway"},
// 	SE:   {"latlng": L.latLng(33.64615, -117.83889), "distance": Infinity, "bubble": null, "name": "Social Ecology I"},
// 	SE2:  {"latlng": L.latLng(33.64656, -117.83915), "distance": Infinity, "bubble": null, "name": "Social Ecology II"},
// 	SH:   {"latlng": L.latLng(33.64621, -117.84484), "distance": Infinity, "bubble": null, "name": "Steinhaus Hall"},
// 	SSH:  {"latlng": L.latLng(33.64623, -117.84007), "distance": Infinity, "bubble": null, "name": "Social Science Hall"},
// 	SSL:  {"latlng": L.latLng(33.64590, -117.84000), "distance": Infinity, "bubble": null, "name": "Social Science Lab"},
// 	SSLH: {"latlng": L.latLng(33.64723, -117.83973), "distance": Infinity, "bubble": null, "name": "Social Science Lecture Hall"},
// 	SSPA: {"latlng": L.latLng(33.64694, -117.83955), "distance": Infinity, "bubble": null, "name": "Social Science Plaza A"},
// 	SST:  {"latlng": L.latLng(33.64646, -117.84027), "distance": Infinity, "bubble": null, "name": "Social Science Tower"},
// 	SSTR: {"latlng": L.latLng(33.64698, -117.84024), "distance": Infinity, "bubble": null, "name": "Social Science Trailer"}
// };

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

var bubble = L.circle([90, 180]);
bubble.addTo(leafletmap);

var mmm = L.marker([90, 180]);
mmm.on("click", function() {
	leafletmap.setView(mmm.getLatLng(), 16);
});
mmm.addTo(leafletmap);

geo.filter(e => e.marker_feed.includes("academic")).forEach(function(bldg) {
	bldg.latlng = L.latLng(bldg.lat, bldg.lng);
	bldg.bubble = L.circle(bldg.latlng, 15, {
		"weight": 1,
		"color": "#0064a4",
		"fillOpacity": 0,
		"renderer": myRenderer
	});
	bldg.bubble.bindPopup(bldg.name);
	bldg.bubble.addTo(leafletmap);
});

function onLeafletLocate(location) {
	bubble.setLatLng(location.latlng);
	bubble.setRadius(location.accuracy);
	bubble.setStyle({
		"stroke": false,
		"color": "#6aa2b8",
		"opacity": 0.75
	});
	bubble.redraw();

	mmm.setLatLng(location.latlng);

	geo.filter(e => e.marker_feed.includes("academic")).forEach(function(bldg) {
		bldg.distance = leafletmap.distance(location.latlng, bldg.latlng);
		bldg.bubble.setStyle({
			"fillOpacity": 1 / Math.pow(Math.E, bldg.distance / 272)
		});
	});
}

function onLeafletLocateError(e) {
	console.log(e.message);
}

var watcher = leafletmap.locate({"watch": true});
watcher.on("locationfound", onLeafletLocate);
watcher.on("locationerror", onLeafletLocateError);

/* Table */

var timetable = TimeTable.new(database, ["room", "distance", "last_active"]);
document.getElementById("list").appendChild(timetable.table);

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
