/* Extracting Room Data from http://www.classrooms.uci.edu/GAC/
var x = {};
var log = "";
Array.from(document.getElementsByTagName("a")) // Get all anchors.
.map(function(e){return e.innerHTML.split(" ");}) // Split anchors by spaces.
.filter(function(e){return e.length == 2 ? e[1].match(/\d/) : 0;}) // Keep anchors of two parts if the second has digits.
.forEach(function(e){x[e[0]] ? x[e[0]].push(e[1]) : x[e[0]] = [e[1]];}); // Create dictionary with building keys and room values.
for(i in x){log += "\t" + i + ":\t" + (i.length < 3 ? "\t" : "") + "[\"" + x[i].join("\", \"") + "\"],\n"} // Create string of dictionary.
console.log("var room = {\n" + log.slice(0, log.length - 2) + "\n};"); // Print dictionary.
*/

/* Extracting Term Codes from https://www.reg.uci.edu/perl/WebSoc
var log = [];
Array.from(document.forms[1].YearTerm.options) // Get all yearterm options.
.map(function(e){return e.value.split("-")[1];}) // Extract the term code from each option..
.forEach(function(e){if(!log.includes(e)){log.push(e);}}); // Compile list of unique term codes.
console.log("var terms = [\"" + log.join("\", \"") + "\"].map(function(e){return year + \"-\" + e;});"); // Print list.
*/

/* For Use on https://www.reg.uci.edu/perl/WebSoc */
javascript:

if (location != "https://www.reg.uci.edu/perl/WebSoc") {
	open("https://www.reg.uci.edu/perl/WebSoc");
}
else {
	var results;
	step1();
}

function step1() {
	/* Time */
	var date = new Date();
	var time = {
		day: ["u", "m", "t", "w", "h", "f", "s"][date.getDay()],
		now: date.getHours() + date.getMinutes() / 60
	};
	
	var year = date.getFullYear();
	var terms = ["76", "39", "25", "14", "03", "92", "51"] // List of term codes.
		.map(e => year + "-" + e); // Append current year to each term code.
	
	var data, xhr = [];
	for (var i = 0; i < terms.length; i++) {
		data = new FormData(document.forms[1]);
		data.set("YearTerm", terms[i]);
		xhr[i] = new XMLHttpRequest();
		xhr[i].open("POST", location, true);
		xhr[i].onload = function() {
			if (this.response.includes("Current")) {
				time.term = terms[xhr.indexOf(this)];
				step2(time);
			}
		};
		xhr[i].send(data);
	}
}

function step2(t) {
	/* Location */
	var room = {
		BS3:  ["1200"],
		DBH:  ["1100", "1200", "1300", "1420", "1422", "1423", "1425", "1427", "1429", "1431", "1433", "1500", "1600"],
		EH:   ["1200"],
		ELH:  ["100", "110"],
		HG:   ["1800", "2310", "2320"],
		HH:   ["100", "105", "108", "112", "118", "142", "143", "156", "178", "210", "214", "220", "224", "226", "230", "231", "232", "236", "242", "254", "262"],
		HIB:  ["100", "110"],
		HICF: ["100K", "100L", "100M", "100N", "100P", "100Q"],
		HSLH: ["100A"],
		IAB:  ["128", "129", "130", "131"],
		ICF:  ["101", "102", "103"],
		ICS:  ["174", "180", "209", "213"],
		LLIB: ["101A"],
		MM:   ["116"],
		MPAA: ["320", "330"],
		MSTB: ["110", "114", "118", "120", "122", "124"],
		PCB:  ["1100", "1200", "1300"],
		PSCB: ["120", "140", "210", "220", "230", "240"],
		PSLH: ["100"],
		RH:   ["101", "104", "108", "114", "184", "188", "190", "192"],
		SBSG: ["G200"],
		SE:   ["101"],
		SE2:  ["1304", "1306"],
		SH:   ["128", "134", "174"],
		SSH:  ["100"],
		SSL:  ["105", "117", "119", "122", "129", "140", "145", "152", "155", "159", "162", "168", "171", "206", "228", "248", "270", "290"],
		SSLH: ["100"],
		SSPA: ["1100", "1165", "1170"],
		SST:  ["120", "122", "220A", "220B", "238"],
		SSTR: ["100", "101", "102", "103"]
	};
	var f, vacancies = [];
	
	var bldg = Object.keys(room);
	for (var i = 0; i < bldg.length; i++) {
		for (var j = 0; j < room[bldg[i]].length; j++) {
			if (i == bldg.length - 1 && j == room[bldg[i]].length - 1) {
				f = function(t, l, r) {
					step4(vacancies, t, l, r);
					step5(vacancies);
				};
			}
			else {
				f = function(t, l, r) {
					step4(vacancies, t, l, r);
				};
			}
			step3(t, {bldg: bldg[i], room: room[bldg[i]][j]}, f);
		}
	}
}

