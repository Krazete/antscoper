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
	leafletmap.setView(mmm.getLatLng(), 17);
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

var TimeTable = {
	"newTime": function() {
		var date = new Date();
		return date.getHours() + date.getMinutes() / 60;
	},
	"newTable": function(table, data, properties) {
		TimeTable.initTable(table, data, properties);
		window.addEventListener("resize", table.resize);
	},
	"new": function(data, properties) {
		var table = document.createElement("table");
		table.className = "timetable";
		TimeTable.newTable(table, data, properties);
		return {
			"name": properties[0],
			"data": data,
			"table": table,
			"sort": function() {
				this.data = this.data.sort(function(a, b) {
					var time = TimeTable.newTime();
					var chapa = a.mo[0] ? a.mo[0][0] : 24 - time;
					var chapb = b.mo[0] ? b.mo[0][0] : 24 - time;
					return -chapb + chapa;
				});
				TimeTable.newTable(table, data, properties);
				// sortByDistance();
				// sortByHoursUntilNext();
				// sortByHoursFromLast();
				// sortByBuildingAndRoom();
			},
			"resize": function() {},
			"changeDay": function(e) {
				console.log(e.target.value);
				for (var i = 1; i < rows.length; i++) {
					rows[i];
				}
			}
		};
	},
	"initTable": function(table, data, properties) {
		var start = 0;
		var end = database.length;
		for (var i = start; i < end; i++) {
			var tr = table.insertRow();
			var td;
			td = tr.insertCell();
			td.innerHTML = data[i].bldg + " " + data[i].room;
			td = tr.insertCell();
			var timeline = TimeTable.newTimeline(6, 24);
			td.appendChild(timeline);
			for (var j = 6 * 2; j < 24 * 2; j++) {
				if (data[i].mo.some(function(e) {return e[0] * 2 <= j && j < e[1] * 2})) {
					timeline.children[j - 6 * 2].classList.add("active");
				}
			}
			td = tr.insertCell();
			try {
				td.innerHTML = geo[data[i].bldg].distance;
			} catch(e) {}
			td = tr.insertCell();
			td.innerHTML = data[i].last_active;
		}
	},
	"initTHead": function(table, properties) {
		var thead = table.createTHead();
		var tr = thead.insertRow();
		var th = tr.appendChild(document.createElement("th"));
		th.innerHTML = properties[0];
		TimeTable.newDays(tr, true);
		for (var i = 1; i < properties.length; i++) {
			var th = tr.appendChild(document.createElement("th"));
			th.innerHTML = properties[i];
		}
	},
	"initTFoot": function(table) {
		var tfoot = table.createTFoot();
		var td = tfoot.insertRow().insertCell();
		td.setAttribute("colspan", 10);
		td.innerHTML = "Switch Sorting Priority | Toggle Column Visibility | Reset Location | Reset Time | Previous | Next | Search";
	},

	"newDays": function(tr, abbreviate) {
		var days = abbreviate ? ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"] : ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
		for (var i = 0; i < 7; i++) {
			var th = tr.appendChild(document.createElement("th"));
			th.className = "day";
			th.innerHTML = days[i];
			th.value = i;
			th.addEventListener("click", TimeTable.changeDay);
		}
	},
	"newTimeline": function(a, b) {
		var timeline = document.createElement("div");
		timeline.className = "timeline";
		for (var i = a * 2; i < b * 2; i++) {
			var timeblock = timeline.appendChild(document.createElement("div"));
			timeblock.className = "timeblock";
			if ((i + 1) % 2) {
				timeblock.innerHTML = (i / 2 - 1) % 12 + 1;
			}
		}
		return timeline;
	}
};

var timetable = TimeTable.new(database, ["room", "distance", "last_active"]);
document.getElementById("list").appendChild(timetable.table);

// Major
// optimize database requests (for quota limit)
// change last_active to active_quarters
// only request last four quarters from database
// keep copy of mapbox data
// only request rooms database with building abbreviations found in mapbox data
//
// Minor
// change data retrieval methods (use codes directly instead of checking websoc form)
// stop retrieval methods from requesting COM quarter data
// convert StringProperty to JsonProperty for all of Room's day attributes
