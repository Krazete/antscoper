/* Building Information */
var geo = {
	BS3:  {lat: 33.64532, long: -117.84608, name: "Biological Sciences III"},
	DBH:  {lat: 33.64326, long: -117.84198, name: "Donald Bren Hall"},
	EH:   {lat: 33.64376, long: -117.84101, name: "Engineering Hall"},
	ELH:  {lat: 33.64447, long: -117.84071, name: "Engineering Lecture Hall"},
	HG:   {lat: 33.64825, long: -117.84451, name: "Humanities Gateway"},
	HH:   {lat: 33.64733, long: -117.84398, name: "Humanities Hall"},
	HIB:  {lat: 33.64841, long: -117.84383, name: "Humanities Instructional Building"},
	HICF: {lat: 33.64687, long: -117.84680, name: "Humanities Interim Classroom Facility"},
	HSLH: {lat: 33.64559, long: -117.84466, name: "Howard Schneiderman Lecture Hall"},
	IAB:  {lat: 33.64822, long: -117.84534, name: "Intercollegiate Athletics Building"},
	ICF:  {lat: 33.64443, long: -117.83997, name: "Interim Classroom Facility"},
	ICS:  {lat: 33.64428, long: -117.84180, name: "Information & Computer Science"},
	LLIB: {lat: 33.64713, long: -117.84109, name: "Langson Library"},
	MM:   {lat: 33.64933, long: -117.84445, name: "Music & Media Building"},
	MPAA: {lat: 33.64707, long: -117.83695, name: "Multipurpose Academic & Administrative Building"},
	MSTB: {lat: 33.64208, long: -117.84442, name: "Multipurpose Science & Technology Building"},
	PCB:  {lat: 33.64451, long: -117.84281, name: "Parkview Classroom Building"},
	PSCB: {lat: 33.64341, long: -117.84349, name: "Physical Sciences Classroom Building"},
	PSLH: {lat: 33.64340, long: -117.84396, name: "Physical Sciences Lecture Hall"},
	RH:   {lat: 33.64451, long: -117.84412, name: "Rowland Hall"},
	SBSG: {lat: 33.64737, long: -117.83909, name: "Social & Behavioral Sciences Gateway"},
	SE:   {lat: 33.64615, long: -117.83889, name: "Social Ecology I"},
	SE2:  {lat: 33.64656, long: -117.83915, name: "Social Ecology II"},
	SH:   {lat: 33.64621, long: -117.84484, name: "Steinhaus Hall"},
	SSH:  {lat: 33.64623, long: -117.84007, name: "Social Science Hall"},
	SSL:  {lat: 33.64590, long: -117.84000, name: "Social Science Lab"},
	SSLH: {lat: 33.64723, long: -117.83973, name: "Social Science Lecture Hall"},
	SSPA: {lat: 33.64694, long: -117.83955, name: "Social Science Plaza A"},
	SST:  {lat: 33.64646, long: -117.84027, name: "Social Science Tower"},
	SSTR: {lat: 33.64698, long: -117.84024, name: "Social Science Trailer"}
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
forGeo(function (e, o) {
	L.circle([e.lat, e.long]).bindPopup(e.name + " (" + o + ")").addTo(leafletmap);
});

var bubble;
leafletmap.locate({watch: true}).on("locationfound", function(e) {
	if (bubble)
		bubble.removeFrom(leafletmap);
	bubble = L.circle([e.latitude, e.longitude], e.accuracy / 2, {
		weight: 0,
		fillColor: "#00ffff",
		fillOpacity: 0.25
	}).addTo(leafletmap).bringToBack();
}).on("locationerror", function(e){
	console.log(e.message);
});

/* Table */
forGeo(function (e, k) {
	var td, tr = document.getElementById("listbox").getElementsByTagName("tbody")[0].insertRow();
	td = tr.insertCell();
	td.innerHTML = e.name;
	td = tr.insertCell();
	td.innerHTML = k;
	td = tr.insertCell();
	td.innerHTML = e.long;
});