function step3(t, l, f) {
	/* Form */
	var form = new FormData(document.forms[1]);
	form.set("ShowComments", "0");
	form.set("ShowFinals", "0");
	form.set("Days", t.day);
	form.set("Bldg", l.bldg);
	form.set("Room", l.room);
	
	var xhr = new XMLHttpRequest();
	xhr.open("POST", location, true);
	xhr.onload = function() {
		f(t, l, this.response);
	};
	xhr.send(form);
}

function step4(v, t, l, r) {
	/* Response */
	var d = document.createElement("html");
	d.innerHTML = r;
	
	var unique = [];
	var occupied = [];
	
	Array.from(d.getElementsByTagName("td")) // Get list of all cells.
		.map(e => e.innerHTML.trim().replace(/&nbsp;/g, "")) // Remove trailing and nonbreaking spaces.
		.filter(e => e.match(/(Su|M|Tu|W|Th|F|Sa)+ +\d+:\d+.+\d+:\d+/)) // Keep properly format cells.
		.map(e => e.split(/[ -]+|:/).slice(1)) // Split each cell into starting and ending hour and minute.
		.forEach(function(e) {
			if(!unique.some(o => o[0] == e[0] && o[1] == e[1] && o[2] == e[2] && o[3] == e[3])) {
		  //if(!unique.some(function(o){return [0, 1, 2, 3].some(function(i){return o[i] == e[i];});})){
				unique.push(e);
			}
		}); // Compile list of unique times.
	
	unique.map(function(e) {
		var p = e[3].endsWith("p");
		return [
			p && (e[0] <= e[2] && e[2] != 12) ? Number(e[0]) + 12 : Number(e[0]),
			Number(e[1]),
			p && e[2] < 12 ? Number(e[2]) + 12 : Number(e[2]),
			Number(p ? e[3].slice(0, 2) : Number(e[3]))
		];
	}) // Convert to military time and to number type.
		.map(e => [e[0] + e[1] / 60, e[2] + (e[3] + 10) / 60]) // Convert to approximate decimal hours.
		.forEach(function(e) {
			var before = occupied.find(o => o[1] == e[0]); // Find classes that end when e starts.
			var after = occupied.find(o => e[1] == o[0]); // Find classes that start when e ends.
			if (before && after) {
				before[1] = after[1];
				occupied.splice(occupied.indexOf(after), 1);
			}
			else if (before) {
				before[1] = e[1];
			}
			else if (after) {
				after[0] = e[0];
			}
			else {
				occupied.push(e);
			}
		}); // Stitch together adjacent times.
	
	if (!occupied.some(e => e[0] <= t.now && t.now <= e[1])) { // Keep location if now is not in any occupied times.
	  //l.occupied = occupied;//Put times in location object.
		v.push(l);
	}
}

function step5(v) {
	/* Geolocation */
	var geo = {};
	
	navigator.geolocation.getCurrentPosition(function(e) {
		step6(v, e.coords);
	});
}

function distance(e, o) {
	return Math.sqrt(Math.pow(e.latitude - o.latitude, 2) + Math.pow(e.longitude - o.longitude, 2));
}

