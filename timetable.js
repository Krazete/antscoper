var TimeTable = {
    "getTime": function() {
		var date = new Date();
		return date.getHours() + date.getMinutes() / 60;
	},
    "getDay": function() {
		var date = new Date();
		return date.getDay();
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
					var time = TimeTable.getTime();
					var chapa = a[TimeTable.getDay()].every(e => e[1] < time || time+1 < e[0]);
					var chapb = b[TimeTable.getDay()].every(e => e[1] < time || time+1 < e[0]);
					return chapa - chapb;
				});
				table.innerHTML = "";
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
		var end = data.length;
		for (var i = start; i < end; i++) {
			var tr = table.insertRow();
			var td;
			td = tr.insertCell();
			td.innerHTML = data[i].id;
			td = tr.insertCell();
			var timeline = TimeTable.newTimeline(6, 24);
			td.appendChild(timeline);
			for (var j = 6 * 2; j < 24 * 2; j++) {
				if (data[i][TimeTable.getDay()].some(function(e) {return e[0] * 2 <= j && j < e[1] * 2})) {
					timeline.children[j - 6 * 2].classList.add("active");
				}
			}
			td = tr.insertCell();
			try {
				td.innerHTML = geo[data[i].id.split(" ", 1)[0]].distance;
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
