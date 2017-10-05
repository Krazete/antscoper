/* Building Information */
var geo = {
	BS3:  {"latitude": 33.64532, "longitude": -117.84608, "distance": 0, "name": "Biological Sciences III"},
	DBH:  {"latitude": 33.64326, "longitude": -117.84198, "distance": 0, "name": "Donald Bren Hall"},
	EH:   {"latitude": 33.64376, "longitude": -117.84101, "distance": 0, "name": "Engineering Hall"},
	ELH:  {"latitude": 33.64447, "longitude": -117.84071, "distance": 0, "name": "Engineering Lecture Hall"},
	HG:   {"latitude": 33.64825, "longitude": -117.84451, "distance": 0, "name": "Humanities Gateway"},
	HH:   {"latitude": 33.64733, "longitude": -117.84398, "distance": 0, "name": "Humanities Hall"},
	HIB:  {"latitude": 33.64841, "longitude": -117.84383, "distance": 0, "name": "Humanities Instructional Building"},
	HICF: {"latitude": 33.64687, "longitude": -117.84680, "distance": 0, "name": "Humanities Interim Classroom Facility"},
	HSLH: {"latitude": 33.64559, "longitude": -117.84466, "distance": 0, "name": "Howard Schneiderman Lecture Hall"},
	IAB:  {"latitude": 33.64822, "longitude": -117.84534, "distance": 0, "name": "Intercollegiate Athletics Building"},
	ICF:  {"latitude": 33.64443, "longitude": -117.83997, "distance": 0, "name": "Interim Classroom Facility"},
	ICS:  {"latitude": 33.64428, "longitude": -117.84180, "distance": 0, "name": "Information & Computer Science"},
	LLIB: {"latitude": 33.64713, "longitude": -117.84109, "distance": 0, "name": "Langson Library"},
	MM:   {"latitude": 33.64933, "longitude": -117.84445, "distance": 0, "name": "Music & Media Building"},
	MPAA: {"latitude": 33.64707, "longitude": -117.83695, "distance": 0, "name": "Multipurpose Academic & Administrative Building"},
	MSTB: {"latitude": 33.64208, "longitude": -117.84442, "distance": 0, "name": "Multipurpose Science & Technology Building"},
	PCB:  {"latitude": 33.64451, "longitude": -117.84281, "distance": 0, "name": "Parkview Classroom Building"},
	PSCB: {"latitude": 33.64341, "longitude": -117.84349, "distance": 0, "name": "Physical Sciences Classroom Building"},
	PSLH: {"latitude": 33.64340, "longitude": -117.84396, "distance": 0, "name": "Physical Sciences Lecture Hall"},
	RH:   {"latitude": 33.64451, "longitude": -117.84412, "distance": 0, "name": "Rowland Hall"},
	SBSG: {"latitude": 33.64737, "longitude": -117.83909, "distance": 0, "name": "Social & Behavioral Sciences Gateway"},
	SE:   {"latitude": 33.64615, "longitude": -117.83889, "distance": 0, "name": "Social Ecology I"},
	SE2:  {"latitude": 33.64656, "longitude": -117.83915, "distance": 0, "name": "Social Ecology II"},
	SH:   {"latitude": 33.64621, "longitude": -117.84484, "distance": 0, "name": "Steinhaus Hall"},
	SSH:  {"latitude": 33.64623, "longitude": -117.84007, "distance": 0, "name": "Social Science Hall"},
	SSL:  {"latitude": 33.64590, "longitude": -117.84000, "distance": 0, "name": "Social Science Lab"},
	SSLH: {"latitude": 33.64723, "longitude": -117.83973, "distance": 0, "name": "Social Science Lecture Hall"},
	SSPA: {"latitude": 33.64694, "longitude": -117.83955, "distance": 0, "name": "Social Science Plaza A"},
	SST:  {"latitude": 33.64646, "longitude": -117.84027, "distance": 0, "name": "Social Science Tower"},
	SSTR: {"latitude": 33.64698, "longitude": -117.84024, "distance": 0, "name": "Social Science Trailer"}
};

function forGeo(f) {
	Object.keys(geo).forEach(function (e) {
		f(geo[e], e);
	});
}

/* Leaflet */
var leafletmap = L.map("map").setView([33.64625, -117.84215], 16);
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw", {
	maxZoom: 18,
	id: "mapbox.streets"
}).addTo(leafletmap);
forGeo(function(e, o) {
	//L.circle([e.latitude, e.longitude]).bindPopup(e.name + " (" + o + ")").addTo(leafletmap);
});

var bubble;
var marker;

function distance(v, w) {
	return Math.sqrt(Math.pow(w.latitude - v.latitude, 2) + Math.pow(w.longitude - v.longitude, 2));
}

function onLeafletLocate(e) {
	if (bubble) {
		bubble.removeFrom(leafletmap);
	}
	bubble = L.circle([e.latitude, e.longitude], e.accuracy / 2, {
		weight: 0,
		fillColor: "#bdf",
		fillOpacity: 0.5
	}).addTo(leafletmap).bringToBack();

	if (marker) {
		marker.removeFrom(leafletmap);
	}
	marker = L.marker([e.latitude, e.longitude]).addTo(leafletmap);

	forGeo(function(object, name) {
		object.distance = distance(e, object) * 1000;
		L.circle([object.latitude, object.longitude], 15, {weight: 1, fillOpacity: 1 / Math.pow(Math.E, distance(e, object) * 500)}).bindPopup(object.name + " (" + name + ")").addTo(leafletmap);
	});
}

function onLeafletLocateError(e) {
	console.log(e.message);
}

var watcher = leafletmap.locate({watch: true});
watcher.on("locationfound", onLeafletLocate);
watcher.on("locationerror", onLeafletLocateError);

/* Table */

var TimeTable = {
	"new": function(data) {
		var table = document.createElement("table");
		init(table, data, properties);
		return {
			"data": data,
			"table": table,
			"sort": function() {
				sortByDistance();
				sortByHoursUntilNext();
				sortByHoursFromLast();
				sortByBuildingAndRoom();
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
	"init": function(table, data, properties) {
		TimeTable.initTHead(table, properties);
		TimeTable.initTBody(table, data, properties);
		TimeTable.initTFoot(table);
		window.addEventListener("resize", table.resize);
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
	"initTBody": function(table, data, properties) {
		var tbody = table.createTBody();
		var start = 0;
		var end = data.length;
		for (var i = start; i < end; i++) {
			var tr = tbody.insertRow();
			var td;
			td = tr.insertCell();
			td.innerHTML = data[i].bldg + " " + data[i].room;
			td = tr.insertCell();
			td.setAttribute("colspan", 7);
			var timeline = TimeTable.newTimeline(6, 24);
			td.appendChild(timeline);
			for (var j = 6 * 2; j < 24 * 2; j++) {
				if (data[i].we.some(function(e) {return e[0] * 2 <= j && j < e[1] * 2})) {
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

var table = document.createElement("table");
table.className = "timetable";
TimeTable.init(table, database, ["room", "distance", "last_active"]);
document.getElementById("list").appendChild(table);

// Notes
// The TimeTable object will take Data (list of objects) and a Table.
// It will add a Row property to every Datum.
// There will be a sort function that can sort the Data and refresh the list of Rows displayed in the table.
// When a Row is hovered over or clicked, certain Data will be displayed.
//
// Questions
// Should I link each row to a piece of data, or should I link data to each row? Or neither?
