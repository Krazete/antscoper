var a = [[0, 1], [1, 2], [3, 5], [8, 10], [4, 9]];
var b = [[0, 2], [3, 10]];

function chronomerge(list) {
	var sorted = list.slice().sort();
	var merged = [];
	var found;
	for (var i = 0; i < sorted.length; i++) {
		found = false;
		for (var j = 0; j < merged.length; j++) {
			if (merged[j][0] <= sorted[i][0] && sorted[i][0] <= merged[j][1] && merged[j][1] <= sorted[i][1]) {
				merged[j][1] = sorted[i][1];
				found = true;
				break;
			}
		}
		if (!found) {
			merged.push(sorted[i]);
		}
	}
	return merged;
}

var c = chronomerge(a);