function step6(v, c) {
	/* Results */
	var geo = {
		BS3:  {latitude: 33.645323, longitude: -117.846083, name: "Biological Sciences III"},
		DBH:  {latitude: 33.643259, longitude: -117.841978, name: "Donald Bren Hall"},
		EH:   {latitude: 33.643764, longitude: -117.841012, name: "Engineering Hall"},
		ELH:  {latitude: 33.644470, longitude: -117.840714, name: "Engineering Lecture Hall"},
		HG:   {latitude: 33.648247, longitude: -117.844513, name: "Humanities Gateway"},
		HH:   {latitude: 33.647330, longitude: -117.843980, name: "Humanities Hall"},
		HIB:  {latitude: 33.648412, longitude: -117.843832, name: "Humanities Instructional Building"},
		HICF: {latitude: 33.646874, longitude: -117.846804, name: "Humanities Interim Classroom Facility"},
		HSLH: {latitude: 33.645587, longitude: -117.844662, name: "Howard Schneiderman Lecture Hall"},
		IAB:  {latitude: 33.648219, longitude: -117.845335, name: "Intercollegiate Athletics Building"},
		ICF:  {latitude: 33.644433, longitude: -117.839968, name: "Interim Classroom Facility"},
		ICS:  {latitude: 33.644283, longitude: -117.841800, name: "Information & Computer Science"},
		LLIB: {latitude: 33.647132, longitude: -117.841093, name: "Langson Library"},
		MM:   {latitude: 33.649325, longitude: -117.844454, name: "Music & Media Building"},
		MPAA: {latitude: 33.647068, longitude: -117.836951, name: "Multipurpose Academic & Administrative Building"},
		MSTB: {latitude: 33.642084, longitude: -117.844415, name: "Multipurpose Science & Technology Building"},
		PCB:  {latitude: 33.644509, longitude: -117.842806, name: "Parkview Classroom Building"},
		PSCB: {latitude: 33.643407, longitude: -117.843494, name: "Physical Sciences Classroom Building"},
		PSLH: {latitude: 33.643399, longitude: -117.843958, name: "Physical Sciences Lecture Hall"},
		RH:   {latitude: 33.644508, longitude: -117.844120, name: "Rowland Hall"},
		SBSG: {latitude: 33.647374, longitude: -117.839088, name: "Social & Behavioral Sciences Gateway"},
		SE:   {latitude: 33.646151, longitude: -117.838889, name: "Social Ecology I"},
		SE2:  {latitude: 33.646556, longitude: -117.839149, name: "Social Ecology II"},
		SH:   {latitude: 33.646210, longitude: -117.844836, name: "Steinhaus Hall"},
		SSH:  {latitude: 33.646225, longitude: -117.840065, name: "Social Science Hall"},
		SSL:  {latitude: 33.645902, longitude: -117.839999, name: "Social Science Lab"},
		SSLH: {latitude: 33.647227, longitude: -117.839731, name: "Social Science Lecture Hall"},
		SSPA: {latitude: 33.646939, longitude: -117.839552, name: "Social Science Plaza A"},
		SST:  {latitude: 33.646456, longitude: -117.840271, name: "Social Science Tower"},
		SSTR: {latitude: 33.646983, longitude: -117.840235, name: "Social Science Trailer"}
	};
	
	var rooms, bldgs = [];
	v.forEach(function(e) {
		if (!bldgs.includes(e.bldg)) {
			bldgs.push(e.bldg);
		}
	}); // Compile list of unique buildings.
	bldgs.sort((e, o) => distance(geo[e], c) - distance(geo[o], c));
	
	var help, available = "Available Classrooms:\n";
	for (var i = 0; i < bldgs.length; i++) {
		rooms = v.filter(e => e.bldg == bldgs[i]) // Get all locations of building.
			.map(e => e.room) // Get all rooms from buidling.
			.sort(); // Sort rooms.
		for (var j = 0; j < rooms.length; j++) {
			if (j == 0) {
				available += bldgs[i];
			}
			if ((j == 0 && (bldgs[i].length < 4 || bldgs[i].includes("I"))) || j != 0) {
				available += "\t";
			}
			available += "\t" + rooms[j] + "\n";
		}
	}
	
	while (help != "") {
		help = prompt(available);
		if (help != "") {
			alert(geo[help.toUpperCase()].name);
		}
	}
	
	results = {vacancies: v, bldgs: bldgs};
}

// Goals:
// Show how long a vacant class is available.
// Show how long until an occupied class becomes available.
// Include non General Assignement Classrooms.
// Organize variables in a smoother way.
// Include a map with results using Google Maps API.
